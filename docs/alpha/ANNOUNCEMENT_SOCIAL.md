# Aurion Demo Public Alpha — Social Announcements

> Three reusable public announcement variants for Aurion's **Demo Public Alpha**.
> Repository: https://github.com/Aurion-Intelligence/aurion-demo-public-alpha
> Each is deliberately low-hype and honest. Edit before posting; nothing is published without operator
> approval. Every variant includes: local-first · permission-governed · mission-based · Mission Receipts
> · Demo Public Alpha · not production / not full public alpha. The copy avoids hype and grandiose
> absolute-safety / general-intelligence claims by design.

---

## Short (social post, ~250–400 characters)

> Aurion is a local-first, permission-governed AI mission system. This Demo Public Alpha runs a small,
> real governed mission offline — you watch allowed vs blocked actions and inspect fresh AuditLedger,
> BlackBox, and Mission Receipt evidence. Not the full runtime, not full public alpha. AGPL-3.0.
> Feedback welcome.

---

## Technical (social post, 3–5 short paragraphs)

> Aurion is a local-first, permission-governed AI mission system. I'm sharing a Demo Public Alpha you can
> actually run: one command executes a small, real governed mission on Linux/macOS/Windows — offline,
> Python standard library only, no model, no network.
>
> The mission goes goal → deterministic plan → permission evaluation → allowed local read → allowed
> bounded write → **blocked** external-network step. It produces fresh AuditLedger events, BlackBox
> decision records, and a Mission Receipt you can open and inspect. You see exactly which actions were
> allowed and which were denied, and why.
>
> It's deliberately bounded: a small public implementation of the governed spine, not the full Aurion
> runtime. No Command Center backend, no live autonomy, no cloud routing, no spending — and none
> demonstrated. CI runs the mission and tests green on Linux, Windows, and macOS.
>
> Honesty about scope: this is a Demo Public Alpha, **not** a full public alpha, production release, or
> enterprise platform, and **not** proof of complete unattended autonomy. AGPL-3.0-only; commercial
> terms and a contributor process are not finalized yet (code merges are paused; feedback/issues
> welcome).
>
> Try it: `python3 -m aurion_demo run` (or `py -m aurion_demo run` on Windows), then
> `python3 -m aurion_demo replay` to validate the historical proof.
> https://github.com/Aurion-Intelligence/aurion-demo-public-alpha

---

## Longer (GitHub / community announcement)

> **Aurion Demo Public Alpha — a runnable, governed AI mission, end to end**
>
> Aurion is a local-first, permission-governed AI mission system. Most AI tooling focuses on giving
> agents more power; Aurion focuses on **governing** that power — checking "should this be allowed?"
> before acting, recording what it decided and why, and leaving a durable receipt.
>
> This Demo Public Alpha is the smallest honest proof of that idea, and you can run it yourself in one
> command on Linux, macOS, or Windows. It's offline and uses the Python standard library only — no
> model, no API keys, no network.
>
> The bundled mission is: *"Review the included project note, identify three action items, save the
> result inside the demo workspace, and do not use the internet."* When you run it, you see:
>
> - a deterministic plan with microsteps,
> - a permission evaluation for each step,
> - an **allowed** local read (only inside the bundled workspace),
> - an **allowed** bounded write (only inside the generated-artifacts directory),
> - a **blocked** external-network step (no network permission is granted),
> - fresh **AuditLedger** events, **BlackBox** decision records, and a **Mission Receipt** that
>   cross-references them.
>
> ```bash
> python3 -m aurion_demo run        # fresh real governed mission
> py -m aurion_demo run             # (Windows)
> python3 -m aurion_demo replay     # validate the historical proof artifacts
> ```
>
> **What this is not:** this is a bounded Demo Public Alpha, **not** the full Aurion runtime, a
> production release, an enterprise platform, or proof of complete unattended autonomy. There's no
> Command Center backend, live autonomy, cloud routing, or spending here — and none is demonstrated.
> Full public alpha is **not** ready.
>
> **License & contributing:** open source under AGPL-3.0-only. Bug reports, questions, and feedback are
> welcome via GitHub Issues. External code contributions (pull requests) are **paused** until a
> contributor-rights process is finalized — please don't invest in large PRs yet.
>
> Repository: https://github.com/Aurion-Intelligence/aurion-demo-public-alpha
