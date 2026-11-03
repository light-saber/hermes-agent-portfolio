# Specialist Routing

This page distinguishes Hermes `delegate_task` specialists from other specialist profiles and external coding workers. It is a public-facing explanation, not a live registry.

## `delegate_task` specialists

Momo routes non-trivial work to one of these ten leaf agents. Each gets a scoped goal and relevant context, then returns a summary to Momo.

| Specialist | Route | Scope |
|---|---|---|
| MacPilot | `delegate_task` | Operate the user's Mac through approved remote-control paths. |
| StockMan | `delegate_task` | Equity research, portfolio analysis, and prediction workflows. |
| TaxBuddy | `delegate_task` | Tax preparation, reconciliation, and tax research. |
| HomeBase | `delegate_task` | Property and home-loan cases. |
| HealthGuard | `delegate_task` | Health insurance, claims, wearables, and family health workflows. |
| FamilyDoc | `delegate_task` | Family health information and triage, with appropriate clinical limitations. |
| CodeForge | `delegate_task` | Scope side projects and produce implementation handoffs; does not implement code. |
| Researcher | `delegate_task` | Multi-source, citation-backed research. |
| QABot | `delegate_task` | Evidence-led QA and exploratory testing. |
| HSBC Card Manager | `delegate_task` | Credit-card statement analysis and rewards optimization. |

## Profile-based caption worker

**Feather / WildlifePhoto** is not a `delegate_task` child. A local helper collects image observations and any EXIF values that were actually extracted, then invokes the dedicated `wildlifephoto` Hermes profile with its caption-specific skills. It returns a draft only: it does not publish, schedule, or edit posts.

This separate route exists because image analysis and account-specific caption formatting are a distinct workflow. A vision model's species guess is evidence, not certainty; captions must not invent metadata, location, or animal behavior.

## Coding execution is a separate stage

CodeForge scopes and hands off; a coding CLI executes only after an explicit user go-ahead. QABot can independently verify the resulting artifact. A specialist's profile/Bot presence does not imply it is the `delegate_task` route for every request.

## Dispatch guardrails

- Keep `delegate_task` workers as leaves unless the task explicitly authorizes an orchestrator role.
- Pass needed context explicitly. Do not assume a child can search Momo's OpenViking memory or share the parent's session.
- Keep scheduled prompts self-contained; cron sessions do not call `delegate_task`.
- Require the named worker's output contract, and verify external writes before claiming success.