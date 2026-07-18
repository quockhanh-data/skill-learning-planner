from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass
from pathlib import Path


DOMAIN_KEYWORDS = {
    "data": {"data", "sql", "analytics", "visualization", "statistics", "excel", "power bi", "tableau", "python"},
    "coding": {"code", "coding", "programming", "web", "flutter", "react", "api", "backend", "frontend"},
    "writing": {"writing", "essay", "report", "blog", "research", "copywriting"},
    "language": {"english", "ielts", "toeic", "speaking", "vocabulary", "grammar", "japanese", "korean"},
    "design": {"design", "ui", "ux", "figma", "visual", "presentation"},
}

DOMAIN_PLAYBOOK = {
    "data": {
        "learn": "Study one concept, method, or chart type with notes.",
        "practice": "Analyze a small dataset and explain one insight.",
        "evidence": "Notebook, dashboard screenshot, SQL query, or short analysis report.",
    },
    "coding": {
        "learn": "Read documentation and build one small feature from scratch.",
        "practice": "Implement, run, debug, and refactor a focused exercise.",
        "evidence": "GitHub commit, demo screenshot, README note, or working CLI/app.",
    },
    "writing": {
        "learn": "Study one structure, argument pattern, or example piece.",
        "practice": "Draft, revise, and compare before/after writing.",
        "evidence": "Published note, article draft, report section, or writing sample.",
    },
    "language": {
        "learn": "Learn vocabulary, grammar, and one real conversation pattern.",
        "practice": "Speak, listen, shadow, and write short responses.",
        "evidence": "Recorded speaking sample, vocabulary deck, or corrected paragraph.",
    },
    "design": {
        "learn": "Study one design principle and inspect examples.",
        "practice": "Recreate a layout and improve one original screen.",
        "evidence": "Figma frame, before/after screenshot, or mini case study.",
    },
    "general": {
        "learn": "Study one core idea and write short notes.",
        "practice": "Complete two focused exercises.",
        "evidence": "Short demo, note, checklist, or reflection.",
    },
}

PHASES = [
    "Foundation",
    "Core Practice",
    "Guided Mini Project",
    "Independent Project",
    "Portfolio Polish",
]


@dataclass
class WeeklyPlan:
    week: int
    phase: str
    focus: str
    learn_task: str
    practice_task: str
    review_task: str
    evidence: str
    checkpoint: str


@dataclass
class LearningPlan:
    skill: str
    domain: str
    goal: str
    weeks: int
    hours_per_week: int
    intensity: str
    weekly_rhythm: dict[str, int]
    milestones: list[str]
    weeks_plan: list[WeeklyPlan]

    def to_dict(self) -> dict:
        return asdict(self)


def infer_domain(skill: str) -> str:
    lowered = skill.lower()
    scores = {
        domain: sum(1 for keyword in keywords if keyword in lowered)
        for domain, keywords in DOMAIN_KEYWORDS.items()
    }
    best_domain, best_score = max(scores.items(), key=lambda item: item[1])
    return best_domain if best_score else "general"


def build_weekly_rhythm(hours: int, intensity: str) -> dict[str, int]:
    hours = max(hours, 1)
    ratios = {
        "light": (0.35, 0.45, 0.20),
        "balanced": (0.25, 0.55, 0.20),
        "deep": (0.20, 0.65, 0.15),
    }
    theory_ratio, practice_ratio, review_ratio = ratios.get(intensity, ratios["balanced"])
    theory = max(round(hours * theory_ratio), 1)
    practice = max(round(hours * practice_ratio), 1)
    review = max(hours - theory - practice, 1)
    return {"theory": theory, "practice": practice, "review": review}


