#!/bin/bash
# Run generic batches sequentially from $1 until the gate pool is exhausted; stop on any failure.
cd "$(dirname "$0")/.."
n=$1
while true; do
  b=$(printf "%03d" $n)
  echo "=== batch $b $(date)"
  python -X utf8 tools/next_batch_generic_v1.py $b prepare component || { echo "STOP prepare $b"; break; }
  python -X utf8 tools/next_batch_generic_v1.py $b build check || { echo "STOP build/check $b"; break; }
  python -X utf8 tools/compare_coldboot_generic_v1.py $b 041 || true
  n=$((n+1))
done
