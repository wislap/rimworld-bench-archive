"""Offline model-visible Wiki trace diagnosis. No network or product changes."""
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / '.bench-results/wiki-eight-semantic-live-20260922'
OUT = SOURCE / 'diagnosis'
OUT.mkdir(exist_ok=True)


def decode(value):
    if isinstance(value, dict) and 'text_chunks' in value:
        value = ''.join(value['text_chunks'])
    if isinstance(value, str):
        try: return json.loads(value)
        except ValueError: return value
    return value


cases = []
for file in sorted(SOURCE.glob('[0-9][0-9]-*.json')):
    if '.started.' in file.name: continue
    data = json.loads(file.read_text())
    evidence = data['evidence']
    bound = {}
    # Two passes: a call result occurs in a later request's messages.
    for req in evidence['requests']:
        for message in req['input']['messages']:
            if message['role'] == 'tool': bound[message['tool_call_id']] = decode(message['content'])
    calls = []
    for req in evidence['requests']:
        for call in req['response'].get('tool_calls', []):
            fn = call['function']
            args = decode(fn['arguments'])
            result = bound.get(call['id'])
            row = dict(round=req['attempt'], id=call['id'], tool=fn['name'], arguments=args,
                       result_visible_in_next_request=result is not None)
            if fn['name'] == 'wiki':
                assert result is not None, call
                value = result.get('data', {})
                encoded = json.dumps(value, ensure_ascii=False).encode()
                metadata = {k:v for k,v in value.items() if k != 'entries'}
                row.update(status=value.get('status'), match_count=value.get('match_count'),
                           bytes=len(encoded), metadata_bytes=len(json.dumps(metadata,ensure_ascii=False).encode()),
                           entries=[])
                for entry in value.get('entries', []):
                    row['entries'].append({k:entry.get(k) for k in ('key','label','match','candidate','read_complete',
                        'missing_fields','not_read','not_read_count','context_not_read','context_not_read_count',
                        'response_truncated','directory','directory_truncated')})
                    row['entries'][-1]['facts'] = entry.get('facts', [])
            elif fn['name'] != 'submit_response':
                row['visible_result'] = result
            calls.append(row)
    case = dict(id=data['case']['id'], question=data['case']['question'],
                metrics=data['measurements'], calls=calls, rounds=[])
    for req in evidence['requests']:
        case['rounds'].append(dict(round=req['attempt'], usage=req['usage'],
                                  message_count=len(req['input']['messages']),
                                  tools=[c['function']['name'] for c in req['response']['tool_calls']]))
    cases.append(case)
    lines = [f"# {case['id']}", case['question'], '', evidence['result']['answer'], '']
    for c in calls:
        lines += [f"R{c['round']} {c['tool']} {json.dumps(c['arguments'],ensure_ascii=False)}"]
        if c['tool']=='wiki':
            lines.append(f"{c['status']}, matches={c['match_count']}, bytes={c['bytes']}, outer_metadata={c['metadata_bytes']}")
            for e in c['entries']:
                lines.append(json.dumps({k:v for k,v in e.items() if k!='facts'},ensure_ascii=False))
                lines.append('FACTS '+json.dumps(e['facts'],ensure_ascii=False))
        elif c['tool']!='submit_response':
            lines.append(json.dumps(c.get('visible_result'),ensure_ascii=False))
        lines.append('')
    (OUT/f"{case['id']}.md").write_text('\n'.join(lines))
(OUT/'decoded.json').write_text(json.dumps(cases,ensure_ascii=False,indent=2))
for c in cases:
    print('\n'+c['id'], 'prompt', [r['usage']['prompt_tokens'] for r in c['rounds']])
    for call in c['calls']:
        if call['tool']!='wiki': continue
        print('R'+str(call['round']),call['arguments'],call['status'],call['match_count'],call['bytes'])
        for e in call['entries']:
            print(' ',e['key'],e['match'],'facts',len(e['facts']),'not_read',e['not_read'],
                  'missing',e['missing_fields'],'directory',len(e.get('directory') or []))
