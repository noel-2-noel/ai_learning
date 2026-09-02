import requests
import os
import json
from dotenv import load_dotenv

load_dotenv()
API_KEY=os.getenv('news_api_key')

if not API_KEY:
    print("Error News cannot be fetched ")
    exit()

def get_news(news):
    url="https://gnews.io/api/v4/search"
    
    params={
        "q":news,
        "token":API_KEY,
        "lang":"en",
        "max":5
    }
    
    try:
        response=requests.get(url,params=params,timeout=10)
        response.raise_for_status()
        
        data=response.json()
        
        articles = data['articles']
        results = []

        for article in articles:
            item = {
          'title': article['title'],
          'source': article['source']['name'],
          'url': article['url']
            }
            print(f"\nTitle: {item['title']}")
            print(f"Source: {item['source']}")
            print(f"Link: {item['url']}")
            results.append(item)

        return results
    except requests.exceptions.Timeout:
        print("Request timed out")
    except requests.exceptions.HTTPError as e:
        if response.status_code ==401:
            print(" Invalid api key - check .env file ")
        elif response.status_code ==404:
            print(f"News '{news}' not found -check spelling")
        else:
            print(f"HTTP error :{e}")
    except Exception as e:
        print(f"Something went wrong: {e}")
        import traceback
        traceback.print_exc()
news=input("enter topic for the news to be searched for:")
results=get_news(news)
with open("news_results.json",'w') as f:
    json.dump(results,f,indent=2)