import gradio as gr
import time
import os
from validator import validate_inputs
from agent import generate_plan

css = """
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

:root {
    --bg: #C7DAFF;
    --primary: #2563EB;
    --accent: #06B6D4;
    --text-main: #0F172A;
    --text-sec: #64748B;
    --white: #FFFFFF;
    --border: #E2E8F0;
}

body {
    background-color: var(--bg) !important;
    font-family: 'Inter', sans-serif !important;
    color: var(--text-main);
}

.gradio-container {
    max-width: 1100px !important;
    margin-left: auto !important;
    margin-right: auto !important;
    background-color: transparent !important;
    border: none !important;
    padding-top: 1rem !important;
}

/* Force Gradio inner wrappers to be transparent/same color */
gradio-app, .gradio-container > div, .gradio-container .main, .gradio-container .wrap {
    background-color: transparent !important;
}

/* Header */
.app-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1rem 1.5rem;
    background: var(--white);
    border-radius: 12px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    margin-bottom: 2rem;
    font-weight: 600;
    color: var(--text-main);
    border: 1px solid var(--border);
}
.app-header span {
    color: var(--text-sec);
    font-weight: 400;
    font-size: 0.9rem;
}

/* Hero Section */
.hero-section {
    align-items: center;
    padding-bottom: 3rem !important;
}
.hero-left {
    padding-right: 2rem;
}
.hero-badge {
    display: inline-block;
    background: rgba(37, 99, 235, 0.1);
    color: var(--primary);
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 0.05em;
    margin-bottom: 1.25rem;
}
.hero-title {
    font-size: 3rem;
    font-weight: 700;
    line-height: 1.15;
    color: var(--text-main);
    margin-bottom: 1rem;
}
.hero-subtitle {
    font-size: 1.1rem;
    color: var(--text-sec);
    line-height: 1.5;
    margin-bottom: 0.75rem;
    font-weight: 500;
}
.hero-subtext {
    font-size: 0.9rem;
    color: #94a3b8;
}
.hero-img {
    border-radius: 20px;
    box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 8px 10px -6px rgba(0, 0, 0, 0.1);
    object-fit: cover;
    max-height: 350px !important;
    width: 100%;
}

/* Floating Planner Card */
.planner-card {
    background: var(--white) !important;
    border-radius: 24px !important;
    padding: 2.5rem !important;
    box-shadow: 0 10px 40px -10px rgba(0,0,0,0.08) !important;
    border: 1px solid rgba(0,0,0,0.04) !important;
    margin-top: -2.5rem !important; /* Floating effect */
    position: relative;
    z-index: 10;
}
.card-title {
    font-size: 1.5rem;
    font-weight: 600;
    margin-bottom: 0.25rem;
    color: var(--text-main);
}
.card-subtitle {
    color: var(--text-sec);
    margin-bottom: 2rem;
    font-size: 0.95rem;
}

/* Inputs & Labels */
.form-label, label {
    color: var(--text-main) !important;
    font-weight: 500 !important;
    font-size: 0.9rem !important;
}
.input-info {
    color: var(--text-sec) !important;
    font-size: 0.8rem !important;
}
input[type="text"], input[type="number"], textarea, .dropdown-container, .wrap, .checkbox-group {
    background: var(--white) !important;
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
    color: var(--text-main) !important;
    box-shadow: 0 1px 2px rgba(0,0,0,0.02) !important;
}
input[type="text"]:focus, input[type="number"]:focus, .dropdown-container:focus-within {
    border-color: var(--primary) !important;
    box-shadow: 0 0 0 3px rgba(37,99,235,0.1) !important;
}

/* Buttons */
.generate-btn {
    background: linear-gradient(135deg, var(--primary) 0%, var(--accent) 100%) !important;
    border: none !important;
    color: var(--white) !important;
    font-size: 1.1rem !important;
    font-weight: 600 !important;
    border-radius: 12px !important;
    padding: 0.75rem 0 !important;
    width: 100% !important;
    margin-top: 1.5rem !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 4px 12px rgba(37, 99, 235, 0.2) !important;
}
.generate-btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 20px rgba(37, 99, 235, 0.3) !important;
}
.btn-subtext {
    text-align: center;
    color: var(--text-sec);
    font-size: 0.85rem;
    margin-top: 0.75rem;
    margin-bottom: 1.5rem;
}
.clear-btn {
    background: transparent !important;
    border: 1px solid var(--border) !important;
    color: var(--text-sec) !important;
    border-radius: 8px !important;
    font-weight: 500 !important;
    padding: 0.4rem 1.25rem !important;
    margin: 0 auto !important;
    display: block !important;
    width: 150px !important;
    transition: all 0.2s;
}
.clear-btn:hover {
    background: var(--bg) !important;
    color: var(--text-main) !important;
}

/* Output Section */
.output-section {
    margin-top: 3.5rem !important;
}
.output-heading {
    font-size: 1.75rem;
    font-weight: 600;
    text-align: center;
    margin-bottom: 1.5rem;
    color: var(--text-main);
}
.output-card {
    background: var(--white) !important;
    border-radius: 20px !important;
    padding: 2.5rem !important;
    box-shadow: 0 4px 20px rgba(0,0,0,0.03) !important;
    border: 1px solid var(--border) !important;
    color: var(--text-main) !important;
    line-height: 1.7;
}

/* Markdown Styling for Output */
.output-card h1, .output-card h2 {
    color: var(--primary);
    border-bottom: 1px solid var(--border);
    padding-bottom: 0.5rem;
    margin-top: 2rem;
    margin-bottom: 1rem;
    font-weight: 600;
}
.output-card h1 { font-size: 1.8rem; margin-top: 0; }
.output-card h2 { font-size: 1.4rem; }
.output-card h3 {
    color: var(--text-main);
    font-weight: 600;
    font-size: 1.15rem;
    margin-top: 1.5rem;
    margin-bottom: 0.5rem;
}
.output-card ul, .output-card ol {
    background: var(--bg);
    padding: 1.5rem 1.5rem 1.5rem 3rem;
    border-radius: 12px;
    border: 1px solid var(--border);
    margin: 1rem 0;
}
.output-card strong {
    color: var(--text-main);
    font-weight: 600;
}

/* Footer */
.footer {
    text-align: center;
    padding: 2rem;
    color: var(--text-sec);
    font-size: 0.85rem;
    margin-top: 3rem;
}
"""

