import os
import sys
from agent import generate_plan

def test():
    print("Testing generate_plan...")
    try:
        plan = generate_plan(
            start_city="Nagpur",
            destination="Goa",
            travelers=2,
            days=3,
            user_budget=30000,
            travel_style="Budget",
            interests=["beaches", "food", "sightseeing"]
        )
        with open("test_output.md", "w", encoding="utf-8") as f:
            f.write(plan)
        print("Plan generated successfully and saved to test_output.md!")
    except Exception as e:
        print(f"Error testing plan: {e}")
        sys.exit(1)

if __name__ == "__main__":
    test()
