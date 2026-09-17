import os
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
API_KEY=os.getenv("GROQ_API_KEY")

if not API_KEY:
    print("Error, no Groq API KEY found in .env file")
    exit()

client=Groq(api_key=API_KEY)

def analyze_text(text):
    response=client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {
                'role':'system',
                'content':""" You are a text analysis assistant.
                Always respond with valid JSON only. No explanation, no markdown, no extra text.
                Return exactly this structure:
                {
                    'sentiment':'positive' or 'negative' or 'neutral',
                    'confidence':a number between 0 or 1,
                    'key_topics': ['topic1','topic2','topic3'],
                    'summary':'one sentence summary'
                }"""
            },
            {
                'role':"user",
                'content':f"analyze this text:{text}"
            }
        ]
    )
    raw= response.choices[0].message.content
    
    try:
        result= json.loads(raw)
        return result
    except json.JSONDecodeError:
        print(f"Model returned invalid JSON:{raw}")
        return None

texts=[
    "I just got my first job offer! The salary is great and the team seems amazing. ",
    "The traffic was terrible today and I missed my important meeting",
    "The weather in Kerala during monsoon is quite heavy with moderate temperatures."
]

for text in texts:
    print(f"\nText: {text}")
    result = analyze_text(text)
    
    if result:
        print(f"Sentiment  : {result['sentiment']}")
        print(f"Confidence : {result['confidence']}")
        print(f"Topics     : {', '.join(result['key_topics'])}")
        print(f"Summary    : {result['summary']}")