"""Prepare the approved twelve-second EVIA gesture film for the production hero.

The last half-second dissolves into the first half-second, then playback resumes
at that exact point. Gestures play forward throughout the 11.5-second cycle.
Original media stays outside public/. Posters use the encoded loop's first frame.
"""
import argparse
from pathlib import Path
import subprocess

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("source", type=Path)
args = parser.parse_args()
assets = Path(__file__).resolve().parents[1] / "public" / "assets"

for stem, sizing, quality in [
    ("evia-premium-gestures-20261029", "scale=1280:720:force_original_aspect_ratio=increase,crop=1280:720", "22"),
    ("evia-premium-gestures-mobile-20261029", "crop=trunc(ih*0.9/2)*2:ih:iw*0.384:0,scale=720:800", "23"),
]:
    graph = (
        f"[0:v]fps=24,trim=duration=12,{sizing},setsar=1,split=2[body][head];"
        "[body]trim=start=0.5,setpts=PTS-STARTPTS,fps=24,settb=AVTB[forward];"
        "[head]trim=duration=0.5,setpts=PTS-STARTPTS,fps=24,settb=AVTB[start];"
        "[forward][start]xfade=transition=fade:duration=0.5:offset=11,format=yuv420p[loop]"
    )
    movie = assets / (stem + ".mp4")
    subprocess.run([
        "ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
        "-i", str(args.source), "-filter_complex", graph, "-map", "[loop]",
        "-an", "-c:v", "libx264", "-preset", "slow", "-crf", quality,
        "-movflags", "+faststart", str(movie),
    ], check=True)
    subprocess.run([
        "ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
        "-i", str(movie), "-frames:v", "1", "-quality", "86",
        str(assets / (stem + ".webp")),
    ], check=True)
    print(movie.name, movie.stat().st_size, "bytes")
