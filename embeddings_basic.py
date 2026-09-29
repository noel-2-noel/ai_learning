import os
from sentence_transformers import SentenceTransformer
from dotenv import  load_dotenv

load_dotenv()

model= SentenceTransformer('all-MiniLM-L6-v2')

sentences =[
    "Python is a programming language",
    "Python is used for machine learning",
    "Cats are cute animals",
    "Dogs are loyal pets",
    "Neural networks learn from data"
]

print(f"Generating Embeddings...\n")

embeddings = model.encode(sentences)

print(f"Number of sentences:{len(sentences)}")
print(f"Embedding shape :{embeddings.shape}")
print(f"Each sentence becomes a vector of {embeddings.shape[1]} numbers\n ")

print(f"First sentence:'{sentences[0]}'")
print(f"First 5 values of its embedding: {embeddings[0][:5]}")

from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

query='programming with python'
query_embedding = model.encode([query])

similarities = cosine_similarity(query_embedding,embeddings)[0]

print(f"\nQuery: '{query}'")
print("\nSimilarity scores:")
for i, (sentence,score) in enumerate(zip(sentences,similarities)):
    print(f"{score:.4f}-{sentence}")

most_similar_idx=np.argmax(similarities)
print(f"\nMost similar sentences: '{sentences[most_similar_idx]}")
