# Skill Learning Planner

A Python CLI that turns a skill goal into a weekly learning roadmap. It infers the learning domain, balances theory/practice/review, and creates checkpoints plus portfolio evidence for each week.

## Highlights

- Supports data, coding, writing, language, design, and general skill plans.
- Infers the domain from the skill name or accepts a manual `--domain`.
- Generates weekly roadmap sections with learn, practice, review, evidence, and checkpoint tasks.
- Supports light, balanced, and deep intensity modes.
- Exports Markdown or JSON.
- Uses only the Python standard library.

## Quick Start

```bash
python skill_planner.py "data visualization" --weeks 4 --hours 5
```

Custom goal:

```bash
python skill_planner.py "SQL for analytics" --weeks 6 --hours 6 --goal "Build confidence writing SQL reports"
```

Deep coding plan:

```bash
python skill_planner.py "Flutter app development" --domain coding --intensity deep --weeks 5
```

Write Markdown:

```bash
python skill_planner.py "Power BI dashboards" --output learning_plan.md
```

Write JSON:

```bash
python skill_planner.py "English speaking" --json --output learning_plan.json
```

## Install As A CLI

```bash
python -m pip install -e .
skill-planner "data visualization" --weeks 4
```

## Output Sections

- Goal
- Plan Settings
- Weekly Rhythm
- Milestones
- Roadmap
- Reflection Template

## Tests

```bash
python -m unittest discover -s tests -v
```

## Portfolio Note

I built this tool to make self-study more measurable: choose a skill, plan the weeks, practice consistently, and keep evidence of progress.
