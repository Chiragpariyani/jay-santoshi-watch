#!/usr/bin/env python3
"""Make the home-page shop video from the photos in src/static/img.

Usage:  python3 src/make_video.py      (needs Pillow + ffmpeg; run only when photos change)
Output: src/static/video/shop-tour.webm, shop-tour.mp4 and shop-tour-poster.webp
"""
import os
import subprocess
import sys

from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from data import PHOTOS  # noqa: E402

SRC = os.path.dirname(os.path.abspath(__file__))
IMG = os.path.join(SRC, "static", "img")
OUT = os.path.join(SRC, "static", "video")
ORDER = ["storefront", "interior", "display", "station-clock", "alarm-clock"]  # first = poster
W, H, FPS = 480, 600, 24
HOLD, FADE = 3.0, 0.6  # seconds per photo, crossfade length
ZOOM = 0.08  # Ken Burns: zoom in by 8% over each photo


def cover(im):
    """Crop to W:H around the centre (a little above centre for portrait shots, to keep signboards)."""
    scale = max(W / im.width, H / im.height)
    im = im.resize((round(im.width * scale * 2), round(im.height * scale * 2)), Image.LANCZOS)  # 2x for smooth zoom
    cw, ch = W * 2, H * 2
    left = (im.width - cw) // 2
    top = int((im.height - ch) * (0.35 if im.height > im.width else 0.5))
    return im.crop((left, top, left + cw, top + ch))


def frame(base, t):
    """t in 0..1 → zoomed frame of size W×H."""
    z = 1 + ZOOM * t
    cw, ch = base.width / z, base.height / z
    x, y = (base.width - cw) / 2, (base.height - ch) / 2
    return base.resize((W, H), Image.LANCZOS, box=(x, y, x + cw, y + ch))


def frames():
    bases = [cover(Image.open(os.path.join(IMG, PHOTOS[k]["file"])).convert("RGB")) for k in ORDER]
    per = int((HOLD + FADE) * FPS)
    fade = int(FADE * FPS)
    for i, base in enumerate(bases):
        nxt = bases[(i + 1) % len(bases)]  # loop back to the first photo seamlessly
        for f in range(per - fade):
            yield frame(base, f / per)
        for f in range(fade):
            a = frame(base, (per - fade + f) / per)
            b = frame(nxt, f / per)
            yield Image.blend(a, b, (f + 1) / fade)


def encode():
    os.makedirs(OUT, exist_ok=True)
    raw = b"".join(im.tobytes() for im in frames())
    common = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
              "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-an", "-pix_fmt", "yuv420p"]
    targets = [
        common + ["-c:v", "libvpx-vp9", "-b:v", "0", "-crf", "40", "-row-mt", "1", "-deadline", "good",
                  os.path.join(OUT, "shop-tour.webm")],
        common + ["-c:v", "libx264", "-profile:v", "main", "-crf", "28", "-preset", "slow",
                  "-movflags", "+faststart", os.path.join(OUT, "shop-tour.mp4")],
    ]
    for cmd in targets:
        subprocess.run(cmd, input=raw, check=True)
    first = cover(Image.open(os.path.join(IMG, PHOTOS[ORDER[0]]["file"])).convert("RGB")).resize((W, H), Image.LANCZOS)
    first.save(os.path.join(OUT, "shop-tour-poster.webp"), "WEBP", quality=78, method=6)
    for n in ("shop-tour.webm", "shop-tour.mp4", "shop-tour-poster.webp"):
        print(n, os.path.getsize(os.path.join(OUT, n)) // 1024, "KB")


if __name__ == "__main__":
    encode()
