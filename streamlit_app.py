import streamlit as st
import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure the page
st.set_page_config(
    page_title="RAG QA Chatbot",
    page_icon="🤖",
    layout="wide"
)

# Constants
API_URL = "http://localhost:8000"

# Initialize session state
if 'session_id' not in st.session_state:
    st.session_state.session_id = None
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

def upload_file(file):
    """Upload a file to the FastAPI backend"""
    try:
        files = {"file": file}
        response = requests.post(f"{API_URL}/upload", files=files)
        if response.status_code == 200:
            st.success(f"File {file.name} uploaded successfully!")
        else:
            st.error(f"Error uploading file: {response.text}")
    except Exception as e:
        st.error(f"Error uploading file: {str(e)}")

def get_documents():
    """Get list of documents from the FastAPI backend"""
    try:
        response = requests.get(f"{API_URL}/documents")
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Error getting documents: {response.text}")
            return []
    except Exception as e:
        st.error(f"Error getting documents: {str(e)}")
        return []

def delete_file(filename):
    """Delete a file from the FastAPI backend"""
    try:
        response = requests.delete(f"{API_URL}/documents/{filename}")
        if response.status_code == 200:
            st.success(f"File {filename} deleted successfully!")
        else:
            st.error(f"Error deleting file: {response.text}")
    except Exception as e:
        st.error(f"Error deleting file: {str(e)}")

def chat_with_documents(question):
    """Send a question to the FastAPI backend"""
    try:
        data = {
            "question": question,
            "session_id": st.session_state.session_id
        }
        response = requests.post(f"{API_URL}/chat", json=data)
        if response.status_code == 200:
            result = response.json()
            st.session_state.session_id = result["session_id"]
            return result["answer"]
        else:
            st.error(f"Error getting response: {response.text}")
            return None
    except Exception as e:
        st.error(f"Error getting response: {str(e)}")
        return None

# Main UI
st.title("🤖 RAG QA Chatbot")

# Sidebar for file management
with st.sidebar:
    st.header("📁 Document Management")
    
    # File upload
    uploaded_file = st.file_uploader("Upload a document (PDF or DOCX)", type=["pdf", "docx"])
    if uploaded_file:
        upload_file(uploaded_file)
    
    # List and delete documents
    st.subheader("Uploaded Documents")
    documents = get_documents()
    for doc in documents:
        col1, col2 = st.columns([3, 1])
        with col1:
            st.write(f"📄 {doc['name']}")
            st.caption(f"Size: {doc['size']/1024:.1f} KB | Modified: {doc['modified']}")
        with col2:
            if st.button("🗑️", key=f"delete_{doc['name']}"):
                delete_file(doc['name'])
                st.rerun()

# Main chat interface
st.header("💬 Chat with your documents")

# Display chat history
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Chat input
if prompt := st.chat_input("Ask a question about your documents"):
    # Add user message to chat history
    st.session_state.chat_history.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)
    
    # Get response from the backend
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = chat_with_documents(prompt)
            if response:
                st.write(response)
                st.session_state.chat_history.append({"role": "assistant", "content": response})

# Add a clear chat button
if st.button("Clear Chat"):
    st.session_state.chat_history = []
    st.rerun()

# Footer
st.markdown("---")
st.markdown("Made with ❤️ using FastAPI and Streamlit") 