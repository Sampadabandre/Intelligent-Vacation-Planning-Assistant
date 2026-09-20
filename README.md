---
title: Intelligent Vacation Planning Assistant
emoji: ✈️
colorFrom: blue
colorTo: indigo
sdk: gradio
app_file: app.py
pinned: false
---
# ✈️ Intelligent Vacation Planning Assistant

## 1. Project Title
Intelligent Vacation Planning Assistant

## 2. Project Description
An AI-powered Intelligent Vacation Planning Assistant built using Python, Gradio, and the Groq API. The system takes a user's travel preferences and generates a personalized vacation plan, including an overview, day-wise itinerary, budget breakdown, and recommended activities.

## 3. Problem Statement
Planning a vacation manually is time-consuming. Users often have to jump between multiple websites to figure out the destination, itinerary, and estimated costs based on their specific travel style and budget constraints. 

## 4. Objectives
- To build an intelligent system that automates the vacation planning process.
- To demonstrate a multi-agent AI architecture using LLMs.
- To incorporate pure Python logic for deterministic tasks like budget estimation.
- To present a clean, user-friendly interface for seamless interaction.

## 5. Features
- **Personalized Itinerary**: Generates a day-wise plan based on user interests and travel style.
- **Budget Estimation**: Uses a deterministic Python engine to estimate travel costs.
- **AI-driven Validation**: Cross-checks if the requested activities make sense for the destination.
- **Interactive UI**: Built with Gradio Blocks for a clean, intuitive user experience.
- **Error Handling**: Gracefully handles API failures and invalid user inputs.

## 6. AI Agent Workflow
This project implements a multi-stage agent workflow:
1. **Agent 1: Preference Analysis Agent**: Parses raw inputs into a structured traveler profile.
2. **Agent 2: Destination Planning Agent**: Suggests activities and a draft itinerary based on the profile.
3. **Agent 3: Budget Planning Engine**: (Python-based) Estimates costs for accommodation, food, transport, and activities based on heuristics and compares it against the user's budget.
4. **Agent 4: Plan Validation Agent**: Verifies that the destination exists and the activities are suitable (e.g., no beach activities in a landlocked city).
5. **Agent 5: Final Vacation Plan Generator**: Combines the profile, draft itinerary, budget estimate, and validation notes into a beautifully formatted Markdown report.

## 7. System Architecture
```text
[ User Interface (Gradio) ] --> [ Input Validator (Python) ]
                                      |
                                      v
[ Agent 1 (Groq) ] <--> [ Agent 3 (Budget Engine) ] <--> [ Agent 2 (Groq) ]
                                      |
                                      v
                            [ Agent 4 (Validator) ]
                                      |
                                      v
                            [ Agent 5 (Generator) ]
                                      |
                                      v
                         [ Output Display (Gradio) ]
```

## 8. Technology Stack
- **Frontend**: Gradio (Python)
- **Backend**: Python 3.x
- **AI Model**: Groq API
- **Environment Management**: `python-dotenv`

## 9. Project Structure
```text
Intelligent-Vacation-Planning-Assistant/
├── app.py                # Main Gradio application
├── agent.py              # Orchestrates the Groq-powered AI agents
├── budget.py             # Pure Python budget estimation logic
├── validator.py          # Input validation logic
├── prompts.py            # System prompts for all agents
├── config.py             # Environment and configuration loading
├── requirements.txt      # Project dependencies
├── .env.example          # Example environment variables
├── .gitignore            # Git ignored files
├── README.md             # Project documentation
├── assets/               # Static assets like images
├── test_models.py        # Model testing script
├── test_generate.py      # Plan generation testing script
└── tests/
    └── test_app.py       # Unit tests for the application logic
```

## 10. Installation Steps
1. Clone the repository or download the project files.
2. Ensure you have Python installed.
3. Navigate to the project directory:
   ```bash
   cd Intelligent-Vacation-Planning-Assistant
   ```
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## 11. API Key Setup
1. Get a Groq API key from the Groq Console.
2. Rename `.env.example` to `.env`.
3. Add your key to the `.env` file:
   ```env
   GROQ_API_KEY=your_actual_api_key_here
   ```

## 12. How to Run
Run the following command in the terminal:
```bash
python app.py
```
This will launch a local web server (usually at `http://127.0.0.1:7860`). Open this link in your browser to interact with the application.

## 13. Sample Input
- **Starting City**: Nagpur
- **Destination**: Goa
- **Number of Travelers**: 2
- **Number of Days**: 3
- **Total Budget**: 15000
- **Travel Style**: Budget
- **Interests**: Beaches, Food, Nature

## 14. Sample Output
The application generates a full 3-day itinerary focusing on Goa's beaches and seafood, showing an estimated budget breakdown (around 13,200 INR depending on exact heuristics) and declaring whether the user is within budget.

## 15. Screenshots

![App Banner](assets/banner.jpg)

*(Add more screenshots of the Gradio interface and the generated outputs here)*

## 16. Limitations
- Budget estimates use hardcoded heuristics and do not reflect real-time live prices.
- The model's suggestions rely on its training data and not real-time availability.

## 17. Future Scope
- Integration with live hotel/flight APIs (like Skyscanner or Booking.com).
- Support for multi-city itineraries.
- Adding map integration to show locations.

## 18. Disclaimer
Travel costs and recommendations are estimates and should be verified before booking. The system does not make actual reservations.