def generate_plan_with_progress(start_city, destination, travelers, days, budget_val, travel_style, interests, progress=gr.Progress()):
    progress(0.1, desc="✈️ Planning your perfect getaway...")
    
    is_valid, error_msg = validate_inputs(start_city, destination, travelers, days, budget_val, interests)
    if not is_valid:
        return f"<div class='output-card'>\n\n## ❌ Validation Error\n**{error_msg}**\n\n</div>"
    
    progress(0.3, desc="🔍 Analyzing your preferences...")
    time.sleep(0.5)
    progress(0.5, desc="🗺️ Building your itinerary...")
    time.sleep(0.5)
    progress(0.7, desc="💰 Optimizing your budget...")
    time.sleep(0.5)
    progress(0.9, desc="✨ Finalizing your vacation plan...")
    
    try:
        final_plan = generate_plan(
            start_city=start_city,
            destination=destination,
            travelers=int(travelers),
            days=int(days),
            user_budget=float(budget_val),
            travel_style=travel_style,
            interests=interests
        )
        return final_plan
    except Exception as e:
        return f"<div class='output-card'>\n\n## ⚠️ System Error\nAn unexpected error occurred: {str(e)}\n\n</div>"

def clear_inputs():
    return "", "", 2, 3, 30000, "Budget", ["beaches", "food", "sightseeing"], ""

banner_path = os.path.join(os.path.dirname(__file__), "assets", "banner.jpg")

theme = gr.themes.Base(
    primary_hue="blue",
    neutral_hue="slate"
)

