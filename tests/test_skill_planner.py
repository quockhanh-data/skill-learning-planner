from __future__ import annotations

import json
import unittest

import skill_planner


class SkillPlannerTests(unittest.TestCase):
    def test_infers_data_domain(self) -> None:
        self.assertEqual(skill_planner.infer_domain("data visualization with Power BI"), "data")

    def test_build_plan_has_expected_weeks(self) -> None:
        plan = skill_planner.build_plan("Flutter app development", weeks=5, hours_per_week=6)
        self.assertEqual(plan.domain, "coding")
        self.assertEqual(len(plan.weeks_plan), 5)
        self.assertTrue(plan.milestones)

    def test_markdown_and_json_outputs(self) -> None:
        plan = skill_planner.build_plan("SQL for analytics", weeks=3, hours_per_week=4)
        markdown = skill_planner.render_markdown(plan)
        payload = json.dumps(plan.to_dict(), ensure_ascii=False)
        self.assertIn("Roadmap", markdown)
        self.assertIn("SQL for analytics", payload)


if __name__ == "__main__":
    unittest.main()
