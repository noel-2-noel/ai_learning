import os
import json
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
API_KEY=os.getenv("GROQ_API_KEY")

if not API_KEY:
    print("ERROR!, There is no GROQ_API_KEY in .env file")
    exit()

client=Groq(api_key=API_KEY)

SYSTEM_PROMPT="""You are a focused study assistant helping a CS fresher learn AI and Python concepts.
Your Rules:
1. Give clear and concise explanation (max 5 sentences)
2. Use simple Analogies when explaining complex topics
3. If the user seems confused, break it down further
4. Stay on topic, only answer AI, Python and CS related questions
5. If asked something unrelated, politely redirect back to studying"""

messages=[
    {
        'role':'system',
        'content':SYSTEM_PROMPT
    }
]

conversation_topics=[]

print("=" * 50)
print("     Personalised Study Assistant")
print("=" * 50)
print()

while True:
    user_input=input("You: ").strip()
    
    if not user_input:
        continue
    
    if user_input.lower()=='quit':
        break
    
    conversation_topics.append(user_input)
    
    messages.append(
        {
            'role':'user',
            'content':user_input
        }
    )
    response=client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=messages
    )
    
    reply=response.choices[0].message.content
    
    messages.append(
        {
            'role':'assistant',
            'content':reply
        }
    )
    
    print(f"\nAssistant: {reply}\n")

print("\n Generating your session summary...\n")

summary_response=client.chat.completions.create(
    model="openai/gpt-oss-20b",
    messages=[
    {
        'role':'system',
        'content':"""You are a study session analyzer.
        Return only valid JSON, no markdown, no extra text.
        use exactly this structure:
        {
            "topics_covered":['topic1,topic2],
            'concepts_learned:['concept1,concept2],
            'recommended_next_topics:['topic1','topic2'],
            'session_rating':'a rating out of 10 based on depth of the question asked',
            'encouragement':'one motivating sentence for the student'
        }"""
    },
    {
        'role':'user',
        'content':f"Analyze this study session. QUestion Asked:{conversation_topics}"
    }
    ]
)

raw_summary=summary_response.choices[0].message.content

try:
    summary = json.loads(raw_summary)
    
    print('='*50)
    print("  Session Summary")
    print('='*50)
    print(f"Topics convered     :{', '.join(summary['topics_covered'])}")
    print(f"Concepts Learned   : {', '.join(summary['concepts_learned'])}")
    print(f"Next Topics        : {', '.join(summary['recommended_next_topics'])}")
    print(f"Session Rating     : {summary['session_rating']}")
    print(f"Note               : {summary['encouragement']}")
    
    with open("study_session.json","w") as f:
        json.dump(summary,f,indent=2)
    print("\nSummary saved to study_session.json")

except json.JSONDecodeError:
    print("Could not parse summary.")
    print(raw_summary)
