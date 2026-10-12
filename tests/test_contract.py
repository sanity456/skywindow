import json
from pathlib import Path

import pytest


@pytest.fixture
def setup(direct_vm, direct_deploy, direct_accounts):
    direct_vm.sender = direct_accounts[0]
    source = Path(__file__).parents[1] / "contracts" / "sky_window.py"
    return direct_deploy(str(source), sdk_version="v0.2.16")


def mock(vm, conditions):
    vm.clear_mocks()
    vm.mock_llm("Classify each declared astronomy viewing time slot", json.dumps({"conditions": conditions}))


def test_earliest_longest_clear_run_and_validator(setup, direct_vm):
    mock(direct_vm, ["CLEAR", "CLEAR", "CLOUDY", "CLEAR", "CLEAR"])
    run_id = setup.assess_run("night1", "Open field outside town.",
        ["20:00", "20:30", "21:00", "21:30", "22:00"],
        ["Clear unobstructed sky", "Mostly clear unobstructed sky", "Heavy clouds", "Clear unobstructed sky", "Clear sky"])
    state = json.loads(setup.get_run(run_id))
    assert state["best_start_index"] == 0 and state["best_end_index"] == 1
    assert state["best_length"] == 2 and state["status"] == "WINDOW_FOUND"
    assert direct_vm.run_validator(leader_result=["CLEAR", "CLEAR", "CLOUDY", "CLEAR", "CLEAR"])
    assert not direct_vm.run_validator(leader_result=["CLEAR", "CLOUDY", "CLOUDY", "CLEAR", "CLEAR"])


def test_no_clear_window_and_atomic_error(setup, direct_vm):
    mock(direct_vm, ["UNCERTAIN", "CLOUDY"])
    run_id = setup.assess_run("night2", "Outdoor site.", ["20:00", "20:30"], ["Patchy clouds", "Heavy cloud cover"])
    state = json.loads(setup.get_run(run_id))
    assert state["status"] == "NO_CLEAR_WINDOW" and state["best_start_index"] == -1
    before = setup.run_count()
    mock(direct_vm, ["CLEAR"])
    with direct_vm.expect_revert("invalid condition vector"):
        setup.assess_run("night3", "Outdoor site.", ["20:00", "20:30"], ["Clear sky", "Clear sky"])
    assert setup.run_count() == before


def test_bounds_owner_scope_and_duplicate_labels(setup, direct_vm, direct_accounts):
    with direct_vm.expect_revert("aligned slots"):
        setup.assess_run("bad", "Site", ["20:00"], ["Clear sky"])
    with direct_vm.expect_revert("duplicate slot label"):
        setup.assess_run("bad", "Site", ["20:00", "20:00"], ["Clear sky", "Clear sky"])
    mock(direct_vm, ["CLEAR", "CLEAR"])
    first = setup.assess_run("shared", "Site", ["20:00", "20:30"], ["Clear sky", "Clear sky"])
    with direct_vm.expect_revert("already exists"):
        setup.assess_run("shared", "Site", ["20:00", "20:30"], ["Clear sky", "Clear sky"])
    direct_vm.sender = direct_accounts[1]
    second = setup.assess_run("shared", "Site", ["20:00", "20:30"], ["Clear sky", "Clear sky"])
    assert first != second
