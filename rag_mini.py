#1. load env,groq client
import os
from dotenv import load_dotenv
from groq import Groq
load_dotenv()
API_KEY=os.getenv("GROQ_API_KEY")

if not API_KEY:
    print("GROQ_API_KEY not found in .env file")
    exit()

client=Groq(api_key=API_KEY)
#2.create chromadb collection
import chromadb
chroma_client=chromadb.PersistentClient(path="./chroma_db")

try:
    chroma_client.delete_collection("knowledge1_base")
    print("old collection deleted")
    
except Exception:
    print("Collection does not exist yet")

collection=chroma_client.get_or_create_collection(name="knowledge1_base")

#3.take a text,split into chunks
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

chunks=load_and_chunk("knowledge.txt")
print(f"Loaded {len(chunks)} chunks from  knowledge.txt")
    
# 4. add chunks to the collection
collection.add(
    documents=chunks,
    ids=[f"chunk{i}"for i in range(len(chunks))]
)
print(collection.count())


#5. query with a question, get top chunks
def retrieve(query,n_results=2):
    results=collection.query(
        query_texts=[query],
        n_results=n_results
    )
    
    print(f"Distance:{results['distances'][0]}")
    
    documents=[]
    for doc,distance in zip(results['documents'][0],results['distances'][0]):
        if distance<1.3:
            documents.append(doc)
    return documents

# 6. send chunks + question to the LLM, print the answer
def generate(query,context_docs):
    
    if not context_docs:
        return "I don't have information in my knowledge base to answer that."
    
    context="\n".join([f"-{doc}" for doc in context_docs])
    
    response=client.chat.completions.create(
        model='openai/gpt-oss-20b',
        messages=[
            {'role':'system',
            'content':"""You are a helpful assistant that answers questions
                based ONLY on the provided context.
                If the context doesn't contain enough information,say so clearly.
                Do not make up information beyond what is in the context."""
            },
            {
               'role':'user',
               'content':f"""Context:{context}
               question:{query}
               answer based on the context above:""" 
            }
        ]
    )
    return response.choices[0].message.content


def rag(query):
    docs=retrieve(query)
    answer=generate(query,docs)
    return answer,docs

while True:
    user_input=input("Ask a question(or quit)").strip()
    
    if not user_input:
        continue
    
    if user_input.lower()=='quit':
        print("Goodbye!")
        break
    
    answer,docs=rag(user_input)
    
    print(f"\nA:{answer}")
    
    if docs:
        print("\nSources")
        for i,doc in enumerate(docs,start=1):
            print(f"{i}.{doc}")
    print()
'''
rag("When was Python created and by whom?")
rag("What is the difference between supervised and unsupervised learning?")
rag("How does RAG reduce hallucination?")
rag("What makes ChromaDB useful for AI applications?")
rag("What is the capital of France?")'''