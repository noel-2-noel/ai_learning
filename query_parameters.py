import requests,json
def search_university(country):
    url="http://universities.hipolabs.com/search"
    
    params={
        "country":country
    }
    try:
        response=requests.get(url,params=params,timeout=10)
        response.raise_for_status()
        
        universities=response.json()
        if not universities:
            print(f"No universities found for {country}. pls check the spelling or try another country")
            return[]
        
        print(f"Found {len(universities)} universities in {country}")
        
        top_5=universities[:5]
        with open("universities.json","w") as f:
            json.dump(top_5,f,indent=2)
        return top_5
    except requests.exceptions.Timeout:
        print("Request timed out — try again")
    except requests.exceptions.HTTPError as e:
        print(f"HTTP error: {e}")
    except Exception as e:
        print(f"Something went wrong: {e}")
name=input("enter the country to be searched\t")
results=search_university(name)
for uni in results:
    print(f"{uni['name']} -->{uni['web_pages']}")