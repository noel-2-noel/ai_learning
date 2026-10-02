import os
import json
from groq import Groq
from dotenv import load_dotenv
import chromadb

load_dotenv()
API_KEY=os.getenv("GROQ_API_KEY")

if not API_KEY:
    print("Error no GROQ API KEY found in .env file")
    exit()

client=Groq(api_key=API_KEY)

chroma_client=chromadb.PersistentClient(path="./chroma_db")
collection=chroma_client.get_or_create_collection(name='knowledge_base')

count=collection.count()
print(f"Documents in Database:{count}\n")

def retrieve(query,n_results=2):
    """Step 1 -Retrieve relevant documents from ChromaDB"""
    results = collection.query(
        query_texts=[query],
        n_results=n_results
    )
    print(f"Distance: {results['distances'][0]}")
    
    
    documents=[]
    for doc,distance in zip(results['documents'][0],results['distances'][0]):
        if distance<1.2:
            documents.append(doc)
    return documents

def generate(query,context_docs):
    """Step 2 -Generate answer using LLM with retrieved context"""
    
    if not context_docs:
        return "I don't have enough information in my knowledge base to answer that."
    
    context ="\n".join([f"- {doc}" for doc in context_docs])
    
    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {
                'role':'system',
                'content':"""You are a helpful assistant that answers questions
                based ONLY on the provided context.
                If the context doesn't contain enough information,say so clearly.
                Do not make up information beyond what is in the context."""
            },
            {
                'role':'user',
                'content':f"""Context:{context}
                Question:{query}
                Answer based only on the context above:"""
            }
        ]
    )
    
    return response.choices[0].message.content

def rag(query):
    """Complete RAG pipeline - retrieve then generate"""
    print(f"QUestion:{query}")
    
    docs=retrieve(query)
    
    if docs:
        print(f'Retrieved {len(docs)} relevant documents(s):')
        for doc in docs:
            print(f" ->{doc}")
    else:
        print("No relevant documents found above threshold")
    
    answer= generate(query,docs)
    print(f"\nAnswer :{answer}\n")
    print("-"*50 +"\n")
    
    return answer

questions =[
    "what is RAG?",
    "Tell me about Python",
    "What is Kerala known for?",
    "Who is the president of India?"
]

for question in questions:
    rag(question)