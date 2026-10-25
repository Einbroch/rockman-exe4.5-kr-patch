# Secondary description input investigation — 2026-10-03

Immutable source SHA256588a77da006fb0dca0c8addbcc316d7bd4b1c3a42db24750bcfe17b170ac5ef8.
Current cumulative ROM9a2a0be8342bad1c37c57213b3d322bcc6cd4240be707fa94f0f71a2ec30d424.

Source consumer at080D2922 loads descriptor halfword[r1+8];080D2926 shifts right7 to source chip ID. It calls080D4D5C at080D2952.
080D4D5C preserves the input and calls080D4CE0 at080D4D6A.
080D4CE0 initially loads secondary description root literal080D4D10; if source ID<=255 it instead loads primary root080D4D0C. It normalizes ID with0xFF at080D4CEE, then calls native fixed-cell parser080554A4 with width10,height3,font08619EF8.
These instructions were disassembled from immutable source with Capstone, not inferred from name-pool order.

First descriptor diagnostic targeted name row read0803CB48 only. It rendered secondary names but produced no secondary description calls. The native-samples receipt was marked incomplete and checkpoint quarantined; no PASS claim for that trial.
Second diagnostic additionally substitutes the source descriptor read at080D2922. It does not write descriptors, text bytes, ROM, progress flags or save RAM. Underlying source selection remains diagnostic, not normal chip acquisition.
Both runs retain the exact same646-unit ROM. No rebuild was required to test the corrected observation boundary.
Selected native IDs256,257,263,272,278,285,344 correspond to secondary scripts0,1,7,16,22,29,88. Their secondary description pointers must be matched to exact compiled archive entries before runtime evidence is credited.
