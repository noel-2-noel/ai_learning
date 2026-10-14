import os
from groq import Groq
from dotenv import load_dotenv
import chromadb

load_dotenv()
API_KEY=os.getenv("GROQ_API_KEY")

if not API_KEY:
    print("Error no Groq API key found in .env file")

client=Groq(api_key=API_KEY)

chroma_client= chromadb.PersistentClient(path="./chroma_db")

try:
    chroma_client.delete_collection("documents")
except:
    pass

collection=chroma_client.create_collection(name="documents")

def load_and_chunk(filepath,chunk_size=2):
    """Loads a text file and split into chunks of chunk size sentences"""
    with open(filepath,'r') as f:
        content=f.read()
        
    lines=[line.strip() for line in content.split('\n') if line.strip()]
    
    chunks=[]
    for i in range(0,len(lines),chunk_size):
        chunk=' '.join(lines[i:i+chunk_size])
        chunks.append(chunk)
        
    return chunks

chunks=load_and_chunk("Knowledge.txt")
print(f"Loaded {len(chunks)} chunks from  knowledge.txt")

collection.add(
    documents=chunks,
    ids=[f"chunk_{i}" for i in range(len(chunks))]
)

print("chunks added to ChromaDB:")
for i,chunk in enumerate(chunks):
    print(f"chunk_{i}: {chunk[:60]}....")
print()

def retrieve(query,n_results=3):
    results=collection.query(
        query_texts=[query],
        n_results=n_results
    )
    
    documents=[]
    for doc,distance in zip(results['documents'][0],results['distances'][0]):
        if distance<1.3:
            documents.append(doc)
            
    return documents

def generate(query,context_docs):
    if not context_docs:
        return "I don't have enough information to answer that."
        
    context="\n".join([f"={doc}"for doc in context_docs])
    
    response = client.chat.completions.create(
        model='openai/gpt-oss-20b',
        messages=[
            {
                "role": "system",
                "content": """You are a helpful assistant. Answer questions based 
                ONLY on the provided context. Be concise and clear.
                If the context doesn't contain the answer, say so."""
            },
            {
                "role":"user",
                "content":f"Context:\n{context}\n\nQuestion:{query}"
            }
        ]
    )
    return response.choices[0].message.content

def rag(query):
    print(f"Q:{query}")
    docs=retrieve(query)
    answer=generate(query,docs)
    print(f"A:{answer}\n")
    
rag("When was Python created and by whom?")
rag("What is the difference between supervised and unsupervised learning?")
rag("How does RAG reduce hallucination?")
rag("What makes ChromaDB useful for AI applications?")
rag("What is the capital of France?")