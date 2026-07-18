from __future__ import annotations

import argparse
from pathlib import Path


PHASES = [
    "Understand the basics and vocabulary",
    "Practice core techniques with small exercises",
    "Apply the skill to a realistic mini project",
    "Review mistakes and improve workflow",
    "Create a portfolio-ready output",
]


def weekly_focus(week: int, total_weeks: int) -> str:
    if total_weeks <= 1:
        return PHASES[-1]
    index = round((week - 1) * (len(PHASES) - 1) / (total_weeks - 1))
    return PHASES[index]


def make_plan(skill: str, weeks: int, hours: int) -> str:
    weekly_hours = max(hours, 1)
    practice_hours = max(round(weekly_hours * 0.55), 1)
    theory_hours = max(round(weekly_hours * 0.25), 1)
    review_hours = max(weekly_hours - practice_hours - theory_hours, 1)

    lines = [
        f"# Learning Plan: {skill}",
        "",
        "## Goal",
        "",
        f"Build practical confidence in **{skill}** over {weeks} weeks with about {weekly_hours} hours per week.",
        "",
        "## Weekly Rhythm",
        "",
        f"- Theory: {theory_hours} hour(s)",
        f"- Practice: {practice_hours} hour(s)",
        f"- Review and notes: {review_hours} hour(s)",
        "",
        "## Roadmap",
        "",
    ]

    for week in range(1, weeks + 1):
        focus = weekly_focus(week, weeks)
        lines.extend(
            [
                f"### Week {week}: {focus}",
                "",
                f"- Learn: one focused concept in {skill}.",
                f"- Practice: complete 2-3 small exercises related to {skill}.",
                "- Review: write short notes about what was confusing and how it was solved.",
                "- Evidence: save one screenshot, notebook, report, or short demo.",
                "",
            ]
        )

    lines.extend(
        [
            "## Final Checkpoint",
            "",
            "- Explain the skill in simple words.",
            "- Complete one small project without following a full tutorial.",
            "- Document the result in a README or short report.",
            "- List what to learn next.",
            "",
            "## Reflection Template",
            "",
            "- What did I learn?",
            "- What was difficult?",
            "- What can I now build or explain?",
            "- What should I practice next week?",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate a practical weekly learning plan for a skill.")
    parser.add_argument("skill", help="Skill to learn, for example: data visualization.")
    parser.add_argument("--weeks", "-w", type=int, default=4, help="Number of weeks.")
    parser.add_argument("--hours", "-hr", type=int, default=5, help="Hours per week.")
    parser.add_argument("--output", "-o", help="Write the plan to a Markdown file.")
    args = parser.parse_args()

    if args.weeks < 1:
        raise SystemExit("--weeks must be at least 1.")
    if args.hours < 1:
        raise SystemExit("--hours must be at least 1.")

    plan = make_plan(args.skill, args.weeks, args.hours)
    if args.output:
        Path(args.output).write_text(plan, encoding="utf-8")
        print(f"Learning plan written to {args.output}")
    else:
        print(plan)


if __name__ == "__main__":
    main()
