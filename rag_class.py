import os
from groq import Groq
from dotenv import load_dotenv
import chromadb

load_dotenv()

class RAGSystem:
    """
    A reusable RAG system that can be intialized with any document
    and queried with natural language questions."""
    
    def __init__(self,collection_name,groq_api_key,db_path="./chroma_db"):
        """Initialize the RAG system with a collection name and API key"""
        
        self.client=Groq(api_key=groq_api_key)
        self.model="openai/gpt-oss-20b"
        
        self.chroma_client=chromadb.PersistentClient(path=db_path)
        
        self.collection=self.chroma_client.get_or_create_collection(name=collection_name)
        print(f"RAG System initialized - collection:'{collection_name}'")
        print(f'Documents in collection: {self.collection.count()}\n')
        
    def load_file(self,filepath,chunk_size=2):
        """Load a text file and add it to the vector database"""
        
        with open(filepath,'r') as f:
            content=f.read()
            
        lines=[line.strip() for line in content.split('\n') if line.strip()]
        
        chunks=[]
        for i in range(0,len(lines),chunk_size):
            chunk=' '.join(lines[i:i+chunk_size])
            chunks.append(chunk)
            
        existing_count=self.collection.count()
        self.collection.add(
            documents=chunks,
            ids=[f"chunk_{existing_count+i}" for i in range(len(chunks))]
        )
        
        print(f"Loaded '{filepath}'- added{len(chunks)} chunks")
        print(f"Total documents in collection: {self.collection.count()}\n")
        return chunks

    def retrieve(self,query,n_results=3,distance_threshold=1.3):
        """Retrieve relevant chunks from ChromaDB"""
        
        results=self.collection.query(
            query_texts=[query],
            n_results=n_results
        )
        
        documents=[]
        for doc,distance in zip(results['documents'][0],results['distances'][0]):
            if distance<distance_threshold:
                documents.append(doc)
                
        return documents
    
    def generate(self,query,context_docs):
        """Generate answer using Groq LLM with retrieved context"""
        
        if not context_docs:
            return "I don't have enough information in my knowledge base to answer that."
        
        context="\n".join([f"-{doc}"for doc in context_docs])
        
        response=self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    'role':'system',
                    'content':"""You are a helpful assistant.ANswer questions based ONLY on the provided context Be concise and clear.
                    If the context doesn't contain the answer,say so clearly."""
                },
                {
                    'role':'user',
                    'content':f"Context:\n{context}\n\nQuestion:{query}"
                }
            ]
        )
        
        return response.choices[0].message.content
    
    def ask(self,query):
        """Main method - retrieve relevant docs and generate answer"""
        
        docs=self.retrieve(query)
        answer=self.generate(query,docs)
        
        return{
            "question":query,
            "sources":docs,
            "answer":answer
        }
        
    def clear(self):
        """Clear all documents from the collection"""
        
        self.chroma_client.delete_collection(self.collection.name)
        self.collection=self.chroma_client.create_collection(
            name=self.collection.name
        )
        print("Collection cleared.\n")
        
if __name__=="__main__":
    
    API_KEY=os.getenv("GROQ_API_KEY")
    if not API_KEY:
        print("Error:GROQ_API_KEY not found")
        exit()
        
    rag=RAGSystem(
        collection_name="rag_classs_test",
        groq_api_key=API_KEY
    )
    
    rag.clear()
    rag.load_file("Knowledge.txt",chunk_size=2)
    
    questions=[
        "Who created Python and when?",
        "what is the difference between supervised and unsupervised learning?",
        "How does RAG reduce hallucination?",
        "What is the weather like today?"
    ]
    
    for question in questions:
        result=rag.ask(question)
        print(f"Q:{result['question']}")
        print(f"A:{result['answer']}")
        print(f"Sources used:{len(result['sources'])}")
        print("-"*50)