"""Explicit model/effort diagnostic, separate from tool architecture scores."""
import argparse
import asyncio
from contextvars import ContextVar
import hashlib
import json
from pathlib import Path
import tomllib

import httpx

from product import module
from runner import Budget
from . import breakthrough as experiment

SLOT = ContextVar("model_probe_slot")
EFFORT = "low"
MODELS = {"flash_low": "deepseek-flash", "pro_low": "deepseek-v4-pro"}


def source_hashes():
    return {**experiment.source_hashes(), str(Path(__file__).resolve()): hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}


class EffortTransport(httpx.AsyncHTTPTransport):
    async def handle_async_request(self, request):
        body = json.loads(request.content)
        body["reasoning_effort"] = EFFORT
        public = module("agent.audit").private_protocol_redacted(body)
        directory = SLOT.get() / "wire"
        number = len(list(directory.glob("*.json.gz"))) + 1
        experiment.save(directory / f"{number:02d}.json.gz", {
            "body": public, "body_sha256": hashlib.sha256(experiment.canonical(body).encode()).hexdigest(),
            "representation": "private_protocol_redacted; authorization header is never recorded"})
        forwarded = httpx.Request(request.method, request.url,
            headers={k: v for k, v in request.headers.items() if k.lower() != "content-length"},
            json=body, extensions=request.extensions)
        return await super().handle_async_request(forwarded)


def prepare(source, out):
    out.mkdir(parents=True, exist_ok=False)
    original = experiment.read(source / "manifest.json")
    cases = original["cases"]
    for case in cases:
        path = source / "packs" / f'{case["id"]}.json.gz'
        if hashlib.sha256(path.read_bytes()).hexdigest() != case["pack_sha256"]:
            raise ValueError("Original evidence changed")
    experiment.save(out / "manifest.json", {"kind": "model_effort_fixed_evidence", "sources": source_hashes(),
        "source": str(source.resolve()), "cases": cases, "models": MODELS, "effort": EFFORT,
        "repeats": 2, "concurrency": 4, "token_ceiling": 5_000_000,
        "stage_seconds": 90, "max_output_tokens": 32768,
        "method": "Exact original visible facts, current length/structure contract, no semantic claim guard or game reads. Compare model/effort configurations, not isolated model or tool architecture effects. No retry of failed slots.",
        "docs": "https://api-docs.deepseek.com/guides/thinking_mode/"})


async def run(out, config):
    manifest = experiment.read(out / "manifest.json")
    if manifest["sources"] != source_hashes():
        raise ValueError("Source changed")
    source = Path(manifest["source"])
    for case in manifest["cases"]:
        path = source / "packs" / f'{case["id"]}.json.gz'
        if hashlib.sha256(path.read_bytes()).hexdigest() != case["pack_sha256"]:
            raise ValueError("Evidence changed")
    cfg = tomllib.loads(config.read_text())
    clients = module("agent.model_client")
    actual = clients.OpenAICompatibleModelClient
    clients.OpenAICompatibleModelClient = lambda settings, **kwargs: actual(settings, transport=EffortTransport(), **kwargs)
    budget = Budget(max_attempts=64, token_ceiling=5_000_000)
    sem = asyncio.Semaphore(4)

    async def one(case, repeat, arm):
        async with sem:
            pack = experiment.read(source / "packs" / f'{case["id"]}.json.gz')
            settings = clients.build_agent_model_settings(**{**cfg, "model": MODELS[arm]})
            directory = out / arm
            token = SLOT.set(directory / "requests" / f'{case["id"]}-{repeat}')
            try:
                return await experiment.stage(pack, "current", repeat, directory, settings, budget)
            finally:
                SLOT.reset(token)

    try:
        results = await asyncio.gather(*(one(case, repeat, arm)
            for repeat in range(2) for case in manifest["cases"] for arm in MODELS), return_exceptions=True)
        experiment.save(out / "run-outcome.json", {"worker_errors": [type(r).__name__ for r in results if isinstance(r, BaseException)]})
    finally:
        clients.OpenAICompatibleModelClient = actual
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
