"""Native RGBA animation for mobile browsers; desktop keeps the packed video."""
from pathlib import Path
import subprocess
ROOT=Path(__file__).resolve().parents[2];target=ROOT/'public/assets/evia-contacto-movil-alpha-20261110.webp'
subprocess.run(['ffmpeg','-v','error','-threads','2','-i',str(ROOT/'public/assets/evia-contacto-completo-20261110.mp4'),'-filter_complex_threads','2','-filter_complex','[0:v]split[r][a];[r]crop=720:960:0:0,format=rgb24[rgb];[a]crop=720:960:720:0,format=rgb24,extractplanes=r[mask];[rgb][mask]alphamerge,fps=12,format=bgra[v]','-map','[v]','-c:v','libwebp_anim','-threads','2','-quality','85','-compression_level','4','-loop','0','-an','-y',str(target)],check=True)
# WebP animation's canvas background must also be transparent (Safari compositing).
s=target.read_bytes();i=s.find(b'ANIM');assert i>=12 and s[i+4:i+8]==b'\x06\x00\x00\x00';target.write_bytes(s[:i+8]+b'\0\0\0\0'+s[i+12:])
print('Native animation with RGBA frames and transparent animation canvas ready')
