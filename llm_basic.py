import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("GROQ_API_KEY")

if not API_KEY:
    print("ERROR: GROQ_API_KEY not found in .env file")
    exit()

client= Groq(api_key=API_KEY)

response= client.chat.completions.create(
    model='openai/gpt-oss-20b',
    messages=[
        {
            'role':'user',
            'content':"Explain what is REST API in 3 sentences, like I'm a beginner"
        }
    ]
)

print(response.choices[0].message.content)