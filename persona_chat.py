import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
API_KEY=os.getenv("GROQ_API_KEY")

if not API_KEY:
    print("ERROR!..GROQ_API_KEY not found in the .env file")
    exit()

client=Groq(api_key=API_KEY)

personas = {
    "1":{
        "Name":"Kerala Uncle",
        "prompt":""" You are a friendly Malayalam uncle from kerala. You give advices in warm,slightly dramatic way mixing English with 
        Malayalam words.You always relate everything with rice,coconut, or family values.Keep responses short - 3 to 4 sentences max."""
    },

    "2":{
        "Name":"Strict CS Professor",
        "prompt":""""You are a strict computer science professor with 20 years of experience.
        You give technically precise answers with no fluff.
        You correct Bad Terminology immediatley.
        You end every response with follow-up question to test the student."""
    },
    
    "3":{
        "Name":"Startup Bro",
        "prompt":"""You are an overenthusiastic startup founder.
        You speak in startup jagron - disrupt, pivot, scale, synergy, MVP.
        You relate everything to building products and raising funding.
        You are extremely optimistic about everything."""
    }
}

print("choose your assistant:")
for key,persona in personas.items():
    print(f" {key}.{persona['Name']}")
    
choice=input("Enter 1, 2, or 3: ")

if choice not in personas:
    print("Invalid choice")
    exit()

selected=personas[choice]
print(f"chatting with {selected["Name"]}")
print("Type 'quit' to exit\n")

messages=[
    {
        "role":'system',
        'content':selected["prompt"]
    }
]

while True:
    user_input = input("You: ")
    if user_input.lower()=='quit':
        print("Goodbye")
        break
    
    messages.append({
        "role":"user",
        'content':user_input
    })

    response=client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=messages
    )
    
    reply=response.choices[0].message.content
    
    messages.append({
        'role':'assistant',
        'content':reply
    })
    print(f"\n{selected['Name']}:{reply}\n")