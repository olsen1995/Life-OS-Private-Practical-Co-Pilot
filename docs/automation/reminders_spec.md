# Reminders & Check-ins Spec (Planning Only)

Status: Planning doc (no automation implementation yet)

Purpose:
- Define what reminders/check-ins exist in Life OS
- Define required inputs and safety boundaries
- Keep reminders non-invasive, user-led, and low-regret
- Prevent scope creep and “automation before clarity”

Non-goals (for now):
- No scheduled automation code
- No background monitoring
- No calendar/email integrations
- No notifications without explicit user opt-in

---

## 1) Core Principles

1. User agency first
   - Reminders exist only when the user asks for them.
   - Default is no reminders.

2. Safety and reversibility
   - Reminders must not create harmful or high-pressure advice loops.
   - High-risk domains (vehicles/electricity/chemicals/food safety/baby safety/large $$) require STOP/CHECK framing when advice is requested.

3. Minimal friction
   - A reminder should be quick to set up and quick to act on.
   - Use short prompts with structured responses.

4. Non-creepy memory discipline
   - Do not store sensitive personal info unless the user explicitly requests it.
   - Avoid reminders that imply tracking without consent.

---

## 2) Reminder Types (Catalog)

Each reminder has:
- Trigger: when it should occur
- Inputs: what data is needed
- Output: what the assistant should say/do
- Safety boundary: what it must not do

### R1 — Daily Check-In (Core)
Trigger:
- Daily (user-chosen time) or on-demand
Inputs:
- Energy (Low/Med/High)
- Time available (Quick/Normal/Deep)
- Stress (Low/Med/High)
Optional:
- Priority, constraints, money/logistics
Output:
- Use knowledge/02_Daily_CheckIn_Template.md
- Return a small, actionable plan (1–3 items)
Safety boundary:
- Do not overwhelm; do not add extra goals
- Ask 1–3 questions max only if needed

### R2 — Weekly Review (Light)
Trigger:
- Weekly (user-chosen day/time)
Inputs:
- Wins (1–3)
- Problems (1–3)
- Next week’s top priority
Output:
- Summarize themes
- Suggest 1–2 system tweaks (habits/tools/checklists)
Safety boundary:
- No shaming language
- No medical/financial directives without context

### R3 — Skincare Routine Check (Optional)
Trigger:
- Weekly (user-chosen)
Inputs:
- Irritation level (None/Mild/Moderate)
- Any new products or reactions
Output:
- Confirm routine consistency using knowledge/10_Skincare.md
- Suggest conservative adjustments if irritation exists
Safety boundary:
- No medical claims; recommend professional advice if severe reactions

### R4 — Bills & Due Dates (Optional / Higher-risk)
Trigger:
- User-provided due dates
Inputs:
- Bill name, amount (CAD), due date, payment method
Output:
- Reminder prompt only (no financial advice unless asked)
Safety boundary:
- Do not assume ability to pay; do not create debt advice without explicit request

### R5 — “Don’t Forget” One-offs (Core)
Trigger:
- One-time date/time set by user
Inputs:
- Reminder text + time
Output:
- Simple reminder, no added advice
Safety boundary:
- Do not store extra details beyond what the user gave

---

## 3) Setup Flow (Conversation UX)

When user asks for reminders, the assistant should collect:
1) What type? (Daily check-in / weekly review / one-off / bills / skincare)
2) When? (time, timezone)
3) How often? (daily/weekly/once)
4) What should the reminder say? (short prompt)
5) Any boundaries? (e.g., “don’t mention X”, “keep it short”)

Then confirm in one sentence:
- “Okay — I’ll remind you [when] to [do X].”

---

## 4) Safety Boundaries (Hard Rules)

- No reminders for illegal activity
- No reminders that pressure self-harm, dieting abuse, or harmful behaviors
- No medical reminders framed as diagnosis or treatment plans
- For baby/child topics: conservative guidance and recommend professional confirmation when needed
- For chemicals/electricity/vehicles: remind to follow STOP/CHECK and seek a pro if red flags appear

---

## 5) Implementation Notes (Future)

Potential future modules:
- A reminders registry (JSON) stored in repo for templates
- A “prompt pack” for reminder messages (minimal, consistent phrasing)
- Optional integration with calendar tools only after planning is approved

Version discipline:
- If this spec changes, bump VERSION and note in CHANGELOG.

Related documents:
- knowledge/02_Daily_CheckIn_Template.md
- knowledge/10_Skincare.md
- knowledge/13_DecisionCheck.md
- docs/safety/TIER2_SAFETY_POLISH.md
