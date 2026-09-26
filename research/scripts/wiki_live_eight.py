"""Eight finite live Wiki consultations using the production runner; no outer retries."""
import argparse
import asyncio
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tomllib

ROOT = Path(__file__).resolve().parent
WORK = ROOT.parent
QUESTIONS = [
    ("wort-natural", "制作麦芽汁需要多少工作量、消耗什么、产出多少？影响制作速度的属性叫什么？请查定义并给出依据。", ["Verse.RecipeDef/Make_Wort", "RimWorld.StatDef/DrugCookingSpeed"]),
    ("medicine-stack", "普通工业医药（不是草药或闪耀世界医药）的定义堆叠上限是多少？这能说明我现在有多少药吗？", ["Verse.ThingDef/MedicineIndustrial"]),
    ("rice-growth", "水稻定义里的基础生长天数和收获产量分别是多少？基础生长天数能直接当成当前地图实际成熟时间吗？", ["Verse.ThingDef/Plant_Rice"]),
    ("kind-modifier", "善良特性在定义中有哪些数值修正？请列出对应属性的中文名、修正值以及是倍率还是加值，不要推断某个小人的最终数值。", ["RimWorld.TraitDef/Kind", "RimWorld.StatDef/CertaintyLossFactor"]),
    ("smithing-boundary", "锻造研究的基础成本和前置研究是什么？仅凭这些定义能否断言当前殖民地已完成锻造？", ["Verse.ResearchProjectDef/Smithing"]),
    ("invalid-key", "请核验 Verse.RecipeDef/BrewWort 这个完整定义键是否存在。若不存在就明确说不存在，不要替换成别的定义。", []),
    ("null-vs-missing", "请读取 Verse.RecipeDef/Make_Wort 的 products[0].count、recipeUsers 和 nekoMissingProbe 字段。分别报告实际值或缺失状态，不要把 null 与字段缺失混为一谈。", ["Verse.RecipeDef/Make_Wort"]),
    ("brewery-direction", "酿造台的定义是否列出了制作麦芽汁的配方？这条关系本身足以证明制作麦芽汁只能在酿造台进行吗？请引用实际定义并说明判断边界。", ["Verse.ThingDef/Brewery", "Verse.RecipeDef/Make_Wort"]),
]


def digest(p):
    h = hashlib.sha256()
    with Path(p).open('rb') as f:
        for b in iter(lambda: f.read(1024 * 1024), b''): h.update(b)
    return h.hexdigest()


def save(p, data):
    with Path(p).open('x') as f: json.dump(data, f, ensure_ascii=False, indent=2)


async def worker(args):
    from product import module
    from runner import run_episode
    from surface_study import PersistentBudget
    from scorers import measurements
    manifest = json.loads((args.out / 'manifest.json').read_text())
    for rel, expected in manifest['sealed_hashes'].items():
        if digest(args.out / rel) != expected: raise ValueError('Sealed input changed: ' + rel)
    cfg = tomllib.loads(args.config.read_text())['neko_rimworld']['agent']
    settings = module('agent.model_client').build_agent_model_settings(**cfg)
    public = settings.public_dict(); public.pop('base_url', None)
    if public != manifest['settings']: raise ValueError('Settings changed')
    case = manifest['cases'][args.case]
    target = args.out / f"{args.case+1:02d}-{case['id']}"
    save(target.with_suffix('.started.json'), {'id':case['id'], 'mode':args.mode})
    def event(data):
        if data.get('event') == 'model_attempt_started':
            names = {t['function']['name'] for t in data['input']['tools']}
            expected = {'look', 'count', 'wiki', 'submit_response'}
            if names != expected and names != {'submit_response'}:
                raise RuntimeError(f'Pre-dispatch tool surface mismatch: {sorted(names)}')
            if data['attempt'] == 1 and names != expected:
                raise RuntimeError('First request must expose the full production surface')
        with target.with_suffix('.events.jsonl').open('a') as f:
            f.write(json.dumps(data, ensure_ascii=False) + '\n'); f.flush(); os.fsync(f.fileno())
    if args.mode != manifest['mode']:
        raise ValueError('Mode differs from sealed manifest')
    def production_interaction(setup, session, update):
        interaction = module('agent.semantic_tools').semantic_interaction_factory(setup, session, update)
        if interaction is None:
            raise RuntimeError('Production semantic surface unavailable; no model dispatch allowed')
        return interaction
    budget = PersistentBudget(args.out / 'budget.json', 1_500_000, 96)
    evidence = await run_episode(case['question'], args.out/'world.json', settings=settings,
        budget=budget, mode=args.mode, on_event=event, max_attempts_per_episode=12,
        query_dll=args.out/'query/FrozenWorld.dll', knowledge_snapshot=args.out/'knowledge/ready.json',
        interaction_factory_override=production_interaction)
    initial_tools = evidence['requests'][0]['input']['tools']
    tool_names = {tool['function']['name'] for tool in initial_tools}
    expected_tools = {'look', 'count', 'wiki', 'submit_response'}
    if not expected_tools.issubset(tool_names) or {'query', 'get_game_info', 'query_game'} & tool_names:
        raise RuntimeError(f'production semantic tool surface drift: {sorted(tool_names)}')
    save(target.with_suffix('.json'), {'case':case, 'evidence':evidence, 'measurements':measurements(evidence)})
    print(json.dumps({'case':case['id'], 'status':evidence['result'].get('status'),
                      'requests':len(evidence['requests']), 'tokens':measurements(evidence)['known_total_tokens']}), flush=True)


