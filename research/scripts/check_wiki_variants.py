"""Read-only deterministic boundary probes for frozen Wiki experiment sources.

Run once per arm with RIMWORLD_PLUGIN_SOURCE. Results report failures rather than
changing sealed code or accepting the candidate behavior as the expected answer.
"""
import json
import tempfile
from pathlib import Path
from product import module, PLUGIN

wiki = module('agent.wiki_tools')


def entry(name, label, facts):
    return dict(key='Verse.ThingDef/'+name, type='Verse.ThingDef', def_name=name,
                label=label, description='', source_mod='Core', package_id='ludeon.rimworld',
                facts=[dict(name=n, value=v) for n,v in facts], related=[], truncated=False)


def query(entries, text):
    with tempfile.TemporaryDirectory() as tmp:
        path=Path(tmp)
        (path/'current.json').write_text(json.dumps(dict(format='neko.defs.v1', game_version='1.6',
            language='test', generated_at='2026-09-22', complete=True, issues=[], mods=[], entries=entries),ensure_ascii=False))
        return wiki.WikiStore(path).query(text)


checks=[]
def record(name, result, passed):
    checks.append(dict(name=name, passed=bool(passed), result=result))


r=query([entry('Alpha','shared',[('data.growDays','3')]), entry('Beta','shared',[('data.speed','6')])], 'shared growDays')
record('duplicate_name_not_resolved_by_field_availability',r,
       r['status']=='ambiguous' and len(r['entries'])==2)
r=query([entry('Alpha','alpha',[('first.value','1'),('second.value','2')])], 'alpha value')
record('duplicate_leaf_not_guessed',r,
       all(e.get('match')!='unique_object_and_fields' for e in r['entries']))
r=query([entry('Alpha','alpha',[('data.value','1')])], 'Verse.ThingDef/Missing value')
record('invalid_full_key_no_fallback',r,r['status']=='not_found' and not r['entries'])
r=query([entry('Alpha','alpha',[('data.value','null')])], 'Verse.ThingDef/Alpha data.value')
e=r['entries'][0]
record('null_preserved',r,any(f['name']=='data.value' and f['value']=='null' for f in e['facts']))
r=query([entry('Alpha','alpha',[('data.value','1')])], 'Verse.ThingDef/Alpha data.absent')
record('missing_preserved',r,r['entries'][0]['missing_fields']==['data.absent'])
r=query([entry('Alpha','alpha',[('data.value','1')])], 'Verse.ThingDef/Alpha data.value')
e=r['entries'][0]
record('empty_optional_lists_not_claimed_truncated',r,
       not e['related_truncated'] and not r['snapshot']['mods_truncated'])

observations=[]
for label in ['水稻','麦芽汁','制作麦芽汁']:
    r=query([entry('Example',label,[('plant.growDays','3')])], label+' growDays')
    observations.append(dict(query=label+' growDays', result=r))
print(json.dumps(dict(source=str(PLUGIN),checks=checks,observations=observations),ensure_ascii=False,indent=2))
