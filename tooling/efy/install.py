"""Restore the supplied skill bundle and its isolated runtimes without overwriting local files."""
from pathlib import Path, PurePosixPath
import hashlib
import stat
import subprocess
import sys
import zipfile

archive = Path(__file__).resolve().parent / 'skills-package.zip'
workspace = Path(__file__).resolve().parents[3]
tools = workspace / 'tools'
with zipfile.ZipFile(archive) as bundle:
    seen = set()
    for entry in bundle.infolist():
        relative = PurePosixPath(entry.filename)
        if relative.is_absolute() or '..' in relative.parts or entry.filename in seen:
            raise ValueError('Invalid or duplicate archive path')
        if stat.S_ISLNK(entry.external_attr >> 16):
            raise ValueError('Archive symlinks are not supported')
        seen.add(entry.filename)
        target = tools.joinpath(*relative.parts)
        if not target.resolve().is_relative_to(tools.resolve()):
            raise ValueError('Archive path escapes tool directory')
        if target.is_symlink():
            raise ValueError('Existing tool path is a symlink')
        if target.exists() and not entry.is_dir():
            if not target.is_file() or hashlib.sha256(target.read_bytes()).digest() != hashlib.sha256(bundle.read(entry)).digest():
                raise ValueError('Existing tool file differs; preserved: ' + entry.filename)
    for entry in bundle.infolist():
        target = tools.joinpath(*PurePosixPath(entry.filename).parts)
        if entry.is_dir():
            target.mkdir(parents=True, exist_ok=True)
        elif not target.exists():
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(bundle.read(entry))

root = tools / 'EFY-SKILLS-COMPLETAS-2026-10-09'
subprocess.run([sys.executable, str(root / 'instalar.py'), '--repo', str(workspace / 'Webefy'), '--destino', 'ambos', '--include-host-skills'], check=True)
for relative in ['animateicons', 'playwright', 'hyperframes/runtime']:
    subprocess.run(['npm', 'ci', '--ignore-scripts', '--cache', '/tmp/efy-npm-cache', '--no-audit', '--no-fund'], cwd=root / 'runtimes' / relative, check=True)
subprocess.run(['npm', 'rebuild', 'ffmpeg-static', '@derhuerst/ffprobe-static', '--cache', '/tmp/efy-npm-cache'], cwd=root / 'runtimes/hyperframes/runtime', check=True)
print('EFY skills and isolated runtimes installed. External services and optional voice models are not configured.')
