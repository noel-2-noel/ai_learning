import requests
import os
import json
from dotenv import load_dotenv

load_dotenv()
API_KEY =os.getenv("Weather_api_key")

if not API_KEY:
    print("Error: WEATHER API KEY not found in .env file")
    exit

def get_weather(city):
    url="https://api.openweathermap.org/data/2.5/weather"
    
    params={
        "q":city,
        'appid':API_KEY,
        'units':'metric
    }
    
    try:
        response=requests.get(url,params=params,timeout=10)
        response.raise_for_status()
        
        data=response.json()
        
        
        weather={
            'city':data['name'],
            'temperature':data['main']['temp'],
            'feels_like':data['main']['feels_like'],
            'description':data['weather'][0]['description'],
            'humidity':data['main']['humidity']
        }
        
        print(f"\n Weather in {weather['city']}:")
        print(f" Temp  : {weather['temperature']} feels like {weather['feels_like']}")
        print(f" Condition : {weather['description'].capitalize()}")
        print(f" Humidity : {weather['humidity']}%")
        
        return weather
    except requests.exceptions.Timeout:
        print("Request timed out")
    except requests.exceptions.HTTPError as e:
        if response.status_code ==401:
            print(" Invalid api key - check .env file ")
        elif response.status_code ==404:
            print(f"City '{city}' not found -check spelling")
        else:
            print(f"HTTP error :{e}")
    except Exception as e:
        print(f"Something went wrong: {e}")
        import traceback
        traceback.print_exc()

cities=['kochi','thrissur','kottayam']

results=[]
for city in cities:
    data=get_weather(city)
    if data:
        results.append(data)

with open("weather_report.json",'w') as f:
    json.dump(results,f,indent=2)

print(f"\n Saved weather for  {len(results)} cities to weather_report.json")