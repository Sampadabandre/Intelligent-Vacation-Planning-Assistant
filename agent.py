import json
import time
from groq import Groq
from config import GROQ_API_KEY, MODEL_NAME
import prompts
import budget

# Initialize Groq Client
client = Groq(api_key=GROQ_API_KEY)

def call_groq_with_retry(system_prompt, user_prompt, response_format=None, max_retries=3):
    """
    Wrapper for Groq API calls with exponential backoff for rate limits and 503 errors.
    """
    delay = 1
    for attempt in range(1, max_retries + 1):
        try:
            kwargs = {
                "model": MODEL_NAME,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ]
            }
            if response_format:
                kwargs["response_format"] = {"type": response_format}
                
            response = client.chat.completions.create(**kwargs)
            return response.choices[0].message.content
        except Exception as e:
            error_msg = str(e).lower()
            if "503" in error_msg or "unavailable" in error_msg or "429" in error_msg or "rate limit" in error_msg:
                if attempt == max_retries:
                    raise Exception(f"The AI model is currently experiencing high demand. Please try again later. (Details: {str(e)})")
                print(f"API busy (attempt {attempt}/{max_retries}). Retrying in {delay} seconds...")
                time.sleep(delay)
                delay *= 2
            else:
                # For other errors, don't retry, just raise
                raise Exception(f"AI Service Error: {str(e)}")

def safe_json_parse(text, default_value):
    """Safely parse JSON, handling potential markdown wrappers from the LLM."""
    try:
        text = text.strip()
        if text.startswith("```json"):
            text = text[7:]
        elif text.startswith("```"):
            text = text[3:]
        if text.endswith("```"):
            text = text[:-3]
        return json.loads(text.strip())
    except Exception as e:
        print(f"JSON Parsing Error: {e}")
        return default_value

def generate_plan(start_city: str, destination: str, travelers: int, days: int, user_budget: float, travel_style: str, interests: list) -> str:
    """
    Orchestrates the entire multi-agent workflow.
    Returns the final markdown plan or an error message.
    """
    if not GROQ_API_KEY:
        return "⚠️ Error: GROQ_API_KEY is missing. Please set it in the .env file."
        
    try:
        # ---------------------------------------------------------
        # AGENT 1: Preference Analysis
        # ---------------------------------------------------------
        agent1_input = f"""
        Start City: {start_city}
        Destination: {destination}
        Travelers: {travelers}
        Days: {days}
        Budget: {user_budget}
        Style: {travel_style}
        Interests: {interests}
        """
        
        response1_text = call_groq_with_retry(
            system_prompt=prompts.AGENT1_PREFERENCE_ANALYSIS_PROMPT, 
            user_prompt=agent1_input,
            response_format="json_object"
        )
        
        default_profile = {
            "travel_type": f"{travel_style} trip",
            "priority": interests,
            "budget_level": "moderate",
            "trip_duration": days
        }
        profile_json = safe_json_parse(response1_text, default_profile)

        # ---------------------------------------------------------
        # AGENT 3: Budget Planning Engine (Pure Python logic)
        # ---------------------------------------------------------
        budget_estimate = budget.estimate_budget(days, travelers, travel_style, user_budget)

        # ---------------------------------------------------------
        # AGENT 2: Destination Planning
        # ---------------------------------------------------------
        agent2_input = f"""
        Profile: {json.dumps(profile_json)}
        Destination: {destination}
        Days: {days}
        Interests: {interests}
        """
        
        response2_text = call_groq_with_retry(
            system_prompt=prompts.AGENT2_DESTINATION_PLANNING_PROMPT, 
            user_prompt=agent2_input,
            response_format="json_object"
        )
        
        default_destination_plan = {
            "recommended_activities": [{"name": "Explore", "description": f"Explore {destination}"}],
            "itinerary_structure": [{"day": 1, "morning": "Arrival", "afternoon": "Settle in", "evening": "Dinner"}]
        }
        destination_plan = safe_json_parse(response2_text, default_destination_plan)

        # ---------------------------------------------------------
        # AGENT 4: Plan Validation Agent (AI validation)
        # ---------------------------------------------------------
        agent4_input = f"""
        Destination: {destination}
        Itinerary: {json.dumps(destination_plan)}
        """
        response4_text = call_groq_with_retry(
            system_prompt=prompts.AGENT4_PLAN_VALIDATION_PROMPT, 
            user_prompt=agent4_input,
            response_format="json_object"
        )
        
        validation = safe_json_parse(response4_text, {"is_valid": True, "feedback": ""})
        
        if not validation.get("is_valid", True):
            warning_note = f"\n\n**⚠️ AI Validation Warning:** {validation.get('feedback', 'Potential issues with this plan.')}"
        else:
            warning_note = ""

        # ---------------------------------------------------------
        # AGENT 5: Final Vacation Plan Generator
        # ---------------------------------------------------------
        agent5_input = f"""
        Trip Details: Start: {start_city}, Dest: {destination}, Days: {days}, Travelers: {travelers}, Style: {travel_style}, Interests: {interests}, User Budget: {user_budget}
        
        Agent 1 Profile: {json.dumps(profile_json)}
        
        Agent 2 Plan: {json.dumps(destination_plan)}
        
        Agent 3 Budget: {json.dumps(budget_estimate)}
        """
        
        response5_text = call_groq_with_retry(
            system_prompt=prompts.AGENT5_FINAL_GENERATOR_PROMPT, 
            user_prompt=agent5_input
        )
        
        final_markdown = response5_text + warning_note
        return final_markdown

    except Exception as e:
        return f"### ⚠️ System Error\n{str(e)}\n\nPlease try clicking 'Generate Vacation Plan' again in a few moments."
