from __future__ import annotations

import unittest

from scripts import verify_job_stack_smoke as smoke


class VerifyJobStackSmokeTests(unittest.TestCase):
    def test_verify_job_stack_passes_locally(self) -> None:
        issues = smoke.verify_job_stack(exercise_http=False)
        self.assertEqual(issues, [])

    def test_main_exits_zero_on_success(self) -> None:
        self.assertEqual(smoke.main([]), 0)


if __name__ == "__main__":
    unittest.main()
