import chromadb
from sentence_transformers import SentenceTransformer

model=SentenceTransformer('all-MiniLM-L6-v2')

client=chromadb.PersistentClient(path="./chroma_db")

collection = client.get_or_create_collection(name="knowledge_base")

documents = [
    "Python is a high-level programming language known for its simplicity.",
    "Machine learning is a subset of AI that learns patterns from data.",
    "ChromaDB is a vector database for storing and searching embeddings.",
    "RAG stands for Retrieval Augmented Generation.",
    "Large language models are trained on massive amounts of text data.",
    "Kerala is a state in South India known for its backwaters and coconuts.",
    "Embeddings convert text into numerical vectors that capture meaning.",
    "Groq is a platform that provides fast LLM inference via API."
]

collection.add(
    documents=documents,
    ids=[f"doc_{i}" for i in range(len(documents))]
)

print(f"Added {len(documents)} documents to chromadb\n")

queries =  [
    "How does retrieval augmented generation work?",
    "Tell me about Python programming",
    "What is Kerala famous for?"
]

for query in queries:
    print(f"Query :'{query}'")
    
    results=collection.query(
        query_texts=[query],
        n_results=2
    )
    
    print("Top matches:")
    for i,doc in enumerate(results['documents'][0]):
        distance = results['distances'][0][i]
        print(f"  {i+1}. {doc}")
        print(f"     Distance: {distance:.4f} (lower = more similar)")
    print()