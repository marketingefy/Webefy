"""Publish the static site with SFTP and a verified server host key."""
import os
from contextlib import contextmanager
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import uuid


def required(name):
    value = os.environ.get(name, "").strip()
    if not value:
        raise ValueError(f"Missing GitHub setting: {name}")
    return value


@contextmanager
def key_agent(root, key_path, passphrase):
    """Unlock the key without placing its passphrase in files, arguments or logs."""
    result = subprocess.run(
        ["ssh-agent", "-s", "-a", str(root / "agent.sock")],
        check=True, capture_output=True, text=True, timeout=10,
    )
    socket = re.search(r"SSH_AUTH_SOCK=([^;]+);", result.stdout)
    pid = re.search(r"SSH_AGENT_PID=(\d+);", result.stdout)
    if not socket or not pid:
        raise ValueError("Could not start SSH agent")
    env = os.environ.copy()
    env.pop("SSH_PRIVATE_KEY", None)
    env.pop("SSH_KEY_PASSPHRASE", None)
    env.update(SSH_AUTH_SOCK=socket.group(1), SSH_AGENT_PID=pid.group(1))
    try:
        askpass = root / "askpass"
        marker = root / "passphrase-attempted"
        marker.unlink(missing_ok=True)
        askpass.write_text(
            '#!/bin/sh\n'
            'if [ -f "$EFY_ASKPASS_MARKER" ]; then printf \'\\n\'; exit 0; fi\n'
            ': > "$EFY_ASKPASS_MARKER"\n'
            'printf \'%s\\n\' "$EFY_KEY_PASSPHRASE"\n'
        )
        askpass.chmod(0o700)
        unlock_env = env.copy()
        unlock_env.update(
            SSH_ASKPASS=str(askpass), SSH_ASKPASS_REQUIRE="force",
            DISPLAY="efy:0", EFY_KEY_PASSPHRASE=passphrase,
            EFY_ASKPASS_MARKER=str(marker),
        )
        unlocked = subprocess.run(
            ["ssh-add", str(key_path)], env=unlock_env,
            stdin=subprocess.DEVNULL, capture_output=True, timeout=30,
        )
        if unlocked.returncode:
            raise ValueError("Could not unlock SSH key. Check SSH_PRIVATE_KEY and SSH_KEY_PASSPHRASE in GitHub Secrets.")
        # Encrypted PEM keys need a public companion for IdentitiesOnly to match the agent.
        public = subprocess.run(
            ["ssh-add", "-L"], env=env, check=True,
            capture_output=True, text=True, timeout=10,
        )
        Path(str(key_path) + ".pub").write_text(public.stdout)
        yield env
    finally:
        subprocess.run(["ssh-agent", "-k"], env=env, capture_output=True, timeout=10)


def publish(check_only=False):
    host = required("SSH_HOST")
    user = required("SSH_USER")
    directory = required("SSH_DIRECTORY")
    key = required("SSH_PRIVATE_KEY")
    known_hosts = os.environ.get("SSH_KNOWN_HOSTS", "").strip()
    if not known_hosts:
        known_hosts = (Path(__file__).resolve().parents[1] / ".github/hostgator_known_hosts").read_text()
    port = int(os.environ.get("SSH_PORT", "22"))
    if not re.fullmatch(r"[A-Za-z0-9.-]+", host) or not re.fullmatch(r"[A-Za-z0-9_-]+", user):
        raise ValueError("Invalid SSH host or username")
    if not 1 <= port <= 65535:
        raise ValueError("Invalid SSH port")
    if not directory.startswith("/") or not re.fullmatch(r"[A-Za-z0-9_/.-]+", directory) or ".." in directory.split("/"):
        raise ValueError("SSH_DIRECTORY must be a confirmed absolute site path")
    site = Path(__file__).resolve().parents[1] / "public"
    if not (site / "index.html").is_file():
        raise ValueError("Required site files are missing")
    if any(p.is_symlink() for p in site.rglob("*")):
        raise ValueError("Symlinks are not allowed in published files")
    files = sorted(p for p in site.rglob("*") if p.is_file() and p.name != "index.html")
    temporary = ".efy-index-" + uuid.uuid4().hex + ".html"
    commands = ['cd "' + directory + '"']
    directories = sorted((p for p in site.rglob("*") if p.is_dir()), key=lambda p: len(p.parts))
    for path in directories:
        commands.append('-mkdir "' + path.relative_to(site).as_posix() + '"')
    for path in files:
        relative = path.relative_to(site).as_posix()
        if not re.fullmatch(r"[A-Za-z0-9_/.-]+", relative):
            raise ValueError("Unsupported site filename")
        commands.append('put "' + path.as_posix() + '" "' + relative + '"')
    commands.extend([
        'put "' + (site / "index.html").as_posix() + '" "' + temporary + '"',
        'rename "' + temporary + '" "index.html"',
    ])
    if check_only:
        commands = ['cd "' + directory + '"', 'pwd', 'ls -la .']
    with tempfile.TemporaryDirectory(prefix="efy-sftp-") as temporary_directory:
        root = Path(temporary_directory)
        key_path = root / "key"
        key_path.write_text(key + "\n")
        key_path.chmod(0o600)
        hosts_path = root / "known_hosts"
        hosts_path.write_text(known_hosts + "\n")
        hosts_path.chmod(0o600)
        batch_path = root / "commands"
        batch_path.write_text("\n".join(commands) + "\n")
        with key_agent(root, key_path, os.environ.get("SSH_KEY_PASSPHRASE", "")) as agent_env:
            subprocess.run([
                "sftp", "-b", str(batch_path), "-i", str(key_path), "-P", str(port),
                "-o", "BatchMode=yes", "-o", "IdentitiesOnly=yes",
                "-o", "StrictHostKeyChecking=yes", "-o", "ConnectTimeout=30",
                "-o", "UserKnownHostsFile=" + str(hosts_path), user + "@" + host,
            ], check=True, env=agent_env)
    if check_only:
        print("SSH authentication and site directory access verified. No remote files modified.")
    else:
        print("Site published. Other remote files were not deleted.")


if __name__ == "__main__":
    try:
        if sys.argv[1:] not in ([], ["--check"]):
            raise ValueError("Use --check for a read-only connection test, or no arguments to publish.")
        publish(check_only=sys.argv[1:] == ["--check"])
    except ValueError as error:
        print(str(error), file=sys.stderr)
        sys.exit(1)
    except subprocess.CalledProcessError:
        sys.exit(1)
