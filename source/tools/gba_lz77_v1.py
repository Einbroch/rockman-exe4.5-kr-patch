"""GBA BIOS LZ77 (type 0x10) codec for in-place graphic edits.

compress() uses an optimal parse (literal 9 bits, match 17 bits) and never emits displacement 1, so the stream is
safe for the VRAM variant (SWI 0x12) as well as WRAM (SWI 0x11).
"""


def decompress(data, at=0):
    if data[at] != 0x10:raise ValueError('not LZ77 type 0x10')
    n = int.from_bytes(data[at + 1:at + 4], 'little');out = bytearray();p = at + 4
    while len(out) < n:
        f = data[p];p += 1
        for b in range(8):
            if len(out) >= n:break
            if f & (0x80 >> b):
                x = data[p] << 8 | data[p + 1];p += 2;l = (x >> 12) + 3;d = (x & 0xFFF) + 1
                if d > len(out):raise ValueError('LZ77 displacement before start')
                for _ in range(l):out.append(out[-d])
            else:out.append(data[p]);p += 1
    return bytes(out[:n]), p - at


def compress(raw):
    n = len(raw);INF = 1 << 60
    cost = [INF] * (n + 1);step = [None] * (n + 1);cost[n] = 0
    heads = {}
    longest = [(0, 0)] * n                   # every shorter length is a prefix of the longest match at the same d
    for i in range(n):
        key = raw[i:i + 3];best = (0, 0)
        if len(key) == 3:
            for j in reversed(heads.get(key, [])):
                d = i - j
                if d > 0x1000:break
                if d < 2:continue
                l = 0
                while l < 18 and i + l < n and raw[j + l] == raw[i + l]:l += 1
                if l > best[0]:
                    best = (l, d)
                    if l == 18 or i + l == n:break
            heads.setdefault(key, []).append(i)
        longest[i] = best
    for i in range(n - 1, -1, -1):
        c = 9 + cost[i + 1];s = (1, 0);l, d = longest[i]
        for ll in range(3, l + 1):
            if 17 + cost[i + ll] < c:c = 17 + cost[i + ll];s = (ll, d)
        cost[i] = c;step[i] = s
    out = bytearray(b'\x10' + n.to_bytes(3, 'little'));i = 0
    while i < n:
        flag_at = len(out);out.append(0);flag = 0
        for b in range(8):
            if i >= n:break
            l, d = step[i]
            if d:
                flag |= 0x80 >> b;x = (l - 3) << 12 | (d - 1);out += bytes((x >> 8, x & 0xFF))
            else:out.append(raw[i])
            i += l
        out[flag_at] = flag
    if decompress(bytes(out))[0] != raw:raise ValueError('LZ77 roundtrip')
    return bytes(out)
