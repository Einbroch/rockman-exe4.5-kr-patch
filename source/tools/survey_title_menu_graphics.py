"""Find the title OBJ sheet by exact native VRAM bytes, not image resemblance."""
import json
from pathlib import Path
from build_visibility_poc import ROOT, sha
from verify_tpi_index import lz77_decompress


def main():
    source = (ROOT / json.loads((ROOT / 'project.json').read_text())['source_profile']['filename']).read_bytes()
    video = (ROOT / 'poc/runtime/title-menu-source-survey-v1/step_002_gbaVideoRam.bin').read_bytes()
    needle = video[0x10800:0x10840]
    matches = []
    for offset in range(0, len(source)-4, 4):
        if source[offset] != 0x10:
            continue
        size = int.from_bytes(source[offset+1:offset+4], 'little')
        if not 64 <= size <= 65536:
            continue
        try:
            payload, used = lz77_decompress(source, offset)
        except (ValueError, IndexError):
            continue
        at = payload.find(needle)
        if at >= 0:
            matches.append(dict(offset=offset, payload_at=at, size=size, consumed=used,
                                payload_sha256=sha(payload), stored_sha256=sha(source[offset:offset+used])))
    print(json.dumps(matches, indent=2))


if __name__ == '__main__':
    main()
