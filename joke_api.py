import requests,json
def get_joke():
    url="https://official-joke-api.appspot.com/random_joke"
    
    try:

        response= requests.get(url,timeout=5)

        response.raise_for_status()
        
        data = response.json()
        print(f"Setup: {data['setup']}")
        print(f"Punchline: {data['punchline']}")
        
        with open("jokes.json",'a') as f:
            json.dump(data,f)
            f.write('\n')
        
        
        return data
    except requests.exceptions.Timeout:
        print("Request timed out")
    except requests.exceptions.HTTPError as e:
        print(f"HTTP error: {e}")
    except Exception as e:
        print(f"Something went wrong: {e}")
for i in range(3):
    get_joke()
    