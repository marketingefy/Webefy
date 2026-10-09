"""Build silent forward/reverse EFY background videos from the approved source.

The original Higgsfield clip stays outside the public website. Reversing actual
frames (rather than seeking in JavaScript) keeps playback smooth on phones.
"""
import argparse
from pathlib import Path
import shutil
import subprocess

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("source", type=Path)
parser.add_argument("--ffmpeg", default=shutil.which("ffmpeg"), required=not shutil.which("ffmpeg"))
args = parser.parse_args()
assets = Path(__file__).resolve().parents[1] / "public" / "assets"

for filename, sizing, quality in [
    ("evia-workshop-loop.mp4", "scale=1280:720:force_original_aspect_ratio=increase,crop=1280:720", "23"),
    ("evia-workshop-loop-mobile.mp4", "crop=trunc(ih*0.9/2)*2:ih:iw*0.43:0,scale=720:800", "24"),
]:
    graph = (
        f"[0:v]fps=24,{sizing},setsar=1,split=2[forward][to_reverse];"
        "[to_reverse]reverse[backward];"
        "[forward][backward]concat=n=2:v=1:a=0,format=yuv420p[loop]"
    )
    subprocess.run([
        args.ffmpeg, "-hide_banner", "-loglevel", "error", "-y",
        "-i", str(args.source), "-filter_complex", graph, "-map", "[loop]",
        "-an", "-c:v", "libx264", "-preset", "slow", "-crf", quality,
        "-movflags", "+faststart", str(assets / filename),
    ], check=True)
    print(filename, (assets / filename).stat().st_size, "bytes")

    # Use the same first frame and framing for the static fallback and video.
    poster = filename.replace("-loop", "").replace(".mp4", ".webp")
    subprocess.run([
        args.ffmpeg, "-hide_banner", "-loglevel", "error", "-y",
        "-i", str(assets / filename), "-frames:v", "1",
        "-quality", "86", str(assets / poster),
    ], check=True)
    if filename == "evia-workshop-loop.mp4":
        subprocess.run([
            args.ffmpeg, "-hide_banner", "-loglevel", "error", "-y",
            "-i", str(assets / filename), "-frames:v", "1",
            "-vf", "scale=1200:675", "-q:v", "2",
            str(assets / "evia-workshop-social.jpg"),
        ], check=True)
