# SkyWindow

SUBMISSION HOLD: This version classifies caller-supplied sky narratives and calculates a viewing window. Although its local and StudioNet tests passed, it does not yet make a consensus-critical shared state transition from independently checkable evidence. Do not submit this deployment as a review-ready intelligent contract. A different mechanism and new deployment are required.

Batch C2. A reusable GenLayer intelligent contract that selects the longest consecutive run of declared clear viewing conditions from an ordered series of astronomy time slots. The caller submits two to twelve labelled slots and a short sky narrative for each. Independent validators classify every slot as `CLEAR`, `CLOUDY`, or `UNCERTAIN`. Deterministic code selects the longest contiguous `CLEAR` run, breaking ties toward the earliest run.

The narratives are user declarations. The contract does not fetch weather data, verify an observer, or guarantee real-world sky conditions. `UNCERTAIN` never counts as clear. Anyone relying on this for an observing event must independently check the actual conditions.

## Interface

`assess_run(run_key, site_notes, slot_labels, narratives)` performs one immutable assessment under a caller-scoped key. `get_run(run_id)` returns canonical JSON containing every classification, the winning start/end indexes, and the run length. `run_count()` returns the record count.

## Review boundary

The model's only role is to classify the written condition in each slot. Validators rerun the full same-length ordered classification and compare every label. The longest-run scan, tie break, and status are deterministic. Duplicate labels, blank text, excess slots, malformed model output, and repeated keys are rejected before state changes.

This differs from the workspace's multi-reporter accessibility snapshot: one caller supplies an ordered time series; there is no reporter quorum, report voting, or coordinator seal. It also differs from EnergyMixReceipt's weighted source totals: the output is a contiguous interval selected by sequence order.

## Verification

Run `genvm-lint check contracts/sky_window.py`, `genvm-lint typecheck contracts/sky_window.py --strict`, and `pytest -q`. The opt-in StudioNet smoke test uses a fresh encrypted wallet outside the repository and records the exact source, ABI, address, and transaction evidence in `deployments/studionet.json`.

StudioNet deployment: [0x5127a4d1fEfff6B0E4BB55752286614ebaA5C5C8](https://explorer-studio.genlayer.com/address/0x5127a4d1fEfff6B0E4BB55752286614ebaA5C5C8). See `AUDIT.md` for the review boundary and test results.
