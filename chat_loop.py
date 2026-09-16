import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
API_KEY=os.getenv('GROQ_API_KEY') 

if not API_KEY:
    print("Error, Groq API KEY Not found in .env file")
    exit()

client=Groq(api_key=API_KEY)

messages =[
    {
        'role':'system',
        'content':"You are a helpful assistant, keep your answers concise and clear"
    }
]

print("Chat started. Type 'quit' to exit.\n")

while True:
    user_input=input("You: ")
    
    if user_input.lower()=='quit':
        print('Goodbye')
        break
    messages.append(
        {
            'role':'user',
            'content':user_input
        }
    )
    
    response=client.chat.completions.create(
        model='openai/gpt-oss-20b',
        messages=messages
    )
    
    reply=response.choices[0].message.content
    
    messages.append(
        {
            'role':'assistant',
            'content':reply
        }
    )
    print(f"\nAssistant:{reply}\n")
    