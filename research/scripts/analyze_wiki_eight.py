"""Offline accounting and readable transcripts; no model dispatch."""
import json
import argparse
from collections import Counter
from pathlib import Path

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--out', type=Path, default=Path(__file__).resolve().parent.parent / '.bench-results/wiki-eight-live-20260922')
ROOT = parser.parse_args().out.resolve()
(ROOT / 'review').mkdir(exist_ok=True)
rows = []
models = Counter()
for path in sorted(ROOT.glob('[0-9][0-9]-*.json')):
    if '.started.' in path.name:
        continue
    data = json.loads(path.read_text())
    evidence, metrics = data['evidence'], data['measurements']
    calls = []
    for request in evidence['requests']:
        models[request['response']['model']] += 1
        for call in request['response'].get('tool_calls', []):
            fn = call['function']
            calls.append({'round': request['attempt'], 'name': fn['name'], 'arguments': fn['arguments']})
    count = Counter(c['name'] for c in calls)
    row = dict(id=data['case']['id'], question=data['case']['question'], status=evidence['result']['status'],
               requests=metrics['model_attempts'], tokens=metrics['known_total_tokens'],
               input_tokens=metrics['known_input_tokens'], output_tokens=metrics['known_output_tokens'],
               cached_tokens=metrics['known_cached_tokens'], missing_usage=metrics['requests_missing_usage'],
               seconds=metrics['elapsed_seconds'], tool_calls=dict(count),
               initial_tools=[t['function']['name'] for t in evidence['requests'][0]['input']['tools']],
               initial_prompt_tokens=evidence['requests'][0]['usage']['prompt_tokens'])
    rows.append(row)
    (ROOT/'review'/f'{path.stem}-calls.json').write_text(json.dumps(calls,ensure_ascii=False,indent=2))
summary = dict(planned=8, completed=len(rows), runtime_ok=sum(r['status']=='ok' for r in rows),
               requests=sum(r['requests'] for r in rows), tokens=sum(r['tokens'] for r in rows),
               cached_tokens=sum(r['cached_tokens'] for r in rows),
               missing_usage=sum(r['missing_usage'] for r in rows), response_models=dict(models), cases=rows,
               limitations=['Single current arm, one run per case; no paired baseline.',
                'Actual first-request tool surface is recorded per case; verify before comparing runs.',
                'Real frozen world and real Def captures differ in capture date; applicability remains unverified.',
                'Runtime ok is not factual correctness. No currency cost calculated without provider invoice/rates.'])
budget=json.loads((ROOT/'budget.json').read_text())
assert summary['tokens']==budget['charged'] and summary['requests']==budget['attempts']
assert len(budget['reservations'])==summary['requests'] and all(r['settled'] for r in budget['reservations'].values())
(ROOT/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2))
print(json.dumps(summary,ensure_ascii=False,indent=2))
