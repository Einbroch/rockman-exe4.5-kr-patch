# 029 continuation — conditional array providers, NOT product adoption

Historical investigation checkpoint. Subsequent work completed the029 development cohort; current authority is `analysis/pending500_029_v1/batch_status.json` and `analysis/PENDING_INSERTION_500_029_HANDOFF.md`. The no029-ROM statements below describe the earlier investigation only.

## Current playable authority stays 028

- Latest completed cohort: `pending500_028_v1.gba`, SHA-256 `66d93c8f0142f2d5e5a48e112af995af5f40e7d031627b9c362878573a95f3ef`.
- Completion authority remains `analysis/pending500_028_v1/batch_status.json` and `analysis/PENDING_INSERTION_500_028_HANDOFF.md`.
- This investigation applies **0 new units**, builds no029 ROM and creates no distribution package. User still requests500-unit cohorts and no BPS/xdelta/ZIP until explicitly requested.

## New evidence

1. Actual028 narrow recensus: `analysis/pending_insertion_500_029_survey_v1/survey.json`.
2. Native producer route: normal FC dispatch pointer500F4 ->51C54; subcommand0F table entry51CA4 ->51DD4 ->38A94 ->38B94. Source row3B0D0 drives active-record count, logical cap, descriptor and record base. Real helper32AC6 copies bytes through E5 without suffix. F90C reader517D0 copies descriptor bytes into dialogue scratch.
3. `tools/bench_profile_arrays_029.py` -> `analysis/pending_insertion_500_029_array_cpu_v1/cpu.json`: **34,256 source/028 fixtures PASS**, all active-record masks, enabled/disabled state, every active selected slot, native lengths0..cap with two token fixtures. Native helpers execute unchanged; BIOS Div only is modeled. No ROM or userdata writes outside declared test fixtures. Every source/product code span is byte-identical and bounded ARMv4T round-tripped.
4. First RNG seed generator failed complete selection coverage because low16 seeds alone did not vary the carry-in from bit31. Before freezing successful evidence, fixed the fixture generator to include both bit31 states and the actual native rotate/add/xor expression. No game code changed.
5. Quarantined actual028 GBA diagnostic `poc/runtime/profile-array-029-friend-v1`: source AquaMan69B134:18 selected with root/table read aliases, while own Rockman remains PET host. Temporary valid six-glyph native records/enable flag at the real FC0F handler; actual producer selects one, copies cache, actual F90C reader copies dialogue scratch. Original records/flag restored and verified before rendering. Six actual glyph234 draws observed at offsets0,44,88,132,176,220. Screenshot viewed: six native small kana followed by the source Japanese first page. This is intentionally **not translated029 output**.
6. `analysis/pending_insertion_500_029_array_runtime_v1/verification.json`: independent bounded trace verifier PASS, captures and tool hashes pinned.

## Conditional analysis, not admission

- `tools/pet_array_capacity_029.py` extends only the analysis model with conditional valid/prepared/lifetime-preserved array cache bounds. Native caps6 for siblings/friend and8 for hobby/show/wish come from editor source table, not13/17 descriptor byte capacities.
- `tools/survey_layout500_029_v1.py` -> `analysis/pending_insertion_500_029_layout_v1/survey.json` finds689 array-provider literal candidates,119 direct-profile,6 normal,3 vertical,25 unadopted guards. These are model-specific candidates, not a whole-game remaining count.
- Conditional exact500 subset exists:162 whole scripts, all array-provider profile. It is analysis-only; every group `product_admitted=false`; no preflight/build registration created.
- Some cloned survey human-readable labels still say025; machine-readable baseline SHA and029 paths are authority. Do not mutate these pinned scripts just to rename stdout. Create a new version if implementation changes.

## Next work

1. Establish native array-cache preparation/lifetime applicability for the chosen PET contexts. Caller candidate309EE ->38A9E loops26 rows; it is only statically located, **not runtime/natural caller proved**. Initial normal snapshot's scratch cache can hold graphics and may be unprepared/stale; never treat arbitrary descriptor contents as a valid record.
2. The current GBA test proves only friend source script18 first page, not hobby on its second page, other seven array display paths, natural AquaMan selection, full caller/default/import/writer/save behavior or any Hangul record support. Diagnostic checkpoint is ineligible as a normal-play checkpoint.
3. Before product adoption, bind new conditional bounds and runtime evidence to original source/current ROM, review complete selected wording/layout/controls, add fail-closed eligibility tests, reconstruct024->025->026->027->028 carry, register new model, compile whole scripts and independently verify final writes/repro/runtime.
4. Critical prior build architecture:027 and028 new RAW arcs are appended after the ordinary main loop. Compose current translated script bodies **before one allocation** at their relevant append stage. Main-loop carry alone misses these arcs.
5. Preserve028 finalizer-v2/caller-index correction, frozen builds/tools, original source, saves, prior packages. Do not infer release approval or automatic Hangul composition/save support.

## Repeat commands

```powershell
python -X utf8 tools/verify_profile_array_029.py
```

CPU and survey output artifacts are immutable once created. Reruns must reproduce identical frozen data or use a versioned output. The GBA run command is recorded in `poc/runtime/profile-array-029-friend-v1/result.json`/segment artifacts; use a fresh exact output path for a new observation.
