## 📌What is it !

AI-powered weather agent backend built using OpenAI lightweight agents
Chainlit chatbot frontend for real-time conversation
LLM-based system that fetches, processes, and explains weather data

## ⚙️ Tech Stack

Python (>=3.13)
OpenAI Agents SDK
Chainlit (chatbot UI)
UV (dependency & environment manager)

## 📦 Installation (UV based)
Install UV (if not already installed):
pip install uv
Clone the project:

`git clone <your-repo-url>`

`cd weather-agent-system`

Install dependencies (auto via UV):

`uv sync`

## 🔑 Environment Setup

Create a `.env` file:

OPENAI_API_KEY=your_api_key_here
WEATHER_API_KEY = your weather api key 

## 📦 UV environment create + activate

`uv venv`

🟢 Environment activate (Windows)

`.\.venv\Scripts\activate`

🟢 Environment activate (Mac / Linux)

`source .venv/bin/activate`

## 🚀 Run Project

Start Chainlit chatbot:
`uv run chainlit run main.py`