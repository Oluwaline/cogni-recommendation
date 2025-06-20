# cogni-recommendation


# 🧠 Cogni Recommendation System

This project intelligently recommends the most suitable Cogni mental health support package based on organizational inputs using FastAPI, Streamlit, and a low-code chatbot powered by Microsoft Copilot Studio.

## 🚀 What It Does

- Collects assessment data from organizations (e.g., service model, team size, timeline)
- Calls a FastAPI endpoint that runs a rule-based or ML model to determine the best-fit Cogni package
- Returns the recommended package tier, number of seats, pricing, and next steps
- Renders a user-facing proposal via Streamlit with query parameters
- Integrates with a Copilot chatbot to streamline conversations and automate recommendations

## 🛠️ Tech Stack

- **FastAPI** – RESTful backend to process recommendations
- **Streamlit** – UI layer for displaying recommendations and proposal follow-ups
- **Copilot Studio** – Conversational interface for collecting assessment data and invoking the API
- **Python + Pandas** – Core logic for decision making and data handling
- **Git + GitHub** – Version control and deployment base

## 📁 Folder Structure
cogni_recommendation_system/ ├── app.py # Streamlit frontend ├── cogni_api.py # FastAPI backend ├── cognii.ipynb # Jupyter logic notebook ├── requirements.txt # Dependency list └── cogni_synthetic_training.csv # Sample data (if applicable)


## ⚙️ How to Run Locally

1. Clone this repo and navigate to the project folder:

   ```bash
   git clone https://github.com/Oluwaline/cogni-recommendation.git
   cd cogni-recommendation


Copilot Studio Integration
The chatbot collects user responses, stores them in global variables, then calls the GetRecommendation plugin (which maps to the FastAPI tool). It dynamically renders the response and optionally deep-links to the Streamlit app.

💡 Future Improvements
Add a machine learning layer for scoring and ranking packages

Enable persistent storage of assessments

Build a hosted dashboard for analytics
