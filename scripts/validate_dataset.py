#!/usr/bin/env python3
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'data/long_context_qa_curated_20.jsonl'
raw=DATA.read_bytes()
assert not raw.startswith(b"\xef\xbb\xbf"), "JSONL has BOM"
assert raw.endswith(b"\n"), "JSONL needs trailing newline"
rows=[json.loads(x) for x in raw.decode('utf-8').splitlines() if x.strip()]
assert len(rows)==20
assert len({r['track_id'] for r in rows})==20
assert len({r['context_id'] for r in rows})==20
assert sum(r['question_type']=='短答案题' for r in rows)==15
assert sum('选择题' in r['question_type'] for r in rows)==5
outputs=0
for r in rows:
    context_path=ROOT/r['file_path']
    assert context_path.read_text(encoding='utf-8')==r['context']
    dr=r['difficulty_result']
    assert dr['rollout_count']==8 and len(dr['rollout_results'])==8
    for rr in dr['rollout_results']:
        p=ROOT/rr['raw_output_file']
        assert p.read_text(encoding='utf-8')==rr['raw_output']
        outputs+=1
r26=next(r for r in rows if r['track_id'].endswith('000026'))
assert r26['answer'][0]=='[Answer]'
a26=json.loads(r26['answer'][1])
assert [x['sentence_id'] for x in a26]==['S1','S2','S3','S4']
r37=next(r for r in rows if r['track_id'].endswith('000037'))
assert r37['question_type']=='选择题'
print(f"PASS · {len(rows)} records · {len(rows)} contexts · {outputs} rollouts")
