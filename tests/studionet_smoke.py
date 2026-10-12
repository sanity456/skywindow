"""Opt-in StudioNet flow with a newly generated, encrypted project wallet."""
import json
import secrets

from gltest.types import TransactionHashVariant
from release_support import prepare, save_proof, send


def test_studionet_sky_window_flow():
    ctx = prepare("sky_window.py", ("creator",))
    creator, account = ctx["contracts"]["creator"], ctx["accounts"]["creator"]
    transactions = {"deploy": ctx["deployment_hash"]}
    run_key = "release_" + secrets.token_hex(4)
    labels = ["20:00", "20:30", "21:00", "21:30"]
    narratives = [
        "Heavy clouds obstruct the sky throughout this slot.",
        "The sky is mostly clear and unobstructed for astronomy viewing.",
        "The sky remains clear and unobstructed for astronomy viewing.",
        "Patchy clouds leave the conditions uncertain for this slot.",
    ]
    send(transactions, "assess_run", creator.assess_run(args=[run_key, "Open field with a clear horizon, as declared by the caller.", labels, narratives]))
    run_id = account.address.lower() + ":" + run_key
    final = json.loads(creator.get_run(args=[run_id]).call(transaction_hash_variant=TransactionHashVariant.LATEST_FINAL))
    assert final["status"] == "WINDOW_FOUND" and final["best_start_index"] == 1, final
    assert final["best_end_index"] == 2 and final["best_length"] == 2, final
    assert [slot["condition"] for slot in final["slots"]] == ["CLOUDY", "CLEAR", "CLEAR", "UNCERTAIN"], final
    save_proof(ctx, transactions, run_id, "WINDOW_FOUND")
