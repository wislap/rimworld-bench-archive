import asyncio
import json

from product import module
from programmatic.breakthrough import report_tool, submitted_text, stage, read
from runner import Budget


def execute(spec, arguments):
    registry = module("agent.tools").ToolRegistry()
    registry.register(spec)
    call = module("agent.contracts").ToolCall("test", "submit_response", json.dumps(arguments))
    return asyncio.run(registry.execute(registry.prepare(call)))


def test_report_contract_preserves_long_text_exactly():
    text = "这是完整的有条件分析，不应因为交接长度而被改写。" * 60
    result = execute(report_tool(), {"report": text})
    assert result.ok
    assert result.value["data"]["full_text"] == text
    assert module("agent.handoff").count_handoff_tokens(text)[0] > 180


def test_report_missing_or_oversized_is_explicit_validation_error():
    for value in (None, "x" * 12001):
        result = execute(report_tool(), {"report": value})
        assert not result.ok
        assert result.value["error"]["code"] in {"invalid_submission", "submission_too_large"}


def test_current_contract_still_rejects_same_long_text():
    handoff = module("agent.handoff")
    text = "这是完整的有条件分析，不应因为交接长度而被改写。" * 60
    result = execute(handoff.make_submission_tool(handoff.SubmissionDraft(), [], references_supported=False), {"answer": text})
    assert not result.ok
    assert result.value["error"]["code"] == "handoff_over_budget"


def test_first_draft_capture_includes_legacy_text_parts():
    assert submitted_text({"answer": [{"text": "结论"}], "detail": "依据"}) == "结论\n\n依据"


def test_budget_rejection_persists_terminal_record_without_network(tmp_path):
    settings = module("agent.model_client").build_agent_model_settings(base_url="http://localhost/v1", model="mock")
    pack = {"id": "example", "question": "test", "evidence": [], "evidence_sha256": "test"}
    result = asyncio.run(stage(pack, "report", 0, tmp_path, settings, Budget(max_attempts=0)))
    assert result["status"] == "model_error"
    assert result["requests"][0]["error_code"] == "benchmark_budget"
    assert not result["requests"][0].get("dispatched")
    assert read(tmp_path / "runs/example-report-0.json.gz") == result
