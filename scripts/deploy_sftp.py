"""Publish the static site with SFTP and a verified server host key."""
import os
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


def publish():
    host = required("SSH_HOST")
    user = required("SSH_USER")
    directory = required("SSH_DIRECTORY")
    key = required("SSH_PRIVATE_KEY")
    known_hosts = required("SSH_KNOWN_HOSTS")
    port = int(os.environ.get("SSH_PORT", "22"))
    if not re.fullmatch(r"[A-Za-z0-9.-]+", host) or not re.fullmatch(r"[A-Za-z0-9_-]+", user):
        raise ValueError("Invalid SSH host or username")
    if not 1 <= port <= 65535:
        raise ValueError("Invalid SSH port")
    if not directory.startswith("/") or not re.fullmatch(r"[A-Za-z0-9_/.-]+", directory) or ".." in directory.split("/"):
        raise ValueError("SSH_DIRECTORY must be a confirmed absolute site path")
    site = Path(__file__).resolve().parents[1] / "public"
    if not (site / "index.html").is_file() or not (site / "assets/nuevo-comienzo.png").is_file():
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
        subprocess.run([
            "sftp", "-b", str(batch_path), "-i", str(key_path), "-P", str(port),
            "-o", "BatchMode=yes", "-o", "IdentitiesOnly=yes",
            "-o", "StrictHostKeyChecking=yes", "-o", "ConnectTimeout=30",
            "-o", "UserKnownHostsFile=" + str(hosts_path), user + "@" + host,
        ], check=True)
    print("Site published. Other remote files were not deleted.")


if __name__ == "__main__":
    try:
        publish()
    except ValueError as error:
        print(str(error), file=sys.stderr)
        sys.exit(1)
    except subprocess.CalledProcessError:
        sys.exit(1)