def prepare(args):
    from product import PLUGIN, module
    args.out.mkdir(parents=True, exist_ok=False)
    cfg = tomllib.loads(args.config.read_text())['neko_rimworld']['agent']
    settings = module('agent.model_client').build_agent_model_settings(**cfg)
    public = settings.public_dict(); public.pop('base_url', None)
    for p in PLUGIN.rglob('*.py'):
        rel=p.relative_to(PLUGIN)
        if any(x in rel.parts for x in ('vendor', '__pycache__', 'tests', 'evaluations', '.venv')): continue
        target=args.out/'plugin'/rel;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,target)
    for name in ('wiki_live_eight.py','runner.py','world.py','product.py','scorers.py','surface_study.py','compare_models.py'):
        target=args.out/'executor'/name;target.parent.mkdir(exist_ok=True);shutil.copyfile(ROOT/name,target)
    query=ROOT/'frozen-world/bin/Debug/net8.0'
    (args.out/'query').mkdir()
    for p in query.iterdir():
        if p.is_file() and (p.suffix in {'.dll','.pdb'} or p.name.endswith(('.deps.json','.runtimeconfig.json')) or p.name=='native-enums.json'): shutil.copyfile(p,args.out/'query'/p.name)
    world=WORK/'.bench-data/v14-final-world/RimWorldBench/resources-20260912-054348-44cf8b3cfd7b408fb936e9eb418a1542.json'
    shutil.copyfile(world,args.out/'world.json')
    source=WORK/'.bench-data/def-knowledge-indexed-20260921-225331/knowledge'
    index=json.loads((source/'ready.json').read_text()); (args.out/'knowledge').mkdir()
    for name in ('ready.json',index['data_file']): shutil.copyfile(source/name,args.out/'knowledge'/name)
    view=module('knowledge').IndexedKnowledgeView(args.out/'knowledge')
    references={k:view.read_entry(k) for _,_,keys in QUESTIONS for k in keys}
    assert all(references.values())
    save(args.out/'references.json',references)
    hashes={str(p.relative_to(args.out)):digest(p) for p in args.out.rglob('*') if p.is_file()}
    save(args.out/'manifest.json', {'cases':[{'id':i,'question':q,'reference_keys':keys} for i,q,keys in QUESTIONS],
        'settings':public,'sealed_hashes':hashes,'mode':args.mode,'repeats':1,'arms':['current'],
        'world_source':str(world),'world_origin':'real game capture; frozen replay, not live bridge',
        'knowledge_source':str(source),'knowledge_payload_sha256':index['data_sha256'],
        'budget':{'max_attempts':96,'token_ceiling':1500000,'per_episode_attempts':12},
        'required_tool_surface':['look','count','wiki','submit_response'],
        'limits':['8 purposive cases, not general accuracy','two explicit technical queries','no paired baseline',
                  'Def and world captures differ in date/configuration; applicability unverified',
                  'references are review-only and never added to model context'],
        'outer_retries':0})
    print('Prepared '+str(args.out),flush=True)


def run(args):
    manifest=json.loads((args.out/'manifest.json').read_text());rows=[]
    for i,c in enumerate(manifest['cases']):
        env=os.environ.copy();env['RIMWORLD_PLUGIN_SOURCE']=str(args.out/'plugin')
        env['NEKO_SEMANTIC_SURFACE']='1'
        command=[sys.executable,str(args.out/'executor/wiki_live_eight.py'),'worker','--out',str(args.out),
                 '--config',str(args.config),'--mode',args.mode,'--case',str(i)]
        try: code=subprocess.run(command,env=env,timeout=150).returncode
        except subprocess.TimeoutExpired: code=-1
        rows.append({'id':c['id'],'exit_code':code})
        print(json.dumps(rows[-1]),flush=True)
    save(args.out/'dispatch.json',{'planned':8,'attempted_sessions':len(rows),'rows':rows})


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('action',choices=['prepare','run','worker']);p.add_argument('--out',type=Path,required=True)
    p.add_argument('--config',type=Path,required=True);p.add_argument('--mode',choices=['mock','live'],default='mock');p.add_argument('--case',type=int)
    a=p.parse_args();a.out=a.out.resolve();a.config=a.config.resolve()
    if a.action=='worker': asyncio.run(worker(a))
    elif a.action=='prepare': prepare(a)
    else: run(a)