def phase_for_week(week: int, total_weeks: int) -> str:
    if total_weeks <= 1:
        return PHASES[-1]
    if week == total_weeks:
        return PHASES[-1]
    index = min((week - 1) * (len(PHASES) - 1) // (total_weeks - 1), len(PHASES) - 2)
    return PHASES[index]


def make_week(skill: str, domain: str, week: int, total_weeks: int) -> WeeklyPlan:
    phase = phase_for_week(week, total_weeks)
    playbook = DOMAIN_PLAYBOOK[domain]
    focus = f"{phase} for {skill}"
    checkpoint = {
        "Foundation": "Explain the basic vocabulary without notes.",
        "Core Practice": "Finish exercises with fewer repeated mistakes.",
        "Guided Mini Project": "Complete a small project with references.",
        "Independent Project": "Build or explain something without a full tutorial.",
        "Portfolio Polish": "Publish a clear result with a README or reflection.",
    }[phase]
    return WeeklyPlan(
        week=week,
        phase=phase,
        focus=focus,
        learn_task=playbook["learn"],
        practice_task=playbook["practice"],
        review_task="Write a short reflection: what worked, what was hard, what to repeat.",
        evidence=playbook["evidence"],
        checkpoint=checkpoint,
    )


def make_milestones(skill: str, domain: str) -> list[str]:
    if domain == "data":
        return [
            f"Explain the main concepts behind {skill}.",
            "Analyze a small dataset and communicate one insight.",
            "Create a portfolio-ready chart, dashboard, notebook, or report.",
        ]
    if domain == "coding":
        return [
            f"Build a small working feature using {skill}.",
            "Debug one issue and document the fix.",
            "Publish a GitHub repo with README, setup steps, and screenshots/output.",
        ]
    if domain == "language":
        return [
            "Hold a short practice conversation.",
            "Write a corrected paragraph using new vocabulary.",
            "Record a before/after speaking sample.",
        ]
    return [
        f"Explain {skill} in simple words.",
        "Complete one realistic practice task.",
        "Publish or save one clear proof of progress.",
    ]


def build_plan(
    skill: str,
    weeks: int = 4,
    hours_per_week: int = 5,
    goal: str | None = None,
    intensity: str = "balanced",
    domain: str | None = None,
) -> LearningPlan:
    if weeks < 1:
        raise ValueError("weeks must be at least 1")
    if hours_per_week < 1:
        raise ValueError("hours_per_week must be at least 1")
    selected_domain = domain or infer_domain(skill)
    if selected_domain not in DOMAIN_PLAYBOOK:
        selected_domain = "general"
    selected_goal = goal or f"Build practical confidence in {skill}."
    weeks_plan = [make_week(skill, selected_domain, week, weeks) for week in range(1, weeks + 1)]
    return LearningPlan(
        skill=skill,
        domain=selected_domain,
        goal=selected_goal,
        weeks=weeks,
        hours_per_week=hours_per_week,
        intensity=intensity,
        weekly_rhythm=build_weekly_rhythm(hours_per_week, intensity),
        milestones=make_milestones(skill, selected_domain),
        weeks_plan=weeks_plan,
    )


def render_markdown(plan: LearningPlan) -> str:
    lines = [
        f"# Learning Plan: {plan.skill}",
        "",
        "## Goal",
        "",
        plan.goal,
        "",
        "## Plan Settings",
        "",
        f"- Domain: {plan.domain}",
        f"- Weeks: {plan.weeks}",
        f"- Hours per week: {plan.hours_per_week}",
        f"- Intensity: {plan.intensity}",
        "",
        "## Weekly Rhythm",
        "",
        f"- Theory: {plan.weekly_rhythm['theory']} hour(s)",
        f"- Practice: {plan.weekly_rhythm['practice']} hour(s)",
        f"- Review: {plan.weekly_rhythm['review']} hour(s)",
        "",
        "## Milestones",
        "",
    ]

    lines.extend(f"- {milestone}" for milestone in plan.milestones)
    lines.extend(["", "## Roadmap", ""])

    for week in plan.weeks_plan:
        lines.extend(
            [
                f"### Week {week.week}: {week.phase}",
                "",
                f"- Focus: {week.focus}",
                f"- Learn: {week.learn_task}",
                f"- Practice: {week.practice_task}",
                f"- Review: {week.review_task}",
                f"- Evidence: {week.evidence}",
                f"- Checkpoint: {week.checkpoint}",
                "",
            ]
        )

    lines.extend(
        [
            "## Reflection Template",
            "",
            "- What did I learn?",
            "- What was difficult?",
            "- What can I now build, explain, or show?",
            "- What should I practice next?",
        ]
    )
    return "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Generate a practical weekly learning plan for a skill.")
    parser.add_argument("skill", help="Skill to learn, for example: data visualization.")
    parser.add_argument("--weeks", "-w", type=int, default=4, help="Number of weeks.")
    parser.add_argument("--hours", "-hr", type=int, default=5, help="Hours per week.")
    parser.add_argument("--goal", help="Custom learning goal.")
    parser.add_argument("--domain", choices=sorted(DOMAIN_PLAYBOOK), help="Override inferred domain.")
    parser.add_argument("--intensity", choices=["light", "balanced", "deep"], default="balanced")
    parser.add_argument("--output", "-o", help="Write output to a file.")
    parser.add_argument("--json", action="store_true", help="Print JSON instead of Markdown.")
    args = parser.parse_args(argv)

    try:
        plan = build_plan(
            skill=args.skill,
            weeks=args.weeks,
            hours_per_week=args.hours,
            goal=args.goal,
            intensity=args.intensity,
            domain=args.domain,
        )
    except ValueError as exc:
        raise SystemExit(str(exc)) from exc

    output = json.dumps(plan.to_dict(), indent=2, ensure_ascii=False) if args.json else render_markdown(plan)
    if args.output:
        Path(args.output).write_text(output, encoding="utf-8")
        print(f"Output written to {args.output}")
    else:
        print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
