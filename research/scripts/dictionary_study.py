"""Presentation-only follow-up over the exact same fixed visible evidence."""
import argparse
import asyncio
import copy
import hashlib
from pathlib import Path
import tomllib

from product import module
from runner import Budget
from . import breakthrough as experiment
from .evidence_dictionary import encode, decode, GUIDANCE


def hashes():
    return {**experiment.source_hashes(), **{
        str(p.resolve()): hashlib.sha256(p.read_bytes()).hexdigest()
        for p in (Path(__file__), Path(__file__).with_name("evidence_dictionary.py"))}}


def prepare(source, out):
    out.mkdir(parents=True, exist_ok=False)
    original = experiment.read(source / "manifest.json")
    cases = []
    for case in original["cases"]:
        path = source / "packs" / f'{case["id"]}.json.gz'
        if hashlib.sha256(path.read_bytes()).hexdigest() != case["pack_sha256"]:
            raise ValueError("Source pack changed")
        pack = experiment.read(path)
        packed = encode(pack["evidence"])
        if decode(packed) != pack["evidence"]:
            raise ValueError("Lossless check failed")
        pack["evidence"] = packed
        pack["original_evidence_sha256"] = pack["evidence_sha256"]
        pack["evidence_sha256"] = hashlib.sha256(experiment.canonical(packed).encode()).hexdigest()
        target = out / "packs" / path.name
        experiment.save(target, pack)
        cases.append({"id": pack["id"], "pack_sha256": hashlib.sha256(target.read_bytes()).hexdigest(),
                      "source": str(path.resolve()), "source_sha256": case["pack_sha256"],
                      "original_evidence_sha256": pack["original_evidence_sha256"]})
    experiment.save(out / "manifest.json", {"kind": "lossless_dictionary_fixed_evidence", "sources": hashes(),
        "cases": cases, "repeats": 2, "concurrency": 4, "max_attempts": 32, "token_ceiling": 3_000_000,
        "settings": original["settings"], "claim_guard": original["claim_guard"],
        "baseline": str((source / "manifest.json").resolve()), "guidance": GUIDANCE,
        "method": "Same current short-answer contract and model. Only evidence dictionary encoding plus its decoding instruction changes. No new facts, no independent reviewer call. Conducted after baseline, not interleaved. Diagnostic only; not autonomous."})


async def run(out, config):
    manifest = experiment.read(out / "manifest.json")
    if manifest["sources"] != hashes():
        raise ValueError("Sealed source changed")
    cfg = tomllib.loads(config.read_text())
    settings = module("agent.model_client").build_agent_model_settings(**cfg)
    for name in ("base_url", "model", "max_output_tokens"):
        if getattr(settings, name) != manifest["settings"][name]:
            raise ValueError("Unexpected model configuration")
    for case in manifest["cases"]:
        pack = out / "packs" / f'{case["id"]}.json.gz'
        if hashlib.sha256(pack.read_bytes()).hexdigest() != case["pack_sha256"]:
            raise ValueError("Evidence pack changed")
        source = Path(case["source"])
        if hashlib.sha256(source.read_bytes()).hexdigest() != case["source_sha256"]:
            raise ValueError("Original evidence changed")
        if decode(experiment.read(pack)["evidence"]) != experiment.read(source)["evidence"]:
            raise ValueError("Evidence no longer lossless")
    # Prompt-only experimental seam; stage's tool/runtime/contract is unchanged.
    experiment.DIAGNOSTIC += GUIDANCE
    semaphore = asyncio.Semaphore(4)
    budget = Budget(max_attempts=32, token_ceiling=3_000_000)

    async def one(case, repeat):
        async with semaphore:
            pack = experiment.read(out / "packs" / f'{case["id"]}.json.gz')
            return await experiment.stage(pack, "current", repeat, out, settings, budget)

    try:
        results = await asyncio.gather(*(one(case, repeat) for repeat in range(2) for case in manifest["cases"]), return_exceptions=True)
        experiment.save(out / "run-outcome.json", {"worker_errors": [type(r).__name__ for r in results if isinstance(r, BaseException)]})
    finally:
        experiment.save(out / "budget.json", {"attempts": budget.attempts, "reported_or_reserved_tokens": budget.charged})


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=("prepare", "run"))
    parser.add_argument("--source", type=Path)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--config", type=Path, default=Path("/dev/shm/neko-programmatic/live.toml"))
    args = parser.parse_args()
    if args.action == "prepare":
        prepare(args.source, args.out)
    else:
        asyncio.run(run(args.out, args.config))
