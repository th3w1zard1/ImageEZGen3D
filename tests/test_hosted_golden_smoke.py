from __future__ import annotations

import importlib.util
import io
import json
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

from imageezgen3d.hosted_golden_smoke import (
    HostedGoldenSmokeResult,
    parse_run_id,
    run_hosted_golden_smoke,
    validate_backend_rail_html,
    validate_g7_not_false_neural_claim,
    validate_hosted_generate_status,
    write_hosted_golden_record,
)
from imageezgen3d.manifest_ui import backend_rail_chips_html


def _valid_status(run_id: str = "20260524-184255-f0ce0436") -> str:
    return "\n".join(
        [
            f"Run `{run_id}` complete.",
            "- **Export budget:** up to 25,000 faces (quality-tier preset)",
            "- **Backend used:** Local CPU Preview",
            "- **Fallback:** ZeroGPU adapter is not enabled yet.",
            "- **Preview disclaimer:** CPU preview fallback is active.",
            "Downloads: manifest, glb, obj",
        ]
    )


class HostedGoldenSmokeTests(unittest.TestCase):
    def test_parse_run_id(self) -> None:
        self.assertEqual(
            parse_run_id("Done. Run `20260524-184255-f0ce0436`."),
            "20260524-184255-f0ce0436",
        )
        self.assertIsNone(parse_run_id("no run id here"))

    def test_validate_hosted_generate_status_accepts_golden_markdown(self) -> None:
        ok, issues, run_id = validate_hosted_generate_status(_valid_status())
        self.assertTrue(ok, issues)
        self.assertEqual(run_id, "20260524-184255-f0ce0436")

    def test_validate_hosted_generate_status_rejects_missing_export_budget(self) -> None:
        status = _valid_status().replace("Export budget", "Quality tier")
        ok, issues, _ = validate_hosted_generate_status(status)
        self.assertFalse(ok)
        self.assertTrue(any("Export budget" in issue for issue in issues))

    def test_validate_backend_rail_html_accepts_chip_section(self) -> None:
        html = backend_rail_chips_html(
            adapter_key="cpu-demo",
            fallback_reason="ZeroGPU adapter not enabled",
        )
        self.assertEqual(validate_backend_rail_html(html), [])

    def test_validate_backend_rail_html_rejects_missing_marker(self) -> None:
        issues = validate_backend_rail_html("<p>overview only</p>")
        self.assertTrue(any("What backend ran" in issue for issue in issues))

    def test_validate_g7_not_false_neural_claim_accepts_cpu_fallback(self) -> None:
        self.assertEqual(validate_g7_not_false_neural_claim(_valid_status()), [])

    def test_validate_g7_not_false_neural_claim_rejects_neural_markers(self) -> None:
        neural_status = "\n".join(
            [
                "Run `20260527-120000-abcdef01` complete.",
                "- **Export budget:** up to 25,000 faces",
                "- **Backend used:** Hosted ZeroGPU (hunyuan-zerogpu)",
                "Downloads: manifest, glb, obj",
            ]
        )
        issues = validate_g7_not_false_neural_claim(neural_status)
        self.assertEqual(len(issues), 1)
        self.assertIn("G7 neural", issues[0])

    def test_write_hosted_golden_record_persists_json(self) -> None:
        result = HostedGoldenSmokeResult(
            ok=True,
            run_id="20260524-000000-00000000",
            space_url="https://example.hf.space/",
            adapter_hint="cpu-demo",
            quality="draft",
            issues=(),
            g7_false_neural_guard_ok=True,
        )
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "hosted-golden.json"
            write_hosted_golden_record(path, result)
            payload = json.loads(path.read_text(encoding="utf-8"))
            self.assertTrue(payload["ok"])
            self.assertEqual(payload["adapter_hint"], "cpu-demo")
            self.assertTrue(payload["g7_false_neural_guard_ok"])

    @patch("gradio_client.Client")
    def test_run_hosted_golden_smoke_validates_predict_output(
        self, client_cls: object,
    ) -> None:
        client = client_cls.return_value
        rail_html = backend_rail_chips_html(adapter_key="cpu-demo")
        predict_outputs: list[object | None] = [None] * 16
        predict_outputs[1] = _valid_status()
        predict_outputs[15] = rail_html
        client.predict.return_value = tuple(predict_outputs)

        with tempfile.TemporaryDirectory() as directory:
            sample = Path(directory) / "block.png"
            sample.write_bytes(b"png")
            result = run_hosted_golden_smoke(
                space_url="https://test.hf.space/",
                sample_path=sample,
            )

        self.assertTrue(result.ok, result.issues)
        self.assertEqual(result.run_id, "20260524-184255-f0ce0436")
        self.assertEqual(result.adapter_hint, "Local CPU Preview")
        self.assertTrue(result.g7_false_neural_guard_ok)

    @patch("gradio_client.Client")
    def test_run_hosted_golden_smoke_rejects_false_g7_neural_status(
        self, client_cls: object,
    ) -> None:
        client = client_cls.return_value
        neural_status = "\n".join(
            [
                "Run `20260527-120000-abcdef01` complete.",
                "- **Export budget:** up to 25,000 faces",
                "- **Backend used:** Hosted ZeroGPU (hunyuan-zerogpu)",
                "Downloads: manifest, glb, obj",
            ]
        )
        predict_outputs: list[object | None] = [None] * 16
        predict_outputs[1] = neural_status
        client.predict.return_value = tuple(predict_outputs)

        with tempfile.TemporaryDirectory() as directory:
            sample = Path(directory) / "block.png"
            sample.write_bytes(b"png")
            result = run_hosted_golden_smoke(
                space_url="https://test.hf.space/",
                sample_path=sample,
            )

        self.assertFalse(result.ok)
        self.assertFalse(result.g7_false_neural_guard_ok)
        self.assertTrue(
            any("G7 neural" in issue for issue in result.issues),
            result.issues,
        )

    @patch("gradio_client.Client")
    def test_hosted_golden_smoke_cli_json_includes_g7_guard_field(
        self, client_cls: object,
    ) -> None:
        client = client_cls.return_value
        rail_html = backend_rail_chips_html(adapter_key="cpu-demo")
        predict_outputs: list[object | None] = [None] * 16
        predict_outputs[1] = _valid_status()
        predict_outputs[15] = rail_html
        client.predict.return_value = tuple(predict_outputs)

        repo_root = Path(__file__).resolve().parents[1]
        script_path = repo_root / "scripts" / "hosted_golden_smoke.py"
        spec = importlib.util.spec_from_file_location(
            "hosted_golden_smoke_cli", script_path,
        )
        assert spec is not None and spec.loader is not None
        cli_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cli_module)

        with tempfile.TemporaryDirectory() as directory:
            sample = Path(directory) / "block.png"
            sample.write_bytes(b"png")
            stdout = io.StringIO()
            with redirect_stdout(stdout):
                exit_code = cli_module.main(
                    [
                        "--json",
                        "--space-url",
                        "https://test.hf.space/",
                        "--sample",
                        str(sample),
                    ],
                )
        self.assertEqual(exit_code, 0)
        payload = json.loads(stdout.getvalue())
        self.assertTrue(payload["g7_false_neural_guard_ok"])


if __name__ == "__main__":
    unittest.main()
