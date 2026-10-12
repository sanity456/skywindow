# Release audit

SUBMISSION HOLD (2026-10-12): The earlier technical checks below do not establish review suitability. This version is a one-party classifier/selector from caller narratives, with no consensus-critical shared settlement or independent evidence source. The earlier StudioNet address remains a test artifact, not a recommended submission. A substantially different contract and new deployment are required.

- Mechanism: consensus classifies an ordered series of written sky-condition slots; deterministic code finds the earliest longest contiguous clear run. There is no reporter quorum, coordinator seal, weighted energy aggregate, or rainfall calculation.
- Source policy: site and slot narratives are public caller declarations. No weather service or astronomical source is fetched or authenticated.
- Security: caller-scoped immutable records, 2–12 aligned slots, unique labels, text bounds, strict vector parsing, and independent validator rerun. No funds are held.
- Local gates: GenVM lint and strict type check passed; 3 direct tests passed, including tie breaking, no clear run, input validation, and validator disagreement.
- StudioNet gate: full deploy/assess flow passed with its own fresh wallet; final state `WINDOW_FOUND`; read-only release proof passed. Manifest source bytes and ABI match the deployment.
- Limits: results summarize written conditions; actual sky conditions and weather must be checked independently.
