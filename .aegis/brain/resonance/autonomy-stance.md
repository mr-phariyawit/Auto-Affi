# Autonomy Stance -- Human as Supervisor Only

> Source: SPEC.md section 1.1
> Last synced: 2026-05-13
> Purpose: Define the human's role in the system. This is load-bearing
> for every autonomy decision, escalation policy, and agent behavior.

## The Principle (verbatim from SPEC 1.1)

> "...by humans as supervisors only"
> (Thai: "โดยมนุษย์เป็นเพียง supervisor")

The human does NOT:
- Create content
- Write scripts
- Edit videos
- Choose products
- Schedule posts
- Curate wiki entries

The human DOES:
- Monitor dashboard (ops console, Next.js + shadcn/ui)
- Set budget constraints
- Approve/reject edge cases escalated by Safety agent
- Override kill switches
- Review wiki promotions (bilateral wiki sync)
- Set strategic direction (niche selection, platform priority)

## Escalation Policy

The system escalates to human ONLY when:

1. **Safety threshold exceeded**: Supervisor/Safety agent detects a
   violation it cannot auto-resolve (e.g., potential legal issue,
   repeated platform policy violations)
2. **Budget override needed**: daily cost exceeds budget * 1.1 and
   human must decide whether to increase budget or halt
3. **Platform ban/suspension**: requires human account recovery action
4. **Kill switch activation**: auto-kill fires (3 policy violations
   in 24h) -- human must review and re-enable

## Quantitative Target

| Phase | Human Intervention Rate |
|-------|------------------------|
| Phase 1 | <= 30% of pipeline runs |
| Phase 3 | <= 5% of pipeline runs |

## Implications for AEGIS Agent Design

- Agents must NOT present options to the human. They decide and execute.
- The AEGIS Master Brain Protocol (MBP) aligns with this: Nick Fury decides,
  agents execute, human watches.
- The 4 MBP escalation categories (Identity, Irreversible scope, External
  access, Explicit approval gate) map to the Auto-Affi escalation triggers above.
- Pre-publish review at low confidence is an open question (SPEC 15, Q4):
  what confidence threshold triggers human review? This should be decided
  by data from Phase 1 outcomes.

## Kill Switches (SPEC 10.4)

Available at: per-product, per-campaign, per-platform, and global level.
Accessible through ops console.
Auto-kill trigger: platform returns policy violation 3 times in 24 hours.
