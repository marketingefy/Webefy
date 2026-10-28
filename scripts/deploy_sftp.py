"""Publish the static site with SFTP and a verified server host key."""
import os
from contextlib import contextmanager
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import uuid

CACHE_START = '# BEGIN EFY HTML REVALIDATION'
CACHE_END = '# END EFY HTML REVALIDATION'
CACHE_RULES = f'''{CACHE_START}
<IfModule mod_headers.c>
  <FilesMatch "\\.html$">
    Header always set Cache-Control "no-cache, max-age=0, must-revalidate"
  </FilesMatch>
</IfModule>
{CACHE_END}'''


def merge_html_cache_rules(existing):
    """Preserve cPanel, HTTPS and other site rules while managing only our block."""
    starts, ends = existing.count(CACHE_START), existing.count(CACHE_END)
    if starts != ends or starts > 1:
        raise ValueError('Ambiguous Efy cache block; refusing to replace Apache configuration')
    if starts:
        first, last = existing.index(CACHE_START), existing.index(CACHE_END)
        if last < first:
            raise ValueError('Invalid Efy cache block order')
        return existing[:first] + CACHE_RULES + existing[last + len(CACHE_END):]
    return existing + ('\n' if existing and not existing.endswith('\n') else '') + CACHE_RULES + '\n'


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
    files = sorted(p for p in site.rglob("*") if p.is_file() and p != site / "index.html")
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
            sftp_command = [
                "sftp", "-i", str(key_path), "-P", str(port),
                "-o", "BatchMode=yes", "-o", "IdentitiesOnly=yes",
                "-o", "StrictHostKeyChecking=yes", "-o", "ConnectTimeout=30",
                "-o", "UserKnownHostsFile=" + str(hosts_path),
            ]
            if not check_only:
                # The server's root .htaccess is not owned by this repo. Read and
                # merge it instead of overwriting existing hosting configuration.
                cache_path = root / 'existing-htaccess'
                read_batch = root / 'read-cache'
                read_batch.write_text('cd "' + directory + '"\nget ".htaccess" "' + str(cache_path) + '"\n')
                fetched = subprocess.run(sftp_command + ['-b', str(read_batch), user + '@' + host],
                                         env=agent_env, capture_output=True, text=True, timeout=60)
                if fetched.returncode:
                    missing = re.search(r'(?:File "[^"\n]*\.htaccess" not found|(?:stat|open) remote "[^"\n]*\.htaccess": No such file or directory)', fetched.stderr)
                    if not missing:
                        raise ValueError('Could not read existing Apache configuration; publication stopped to preserve it')
                    existing = ''
                else:
                    existing = cache_path.read_text()
                merged = root / 'merged-htaccess'
                merged.write_text(merge_html_cache_rules(existing))
                remote_cache = '.efy-cache-' + uuid.uuid4().hex
                # Apply the cache rule after the assets and before the new homepage.
                commands[-2:-2] = ['put "' + str(merged) + '" "' + remote_cache + '"',
                                   'rename "' + remote_cache + '" ".htaccess"']
                batch_path.write_text('\n'.join(commands) + '\n')
            subprocess.run(sftp_command + ['-b', str(batch_path), user + '@' + host], check=True, env=agent_env)
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
