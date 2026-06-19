# AetherOS Documentation

This directory contains the canonical documentation for AetherOS, ordered for professional software engineering practice. Each document builds on the previous one. Read them in sequence.

## Document Chain

| Order | Document | Purpose | Audience |
|-------|----------|---------|----------|
| 01 | [01_VISION.md](./01_VISION.md) | Strategic north star — why AetherOS exists and where it is headed | Founders, contributors, stakeholders |
| 02 | [02_PRD.md](./02_PRD.md) | Product Requirements Document — what we build, for whom, and by when | Product, engineering, design |
| 03 | [03_SRS.md](./03_SRS.md) | Software Requirements Specification — functional and non-functional requirements | Engineering, QA |
| 04 | [04_HLD.md](./04_HLD.md) | High Level Design — system structure, components, and data flows | Engineering, architecture |
| 05 | [05_LLD.md](./05_LLD.md) | Low Level Design — implementation details, APIs, schemas, algorithms | Engineering |

## Reading Order

```
01_VISION  →  02_PRD  →  03_SRS  →  04_HLD  →  05_LLD
   Why          What         Must do      Structure    Implementation
```

## Document Status

| Document | Status |
|----------|--------|
| 01_VISION.md | Draft |
| 02_PRD.md | Not started |
| 03_SRS.md | Not started |
| 04_HLD.md | Not started |
| 05_LLD.md | Not started |

## Conventions

- **Vision** is stable for years; change only when the fundamental problem or market thesis shifts.
- **PRD** and **SRS** change per release or milestone.
- **HLD** and **LLD** change when architecture or implementation changes.
- Numbered prefixes enforce reading order and traceability.
- Downstream documents must trace requirements back to upstream documents.

## Traceability Rule

Every feature in the PRD must connect to a strategic pillar in the Vision. Every requirement in the SRS must connect to a PRD item. Every component in the HLD must satisfy one or more SRS requirements.
