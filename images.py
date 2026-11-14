#!/usr/bin/env python3
"""Скачивает фото по images.txt и делает две версии: _m (1600 px) и _s (800 px)."""
import io
import os
import sys
import urllib.request

from PIL import Image, ImageOps

HERE = os.path.dirname(os.path.abspath(__file__))
DEST = sys.argv[1] if len(sys.argv) > 1 else "/var/www/portfolio/img"
SIZES = {"m": 1600, "s": 800}


def main():
    ok = skip = fail = 0
    for line in open(os.path.join(HERE, "images.txt"), encoding="utf-8"):
        if not line.strip():
            continue
        path, url = line.split()
        base = os.path.join(DEST, path[:-4])
        if all(os.path.exists(f"{base}_{k}.jpg") for k in SIZES):
            skip += 1
            continue
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 portfolio-import"})
            with urllib.request.urlopen(req, timeout=60) as r:
                im = Image.open(io.BytesIO(r.read()))
            im = ImageOps.exif_transpose(im).convert("RGB")
            os.makedirs(os.path.dirname(base), exist_ok=True)
            for k, size in SIZES.items():
                v = im.copy()
                v.thumbnail((size, size), Image.LANCZOS)
                v.save(f"{base}_{k}.jpg", "JPEG", quality=85, optimize=True, progressive=True)
            ok += 1
            print(f"  {path}")
        except Exception as ex:  # noqa: BLE001
            fail += 1
            print(f"  ! {path}: {ex}")
    print(f"Фото: новых {ok}, уже были {skip}, ошибок {fail}")
    return fail


if __name__ == "__main__":
    sys.exit(1 if main() else 0)
