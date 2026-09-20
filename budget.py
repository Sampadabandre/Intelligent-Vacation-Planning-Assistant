def estimate_budget(days: int, travelers: int, travel_style: str, user_budget: float) -> dict:
    """
    Agent 3: Budget Planning Engine (Pure Python Logic)
    Estimates the budget based on heuristics and compares it to the user's budget.
    """
    # Base costs per person per day (in INR) based on travel style
    style_multipliers = {
        "Budget": {"accommodation": 800, "food": 500, "transport": 300, "activities": 400},
        "Comfort": {"accommodation": 2500, "food": 1200, "transport": 800, "activities": 1000},
        "Luxury": {"accommodation": 8000, "food": 3000, "transport": 2000, "activities": 3000},
        "Adventure": {"accommodation": 1500, "food": 800, "transport": 1000, "activities": 2500},
    }

    style_costs = style_multipliers.get(travel_style, style_multipliers["Comfort"])

    # Calculate estimated costs
    est_accommodation = style_costs["accommodation"] * travelers * days
    est_food = style_costs["food"] * travelers * days
    est_transport = style_costs["transport"] * travelers * days
    est_activities = style_costs["activities"] * travelers * days
    est_misc = (est_accommodation + est_food + est_transport + est_activities) * 0.10 # 10% for misc

    total_estimated = est_accommodation + est_food + est_transport + est_activities + est_misc

    # Compare with user budget
    is_sufficient = total_estimated <= user_budget
    remaining = user_budget - total_estimated
    
    # Generate notes based on budget comparison
    notes = []
    if is_sufficient:
        notes.append(f"Your budget is sufficient. You have an estimated remaining amount of ₹{remaining:,.2f}.")
    else:
        notes.append(f"Your estimated cost (₹{total_estimated:,.2f}) exceeds your budget (₹{user_budget:,.2f}) by ₹{abs(remaining):,.2f}.")
        notes.append("Consider reducing the number of days, switching to a more budget-friendly travel style, or picking fewer paid activities.")

    return {
        "breakdown": {
            "Accommodation": est_accommodation,
            "Food": est_food,
            "Transportation": est_transport,
            "Activities": est_activities,
            "Miscellaneous": est_misc
        },
        "total_estimated": total_estimated,
        "is_sufficient": is_sufficient,
        "remaining_budget": remaining,
        "notes": notes
    }
