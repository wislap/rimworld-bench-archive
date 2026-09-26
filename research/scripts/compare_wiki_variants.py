"""Offline comparison for two completed Wiki variant runs."""
from __future__ import annotations
import json
import sys
from pathlib import Path


def read(root):
    rows=[]
    for p in sorted(Path(root).glob('[0-9][0-9]-*.json')):
        if '.started.' in p.name: continue
        d=json.loads(p.read_text());m=d['measurements'];e=d['evidence']
        rows.append({'id':d['case']['id'],'status':e['result']['status'],'requests':m['model_attempts'],
                     'tokens':m['known_total_tokens'],'tool_failures':m['tool_failures'],
                     'submission_failures':m['submission_failures'],
                     'tools':[t['function']['name'] for t in e['requests'][0]['input']['tools']]})
    b=json.loads((Path(root)/'budget.json').read_text())
    return {'cases':rows,'requests':sum(x['requests'] for x in rows),'tokens':sum(x['tokens'] for x in rows),
            'tool_failures':sum(x['tool_failures'] for x in rows),'submission_failures':sum(x['submission_failures'] for x in rows),
            'budget_attempts':b['attempts'],'budget_charged':b['charged']}

if __name__=='__main__':
    a=read(sys.argv[1]);b=read(sys.argv[2]);out={'left':a,'right':b}
    by={x['id']:x for x in a['cases']}
    for x in b['cases']:
        by[x['id']]['right']=x
    out['per_case']=list(by.values())
    print(json.dumps(out,ensure_ascii=False,indent=2))
