# Custom GPT Update Workflow — Life OS Practical Co-Pilot

This document defines the **only supported process** for updating the Custom GPT after making repository changes.

GitHub does NOT auto-sync to Custom GPTs. Updates are always manual.

---

## Source of Truth

- **Runtime instructions:** `instructions/Instructions.txt`
- **Canonical structure:** `canon/CANON_MANIFEST.json`
- **Knowledge files:** `knowledge/`
- **Safety & routing rules:** Enforced silently via instructions

If these files are not uploaded, the GPT is stale.

---

## When You MUST Update the Custom GPT

You must re-upload files to the Custom GPT if you change:
- `instructions/Instructions.txt`
- Any file in `knowledge/`
- `canon/CANON_MANIFEST.json`
- Core behavior rules referenced by instructions

You do NOT need to update the GPT for:
- README changes
- ROADMAP changes
- Tests-only changes

---

## Step-by-Step Update Process (Required)

### Step 1 — Make repo changes
Edit files as needed.

### Step 2 — Run QuickSmoke
From repo root:
```powershell
.\tools\quicksmoke.ps1
