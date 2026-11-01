import os
import streamlit as st
from PyPDF2 import PdfReader
from dotenv import load_dotenv
from rag_class import RAGSystem

load_dotenv()

st.set_page_config(page_title="Document Q&A",page_icon="📄")
st.title("📄 Ask Your Document")
st.caption("Upload a PDF or text file,then ask questions about it.")

API_KEY=os.getenv("GROQ_API_KEY")
if not API_KEY:
    st.error('GROQ_API_KEY not found in .env file')
    st.stop()
    
if "rag" not in st.session_state:
    st.session_state.rag=RAGSystem(
        collection_name="app_docs",
        groq_api_key=API_KEY
    )
    st.session_state.messages=[]
    st.session_state.loaded_file=None

Uploaded =st.file_uploader('Upload a document',type=["pdf","txt"])

if Uploaded and st.session_state.loaded_file !=Uploaded.name:
    with st.spinner("Reading and Indexing your Document...."):
        if Uploaded.name.endswith('.pdf'):
            reader = PdfReader(Uploaded)
            text="\n".join(page.extract_text() or "" for page in reader.pages)
        
        else:
            text=Uploaded.read().decode("utf-8")
            
        st.session_state.rag.clear()
        n_chunks=st.session_state.rag.load_text(text)
        st.session_state.loaded_file=Uploaded.name
        st.session_state.messages=[]
        
    st.success(f"Indexed '{Uploaded.name}' into {n_chunks} chunks")

if st.session_state.loaded_file:
    for msg in st.session_state.messages:
        with st.chat_message(msg['role']):
            st.write(msg['content'])
            
    if question :=st.chat_input("Ask something about your document"):
        st.session_state.messages.append({"role":"user","content":question})
        with st.chat_message("user"):
            st.write(question)
            
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                result=st.session_state.rag.ask(question)
            st.write(result["answer"])
            with st.expander(f"Sources used ({len(result['sources'])})"):
                for source in result['sources']:
                    st.caption(source)
                    
        st.session_state.messages.append(
            {"role":"assistant","content":result["answer"]}
        )
        
else:
    st.info("Upload a document to get started.")