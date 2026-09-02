# AI Learning — Week 1

Python + APIs foundation built as part of my 90-day AI learning plan.

## Projects

- **joke_api.py** — Fetches 3 random jokes from a public API and saves to jokes.json
- **query_parameters.py** — Searches universities by country using query parameters
- **weather.py** — Gets live weather for 3 Kerala cities using OpenWeatherMap API
- **news.py** — Searches top 5 news articles by topic using GNews API, saves to news_results.json

## Setup

1. Clone the repo
2. Create a virtual environment: `python -m venv venv`
3. Activate it: `venv\Scripts\activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Create a `.env` file with your API key:
WEATHER_API_KEY=your_openweathermap_api_key_here
6. Run any script: `python weather.py`

## What I learned
- Virtual environments and dependency management
- Making API calls with the requests library
- Handling query parameters and API keys
- Saving and loading JSON data
- Securing secrets with .env files