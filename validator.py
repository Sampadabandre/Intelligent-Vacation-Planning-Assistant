def validate_inputs(start_city: str, destination: str, travelers: int, days: int, budget: float, interests: list) -> tuple[bool, str]:
    """
    Validates user inputs from the Gradio interface.
    Returns (is_valid, error_message).
    """
    if not destination or not destination.strip():
        return False, "Please enter a destination."
    
    if not start_city or not start_city.strip():
        return False, "Please enter your starting city."
    
    if budget is None or budget <= 0:
        return False, "Please enter a valid budget (greater than 0)."
    
    if travelers is None or travelers < 1:
        return False, "Number of travelers must be at least 1."
    
    if days is None or days < 1:
        return False, "Trip duration must be at least 1 day."
    
    return True, ""
