"""Offline regression evidence from retained Wort tool calls; no model dispatch."""
from __future__ import annotations

import hashlib
import json
import resource
import time
from pathlib import Path

from product import module


def main():
    root = Path(__file__).resolve().parent.parent
    source = root / ".bench-data/def-knowledge-indexed-20260921-225331/knowledge"
    calls_path = root / ".bench-results/wiki-live-pilot-20260921/review/wort-context/candidate-calls-decoded.json"
    output = root / ".bench-results/wiki-structure-offline-20260922"
    output.mkdir(parents=True, exist_ok=True)
    knowledge, wiki = module("knowledge"), module("agent.wiki_tools")
    measurements = []
    for _ in range(5):
        start = time.perf_counter()
        library = knowledge.KnowledgeLibrary(source, allow_legacy_import=False)
        view = library.open_view()
        assert view is not None
        attached = time.perf_counter()
        store = wiki.WikiStore(view)
        store.query("Verse.RecipeDef/Make_Wort products[0].count recipeUsers")
        queried = time.perf_counter()
        measurements.append({"attach_ms": (attached - start) * 1000,
                             "first_exact_read_ms": (queried - attached) * 1000})
    replay = []
    for call in json.loads(calls_path.read_text()):
        if call["tool"] != "wiki":
            continue
        start = time.perf_counter()
        result = store.query(call["arguments"]["query"])
        elapsed = (time.perf_counter() - start) * 1000
        size = len(json.dumps(result, ensure_ascii=False).encode())
        assert size <= 8192
        replay.append({"round": call["round"], "query": call["arguments"]["query"],
                       "ms": elapsed, "bytes": size, "result": result})
    assert len(replay) == 20
    exact = store.query("Verse.RecipeDef/Make_Wort products[0].count recipeUsers workAmount workSpeedStat")
    facts = {f["name"]: f for f in exact["entries"][0]["facts"]}
    assert facts["products[0].count"]["value"] == "5"
    assert facts["products[0].thingDef"]["label"] == "麦芽汁"
    assert facts["recipeUsers"]["type"] == "null"
    assert facts["workAmount"]["value"] == "1000"
    assert facts["workSpeedStat"]["label"] == "酿酒速度"
    assert exact["entries"][0]["read_complete"]
    assert "Verse.RecipeDef/Make_Wort" in {e["key"] for e in replay[0]["result"]["entries"]}
    files = [Path(wiki.__file__), Path(module("agent.wiki_records").__file__), Path(knowledge.__file__), Path(__file__)]
    report = {"mode": "offline_fixed_query_replay_not_model_retest", "model_requests": 0,
              "historical_calls_sha256": hashlib.sha256(calls_path.read_bytes()).hexdigest(),
              "source_sha256": view.metadata["sha256"],
              "code_sha256": {str(p.relative_to(root)): hashlib.sha256(p.read_bytes()).hexdigest() for p in files},
              "measurements": measurements, "peak_rss_kib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
              "warm_cache_possible": True, "calls": replay, "combined_exact_read": exact}
    (output / "replay.json").write_text(json.dumps(report, ensure_ascii=False, indent=2))
    summary = {"queries_replayed": len(replay), "model_requests": 0,
               "measurements": measurements, "peak_rss_kib": report["peak_rss_kib"],
               "queries": [{k: row[k] for k in ("round", "query", "ms", "bytes")} |
                           {"status": row["result"]["status"], "keys": [e["key"] for e in row["result"]["entries"]]}
                           for row in replay]}
    (output / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2))
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