with gr.Blocks(title="Intelligent Vacation Planning Assistant") as app:
    
    # Navigation / Header
    gr.HTML("""
    <div class='app-header'>
        <div>✈️ Intelligent Vacation Planner</div>
        <span>AI Travel Assistant</span>
    </div>
    """)
    
    # Hero Section
    with gr.Row(elem_classes="hero-section"):
        with gr.Column(scale=1, elem_classes="hero-left"):
            gr.HTML("""
                <div class='hero-badge'>✦ AI-POWERED TRAVEL PLANNER</div>
                <div class='hero-title'>Plan Your Perfect<br/>Getaway ✈️</div>
                <div class='hero-subtitle'>Personalized itineraries, smart budgets, and unforgettable experiences — all planned by AI.</div>
                <div class='hero-subtext'>Tell us where you're going. We'll handle the planning.</div>
            """)
        with gr.Column(scale=1):
            if os.path.exists(banner_path):
                gr.Image(value=banner_path, elem_classes="hero-img", show_label=False, interactive=False, container=False)

    # Main Trip Planner Card
    with gr.Column(elem_classes="planner-card"):
        gr.HTML("""
        <div class='card-title'>Plan Your Trip</div>
        <div class='card-subtitle'>Customize your journey to match your style and budget.</div>
        """)
        
        with gr.Row():
            with gr.Column(scale=1):
                start_city = gr.Textbox(label="Starting City", placeholder="e.g. Nagpur", info="Where are you travelling from?")
            with gr.Column(scale=1):
                destination = gr.Textbox(label="Destination", placeholder="e.g. Goa", info="Where do you want to go?")
                
        with gr.Row():
            with gr.Column(scale=1):
                travelers = gr.Number(label="Travelers", minimum=1, value=2, precision=0)
            with gr.Column(scale=1):
                days = gr.Slider(label="Duration (Days)", minimum=1, maximum=15, step=1, value=3)
                
        with gr.Row():
            with gr.Column(scale=1):
                budget_val = gr.Number(label="Total Budget (INR)", value=30000, minimum=0, placeholder="e.g. ₹30,000")
            with gr.Column(scale=1):
                travel_style = gr.Dropdown(
                    choices=["Budget", "Moderate", "Luxury", "Adventure"], 
                    label="Travel Style", 
                    value="Budget"
                )
                
        interests = gr.CheckboxGroup(
            choices=["nature", "beaches", "food", "adventure", "history", "culture", "shopping", "nightlife", "sightseeing", "photography"],
            label="Interests",
            value=["beaches", "food", "sightseeing"]
        )
        
        generate_btn = gr.Button("✨ Generate My Vacation Plan", elem_classes="generate-btn")
        gr.HTML("<div class='btn-subtext'>AI will analyze your preferences and create a personalized itinerary.</div>")
        
        clear_btn = gr.Button("↻ Start Over", elem_classes="clear-btn")

    # Output Section
    with gr.Column(elem_classes="output-section"):
        gr.HTML("<div class='output-heading'>Your Trip Awaits 🌍</div>")
        output_box = gr.Markdown(
            "Fill out the details above and click Generate to see your beautiful AI-crafted itinerary.",
            elem_classes="output-card"
        )

    # Footer
    gr.HTML("""
    <div class='footer'>
        <strong>Intelligent Vacation Planning Assistant</strong><br/>
        AI & Automation • Gradio • Python
    </div>
    """)

    # Event Bindings
    generate_btn.click(
        fn=generate_plan_with_progress,
        inputs=[start_city, destination, travelers, days, budget_val, travel_style, interests],
        outputs=output_box,
        api_name="generate"
    )
    
    clear_btn.click(
        fn=clear_inputs,
        inputs=[],
        outputs=[start_city, destination, travelers, days, budget_val, travel_style, interests, output_box]
    )

if __name__ == "__main__":
    app.launch(
        server_name="0.0.0.0",
        server_port=int(os.environ.get("PORT", 7860)),
        theme=theme,
        css=css
    )
