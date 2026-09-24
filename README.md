# AI Learning Journey — 90 Day Plan

Building toward an AI Apps developer role through daily hands-on projects.

## Week 1 — Python + APIs Foundation

- **joke_api.py** — Fetches random jokes from public API, saves to JSON
- **query_parameters.py** — University search using query parameters
- **weather.py** — Live weather for 3 Kerala cities using OpenWeatherMap API
- **news.py** — News aggregator by topic using GNews API

## Week 2 — LLM APIs with Groq

- **llm_basic.py** — First LLM API call, understanding request/response structure
- **chat_loop.py** — Conversational chat with full history memory
- **structured_output.py** — Forcing LLM to return structured JSON for programmatic use
- **persona_chat.py** — Same LLM, 3 completely different personas via system prompts
- **study_assistant.py** — Full mini AI assistant combining all Week 2 concepts

## What I'm Building Toward

A deployed RAG application — an AI assistant that answers questions from any document,
with a public URL, built entirely from scratch.

## Setup

1. Clone the repo
2. Create virtual environment: `python -m venv venv`
3. Activate: `venv\Scripts\activate` (Windows) or `source venv/bin/activate` (Mac/Linux)
4. Install dependencies: `pip install -r requirements.txt`
5. Create `.env` file:
    GROQ_API_KEY=your_groq_key_here
    WEATHER_API_KEY=your_openweathermap_key_here
    GNEWS_API_KEY=your_gnews_key_here
6. Run any script: `python study_assistant.py`

## Tech Stack
- Python, Groq API, LLM (openai/gpt-oss-20b)
- requests, python-dotenv, groq

## Progress
- [x] Week 1 — Python + APIs
- [x] Week 2 — LLM APIs
- [ ] Week 3 — Embeddings + Vector Databases
- [ ] Week 4 — RAG Pipeline
- [ ] Month 2 — Deploy RAG App