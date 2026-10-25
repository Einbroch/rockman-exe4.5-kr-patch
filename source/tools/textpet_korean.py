"""Deterministic, source-pinned TextPet profile for the dialogue Hangul escape.

The English reference database allows all high bits in the printString family
(including 70 named specializations). Bit 4 is not a declared parameter and is
unused by the retail catalog. Requiring it to be zero excludes F9 FC from all
71 commands, so TextPet can use the longer table entry at a command boundary.
No source plugin or retail encoding is overwritten.
"""

from __future__ import annotations

import json
import re
import shutil
from pathlib import Path

from build_visibility_poc import ROOT, require_hash, sha
from korean_codec import HANGUL_BASE, HANGUL_COUNT, EXTRA_CHARACTER_INDICES, encode_character, encode_syllable


def prepare_plugins(destination: Path, extra_characters: set[str] | None = None) -> dict:
    config = json.loads((ROOT / "project.json").read_text(encoding="utf-8"))
    profile = config["textpet"]
    require_hash(ROOT / profile["exe"], profile["exe_sha256"])
    require_hash(ROOT / profile["dll"], profile["dll_sha256"])
    source = ROOT / profile["plugins"]
    for name, expected in profile["plugin_sha256"].items():
        require_hash(source / name, expected)
    if destination.exists():
        raise ValueError(f"refusing to overwrite plugins: {destination}")
    shutil.copytree(source, destination)
    ini = destination / "mmbn45-en.ini"
    original = ini.read_text(encoding="utf-8-sig")
    blocks = re.split(r"(?=^\[Command\]$)", original, flags=re.MULTILINE)
    changed_commands = []
    for i, block in enumerate(blocks):
        if not re.search(r"^base = F9 0C(?: |$)", block, re.MULTILINE):
            continue
        if "offs = 1.4" in block:
            raise ValueError("reserved bit has acquired a command parameter")
        changed_block, count = re.subn(r"^mask = FF 0F (FF|00)$", r"mask = FF 1F \1", block,
                                      flags=re.MULTILINE)
        if count != 1:
            raise ValueError("printString-family mask anchor changed")
        changed_commands.append(re.search(r"^name = (.+)$", block, re.MULTILINE).group(1))
        blocks[i] = changed_block
    if len(changed_commands) != 71 or "printString" not in changed_commands:
        raise ValueError("printString command family changed")
    changed = "".join(blocks)
    ini.write_text(changed, encoding="utf-8", newline="\n")
    table = destination / "exe45-utf8.tbl"
    original_table = table.read_text(encoding="utf-8-sig").rstrip("\r\n") + "\n"
    if "F9FC" in original_table:
        raise ValueError("source table already has a Hangul prefix")
    entries = [f"{encode_syllable(chr(cp)).hex().upper()}={chr(cp)}\n"
               for cp in range(HANGUL_BASE, HANGUL_BASE + HANGUL_COUNT)]
    extra_characters = extra_characters or set()
    if not extra_characters <= EXTRA_CHARACTER_INDICES.keys():
        raise ValueError("unknown extra-character mapping")
    entries.extend(f"{encode_character(ch).hex().upper()}={ch}\n"
                   for ch in sorted(extra_characters, key=EXTRA_CHARACTER_INDICES.get))
    table.write_text(original_table + "".join(entries), encoding="utf-8", newline="\n")
    return {
        "schema": 2,
        "source_plugin_sha256": profile["plugin_sha256"],
        "derived_plugin_sha256": {p.name: sha(p.read_bytes())
                                  for p in sorted(destination.iterdir()) if p.is_file()},
        "change": "71 mmbn45 F9 0C commands: mask byte 1 0F -> 1F; append all F9 FC syllables",
        "changed_commands": changed_commands,
        "reserved_command_bit": "byte 1 bit 4, outside every printString parameter",
        "hangul_syllables": HANGUL_COUNT,
        "extra_character_indices": {ch: EXTRA_CHARACTER_INDICES[ch] for ch in sorted(extra_characters)},
        "scope": "shared mmbn45/mmbn45s encoding table; renderer support and command-boundary evidence are consumer-specific",
    }


def command(plugins: Path) -> list[str]:
    config = json.loads((ROOT / "project.json").read_text(encoding="utf-8"))
    return [str(ROOT / config["textpet"]["exe"]), "Load-Plugins", str(plugins),
            "Game", config["textpet"]["game"]]
