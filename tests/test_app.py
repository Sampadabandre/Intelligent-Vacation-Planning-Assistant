import pytest
from validator import validate_inputs
from budget import estimate_budget

def test_valid_inputs():
    is_valid, msg = validate_inputs("Nagpur", "Goa", 2, 3, 15000, ["Beaches", "Food"])
    assert is_valid is True
    assert msg == ""

def test_invalid_budget():
    is_valid, msg = validate_inputs("Nagpur", "Goa", 2, 3, 0, ["Beaches"])
    assert is_valid is False
    assert "budget" in msg.lower()

def test_empty_destination():
    is_valid, msg = validate_inputs("Nagpur", "   ", 2, 3, 15000, ["Beaches"])
    assert is_valid is False
    assert "destination" in msg.lower()

def test_invalid_travelers():
    is_valid, msg = validate_inputs("Nagpur", "Goa", 0, 3, 15000, ["Beaches"])
    assert is_valid is False
    assert "travelers" in msg.lower()

def test_budget_calculation_sufficient():
    # 2 travelers, 3 days, Budget style, 15000 user budget
    # Base budget style cost per day = 800+500+300+400 = 2000
    # Total for 2 travelers 3 days = 2000 * 2 * 3 = 12000
    # Misc = 10% = 1200
    # Total = 13200
    res = estimate_budget(days=3, travelers=2, travel_style="Budget", user_budget=15000)
    assert res["is_sufficient"] is True
    assert res["total_estimated"] == 13200
    assert res["remaining_budget"] == 1800

def test_budget_calculation_insufficient():
    # 2 travelers, 3 days, Luxury style, 15000 user budget
    res = estimate_budget(days=3, travelers=2, travel_style="Luxury", user_budget=15000)
    assert res["is_sufficient"] is False
    assert res["total_estimated"] > 15000
