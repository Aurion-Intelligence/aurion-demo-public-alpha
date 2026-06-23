# Aurion Demo Public Alpha — FAQ

> **Status: SUPPLEMENTAL.** This FAQ supports — and does not supersede — the canonical publish-pack
> documents: [`PUBLISH_PACK.md`](PUBLISH_PACK.md) (operator hub),
> [`KNOWN_LIMITATIONS_PUBLIC.md`](KNOWN_LIMITATIONS_PUBLIC.md), and the announcements
> ([`ANNOUNCEMENT_GITHUB.md`](ANNOUNCEMENT_GITHUB.md) / [`ANNOUNCEMENT_SOCIAL.md`](ANNOUNCEMENT_SOCIAL.md)).
> If anything here disagrees with those, the canonical docs win.
>
> Honest answers for a **controlled Demo Public Alpha**. Aurion is a local-first governed AI mission
> system. It is **not production-ready** and **not a full public alpha release yet**.

### Is Aurion production-ready?

No. Aurion is early developer-alpha software. It is **not production-ready**.

### Is this full public alpha?

No. This is a **controlled Demo Public Alpha** of one verified governed mission spine. Full public
alpha is **not** ready — it is currently blocked by the broad frontend (npm) test suite.

### Does Aurion have live autonomy?

No. Live autonomy is **not complete**. The demo runs a deterministic, local-first governed mission and
shows proposed/dry-run and read-only paths. Live autonomy controls are honestly shown as unavailable.

### Does Aurion send data to the cloud?

The demo is local-first and the public spine demo does not require the cloud. External/cloud model use
is gated — "external models require approval" — and is not part of the Demo Public Alpha surface. We do
not claim cloud escalation is production-ready.

### Can Aurion spend money?

Not in this demo. Cost evidence on the Mission Receipt is **advisory and read-only**. There is no real
spending in the demo, and we do not claim real spending adapters are live.

### Can Aurion use external tools?

The demo exercises permission checks (e.g. local read allowed; external network and writes denied). We
do **not** claim that all tools/actions/side-effects are permission-governed across the product.

### What is a Mission Receipt?

A human-readable, read-only summary of a governed mission: what Aurion understood, the plan and
microsteps, which permissions were checked, what was allowed or blocked, AuditLedger references, a
BlackBox decision-trace reference, advisory cost-governance evidence, warnings, and next steps. Missing
data is shown as *unavailable* — never faked green.

### Why local-first, not local-only?

Aurion is designed to run locally first — your goals and missions execute on your machine with local
models by default. It is local-*first*, not local-*only*: cloud/external model use is possible but
gated behind explicit approval, and is not part of this demo.

### What is missing?

Plenty — this is early software. Full public alpha is blocked by the broad frontend test suite. Most
lab/dev modules sit behind Developer Mode and are not part of the Demo Public Alpha surface. See
[`KNOWN_ISSUES.md`](KNOWN_ISSUES.md) and [`ALPHA_STATUS.md`](ALPHA_STATUS.md) for the generated,
evidence-derived truth.

### What is the next milestone?

Greening the broad frontend (npm) test suite, which is the current honest blocker for full public alpha.

### Can people contribute?

You can inspect and run the demo locally (see [`INSTALL_WALKTHROUGH.md`](INSTALL_WALKTHROUGH.md)).
Contribution processes are still being shaped during this early phase.

### What license is Aurion under?

This Demo Public Alpha repository is **open source under GNU AGPL-3.0-only** — see
[`../../LICENSE`](../../LICENSE). You may use, modify, redistribute, and commercially use Aurion under
AGPL-3.0-only.

AGPL is strong copyleft: if you distribute a modified version, you must make the modified source
available under AGPL-3.0-only, and if you run a modified version that users reach over a network, you
must offer them that modified source (AGPL §13). Commercial use under AGPL is allowed and does **not**
automatically require payment. **No paid commercial license exists today**; an alternative commercial
license may be developed later, subject to legal review. The **plugin/limb licensing boundary is still
under review** — we do not promise every independent plugin can stay proprietary. Advanced/private
Aurion modules outside this package are not covered by this
repository.

---

*See also: [Publish pack](PUBLISH_PACK.md) · [Demo script](DEMO_SCRIPT.md) ·
[Screenshot gallery](SCREENSHOT_GALLERY.md) · [Announcement draft](ANNOUNCEMENT_DRAFT.md).*
