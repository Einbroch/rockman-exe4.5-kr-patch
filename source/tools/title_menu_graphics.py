"""Same-slot title labels: original 52 OBJ tiles, layout, palette and loader."""
import json
import re
import struct
from build_visibility_poc import ROOT, sha, bdf_glyphs, require_hash, FONT_SHA256
from verify_tpi_index import lz77_decompress
from lz10_greedy import encode as compress

BASE = 0x7CEA94
STORED = 657
SIZE = 1668
DIGEST = 'adfb7a3b6fbaf35eb7c76712bf9dae0382be954222ace022743444401526b626'
SOURCE_SHA = '588a77da006fb0dca0c8addbcc316d7bd4b1c3a42db24750bcfe17b170ac5ef8'


def decode(payload, column, width=48):
    return [[(payload[4 + ((y//8)*26 + column + x//8)*32 + y%8*4 + x%8//2]
              >> (4*(x%2))) & 15 for x in range(width)] for y in range(16)]


def encode(payload, rows, column):
    for y, row in enumerate(rows):
        for x, role in enumerate(row):
            at = 4 + ((y//8)*26 + column + x//8)*32 + y%8*4 + x%8//2
            shift = 4*(x%2)
            payload[at] = (payload[at] & ~(15 << shift)) | (role << shift)


def construct(source, asset):
    expected = [(u['id'], u['source'], u['translation'], u['tile_column']) for u in asset['units']]
    original_units=[('title.new_game', 'はじめから', '처음부터', 0),
                    ('title.continue', 'つづきから', '이어하기', 10)]
    if expected not in [original_units, original_units+[('title.weekend_tournament', 'どにちのたいかい', '주말 대회', 16)]]:
        raise ValueError('title wording/identity mismatch')
    if sha(source) != SOURCE_SHA or asset['source_sha256'] != SOURCE_SHA:
        raise ValueError('title source mismatch')
    if (asset['source_offset'], asset['stored_bytes'], asset['decompressed_bytes'],
        asset['source_stored_sha256']) != (BASE, STORED, SIZE, DIGEST):
        raise ValueError('title boundary mismatch')
    if asset['policy'] != 'development-draft; NON-DISTRIBUTION' or asset['release_eligible'] is not False:
        raise ValueError('title development policy')
    if asset['advance'] != 11 or asset['origin'] != [1, 2] or asset['font_sha256'] != FONT_SHA256:
        raise ValueError('title adopted typography mismatch')
    old = source[BASE:BASE+STORED]
    if sha(old) != DIGEST:
        raise ValueError('title slot mismatch')
    refs = [m.start() for m in re.finditer(re.escape(struct.pack('<I', 0x08000000+BASE)), source)]
    if refs != [0x2910C]:
        raise ValueError('title literal lookup mismatch')
    payload, used = lz77_decompress(old, 0)
    if used != STORED or len(payload) != SIZE or payload[:4] != bytes.fromhex('00840600'):
        raise ValueError('title sheet metadata mismatch')
    require_hash(ROOT / asset['font'], FONT_SHA256)
    g = bdf_glyphs(ROOT / asset['font'], set(''.join(u['translation'] for u in asset['units']).replace(' ','')))
    final = bytearray(payload)
    allowed = set()
    for unit in asset['units']:
        column = unit['tile_column']
        width=80 if column==16 else 48
        original = decode(payload, column, width)
        roundtrip = bytearray(payload)
        encode(roundtrip, original, column)
        if roundtrip != payload or set(c for row in original for c in row) != {0, 1, 2}:
            raise ValueError('title unchanged roundtrip / roles')
        rows = [[0]*width for _ in range(16)]
        pen=1
        for ch in unit['translation']:
            if ch==' ':
                pen+=4
                continue
            glyph = g[ch]
            # Render all shadows first; overlapping adjacent glyphs retain ink.
            for role, native in [(2, 2), (3, 1)]:
                for y in range(12):
                    for x in range(16):
                        actual = (glyph[y*8+x//2] >> (4*(x%2))) & 15
                        if actual != role:
                            continue
                        px, py = pen+x, 2+y
                        if not (0 <= px < width and 0 <= py < 16):
                            raise ValueError('title glyph overflow')
                        if native == 1 or rows[py][px] == 0:
                            rows[py][px] = native
            pen+=11
        encode(final, rows, column)
        if decode(final, column, width) != rows:
            raise ValueError('title modified roundtrip')
        for row in (0, 1):
            for tile in range(column, column+width//8):
                allowed.update(range(4+(row*26+tile)*32, 4+(row*26+tile+1)*32))
    if any(a != b and i not in allowed for i, (a,b) in enumerate(zip(payload, final))):
        raise ValueError('title protected sheet pixels/metadata changed')
    stored = compress(bytes(final), output_limit=SIZE, stored_limit=STORED)
    padded = stored + bytes(STORED-len(stored))
    if lz77_decompress(padded, 0)[0] != final:
        raise ValueError('title compressed roundtrip')
    return padded, dict(asset, final_stored_sha256=sha(padded), final_payload_sha256=sha(final),
                        source_payload_sha256=sha(payload), compressed_bytes=len(stored),
                        source_offset=BASE, native_references=refs,
                        protected_pixels_equal=True, unchanged_roundtrip=True,
                        translated_graphic_labels=len(asset['units']), runtime='pending exact-ROM menu states')


if __name__ == '__main__':
    source = (ROOT / json.loads((ROOT / 'project.json').read_text())['source_profile']['filename']).read_bytes()
    asset = json.loads((ROOT / 'translations/title_menu_graphics_ko.json').read_text(encoding='utf-8'))
    stored, record = construct(source, asset)
    print(json.dumps(record, ensure_ascii=False, indent=2))
