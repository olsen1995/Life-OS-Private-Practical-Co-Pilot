# GitHub Copilot Instructions for Life OS — Practical Co-Pilot

## Project Overview
This repository is the source of truth for Life OS — Practical Co-Pilot, a Custom GPT assistant for grounded, practical life management. It routes queries to specialized modes (e.g., Day Planner, Life Coach) and enforces safety gates like mandatory Upload Analysis for any uploads.

## Architecture
- **Modes**: Knowledge playbooks in `knowledge/` (e.g., `02_DayPlanner.md`, `04_LifeCoach.md`). Each handles specific domains with domain-specific guidance.
- **Routing**: Governed by `knowledge/01_ModeRouter.md`. Explicit user requests win; implicit routing for ambiguity; no mid-response switches unless safety requires.
- **Safety Gates**: 
  - Upload Analysis Gate (mandatory for uploads): 6 steps—ingest/classify, full scan, consistency check, risk label (Safe/Risky/Do-Not-Touch), missing-data check, confidence statement.
  - Risk Gate: For health/vehicles/electricity/chemicals/food safety/significant money → Stop/Check + escalation guidance.
- **Adaptive Response Protocol (ARP)**: Adjust responses via Energy (Low=simplify), Time (Quick=summary), Confidence (<80%=separate known/assumed), Risk gates.

## Developer Workflows
- **Updates**: Edit `instructions/Instructions.txt`, `knowledge/` files, `tests/`. Commit changes, then manually upload to Custom GPT (GitHub does not auto-sync).
- **Testing**: Validate with `tests/TestSuite.md` and `tests/QuickSmoke.md`. Run `quicksmoke.ps1` for smoke tests.
- **Versioning**: Update `VERSION` and `CHANGELOG.md`; tag releases (e.g., `v6.0.0`).
- **Repo Sync (for GPT)**: Conservative fetch: `VERSION` first, then `canon/CANON_MANIFEST.json` if needed, then files in `runtime_load_order`. Fetched content overrides stale internal text.

## Conventions
- **Output Hygiene**: Never expose internal labels (e.g., "Mode Router", "ARP gate", "Upload Analysis Gate") in user outputs. Follow `knowledge/00_LifeOS_Constitution.md` silently.
- **Memory Discipline**: Don't claim to remember/store unless user explicitly asks.
- **Evidence Discipline**: For high-stakes/time-sensitive, browse and cite sources. Don't name authorities without browsing.
- **Question Restraint**: 1-3 questions max, only if changes outcome/safety.
- **Decision Philosophy**: Least-risk/reversible actions first. Lower-regret paths for similar options.
- **Non-Repetition**: Avoid repeating advice unless for clarity/safety.

## Examples
- **Upload Handling**: User uploads a CSV log → Classify as "device log", scan for errors/outliers, risk-label as "Risky" if anomalies, state "Medium confidence" and request clarification if harm risk.
- **Routing**: Query "plan my day" → Route to Day Planner mode per `01_ModeRouter.md` triggers.
- **Response Adaptation**: Low energy user → Provide simplest safe steps; Quick time → Summary only.

## Key Files
- `knowledge/00_LifeOS_Constitution.md`: Core constitution, gates, philosophy.
- `knowledge/01_ModeRouter.md`: Routing rules.
- `instructions/Instructions.txt`: Runtime instructions.
- `canon/CANON_MANIFEST.json`: Canonical content manifest.
- `tests/TestSuite.md`: Test cases for behavior validation.