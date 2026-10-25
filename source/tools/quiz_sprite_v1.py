"""Numberman quiz word sprite (archive 0x5131A4): frame tiles, OAM pieces and canvas compose/split helpers."""
import struct

ARCHIVE, BASE = 0x5131A4, 0x5131A8
SIZES = {(0, 0): (1, 1), (0, 1): (2, 2), (0, 2): (4, 4), (0, 3): (8, 8), (1, 0): (2, 1), (1, 1): (4, 1), (1, 2): (4, 2), (1, 3): (8, 4),
         (2, 0): (1, 2), (2, 1): (1, 4), (2, 2): (2, 4), (2, 3): (4, 8)}


def frame(rom, k):
    rec = BASE + struct.unpack_from('<I', rom, BASE + 4 * k)[0]
    ts, pal, _, oam, _ = struct.unpack_from('<5I', rom, rec)
    tiles = BASE + ts;size = struct.unpack_from('<I', rom, tiles)[0]
    o = BASE + oam;o += struct.unpack_from('<I', rom, o)[0];pieces = []
    while rom[o] != 0xFF:
        t, x, y, a, b = rom[o:o + 5];x -= 256 * (x > 127);y -= 256 * (y > 127)
        w, h = SIZES[(b & 3, a & 3)];pieces.append((t, x, y, w, h));o += 5
    return dict(tiles=tiles + 4, ntiles=size // 32, palette=BASE + pal + 4, pieces=pieces)


def canvas(rom, f, data=None):
    data = data if data is not None else rom[f['tiles']:f['tiles'] + f['ntiles'] * 32]
    x0 = min(p[1] for p in f['pieces']);y0 = min(p[2] for p in f['pieces'])
    W = max(p[1] + p[3] * 8 for p in f['pieces']) - x0;H = max(p[2] + p[4] * 8 for p in f['pieces']) - y0
    px = [[0] * W for _ in range(H)]
    for t, x, y, w, h in f['pieces']:
        for k in range(w * h):
            for yy in range(8):
                for xx in range(8):
                    b = data[(t + k) * 32 + yy * 4 + xx // 2];v = (b >> 4) if xx & 1 else b & 15
                    px[y - y0 + (k // w) * 8 + yy][x - x0 + (k % w) * 8 + xx] = v
    return px, (x0, y0)


def split(f, px, origin, data):
    out = bytearray(data);x0, y0 = origin
    for t, x, y, w, h in f['pieces']:
        for k in range(w * h):
            for yy in range(8):
                for xx in range(0, 8, 2):
                    cy, cx = y - y0 + (k // w) * 8 + yy, x - x0 + (k % w) * 8 + xx
                    out[(t + k) * 32 + yy * 4 + xx // 2] = px[cy][cx] | px[cy][cx + 1] << 4
    return bytes(out)
