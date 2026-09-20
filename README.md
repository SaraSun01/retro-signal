# RetroSignal

Weekly team feedback that turns honest reflection into clear action.

RetroSignal is a focused retrospective tool for project teams. It collects private Start, Stop, and Continue feedback, reveals it at the right moment, helps the team group and prioritize themes, and preserves the decisions and action items that come out of the discussion.

## What it will do

- Collect attributed or anonymous feedback cards before a retrospective
- Reveal all feedback simultaneously
- Suggest editable thematic clusters with OpenAI
- Let participants allocate three hidden, stackable votes
- Build a prioritized discussion agenda
- Record decisions and accountable action items
- Extract draft outcomes from pasted transcript text for facilitator review
- Publish a durable retrospective summary

## Product principles

- Anonymous feedback stays anonymous.
- Vote totals remain hidden until voting closes.
- AI suggests; people decide.
- The product supports retrospectives rather than becoming a survey, recording, or project-management platform.

## Planned stack

- Python and Django
- Django templates, HTMX, Tailwind CSS, and SortableJS
- PostgreSQL
- Django Channels and Redis
- OpenAI Responses API with Structured Outputs
- Docker Compose

## Project status

RetroSignal is in early development. The product scope and implementation architecture are defined, and the implementation backlog is tracked in GitHub Issues.

## Local development

Create and activate a virtual environment, then install the pinned dependency:

```shell
python -m pip install -r requirements.txt
```

## Tests

Run the test suite with one command:

```shell
python manage.py test
```

## Documentation

- [MVP plan](_docs/plan.md)
- [Architecture](_docs/architecture.md)
- [Implementation backlog](https://github.com/SaraSun01/retro-signal/issues)
