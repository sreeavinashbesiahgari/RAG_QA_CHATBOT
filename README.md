# RAG_QA_CHATBOT

Project: RAG OpenAI QA
This project implements a retrieval-augmented generation (RAG) based question-answering system using OpenAI's GPT-4, LangChain, and various document processing tools like PyPDF, Docx2txt, and Chroma for efficient document embedding and similarity search.

Table of Contents
Installation

Project Setup

How It Works

Usage

File Structure

Contributors

License

Installation
To get started with this project, clone the repository and install the necessary dependencies.

Clone the repository:


git clone https://github.com/yourusername/project_rag_openai_qa.git


Navigate into the project directory:

cd project_rag_openai_qa

Install the dependencies:


pip install -q langchain langchain-openai langchain-core langchain_community docx2txt pypdf langchain_chroma sentence_transformers

You will also need to set up environment variables for the OpenAI API key and Langchain API key.


OPENAI_API_KEY="your_open_ai_api_key"

LANGCHAIN_API_KEY="your_langchain_api_key"

LANGCHAIN_PROJECT="PROJECT_RAG_OPENAI_QA"

Project Setup

1. API Setup
The system utilizes the OpenAI API to access the GPT-4 model and LangChain to structure and manage prompt templates and embeddings.

2. Document Loaders
The project supports loading .pdf and .docx files using the PyPDFLoader and Docx2txtLoader from LangChain.

4. Text Splitting
The documents are split into smaller chunks using the RecursiveCharacterTextSplitter for better document processing and vector embedding.

5. Embedding & Similarity Search
Text from documents is embedded into vectors using OpenAI embeddings.

A Chroma vector store is used for storing the embedded vectors, allowing for efficient similarity searches.

5. Retrieval Augmented Generation (RAG) Chain
The system employs a RAG chain using documents, context, and prompt templates to answer questions. It ensures that if the model doesn't know the answer, it responds appropriately.

6. Chat History & Multi-User Support
SQLite is used to store application logs (user queries, GPT responses), and the chat history is maintained for multi-session interactions.

7. Database Logging
The project logs user interactions, including session information, questions, and GPT responses.

How It Works
Document Loading: The system loads PDF and DOCX documents from a directory.

Document Splitting: The documents are split into manageable chunks to fit within the token limits of the model.

Embedding: The chunks of text are embedded into vector representations using OpenAI embeddings.

Vector Storage: The embedded vectors are stored in Chroma for fast similarity searches.

Query Handling: When a user asks a question, the system performs a similarity search in the vector store and retrieves relevant documents. This information is used to generate an answer via a GPT-4-based LLM model.

RAG Chain: A RAG chain that combines document retrieval, context embedding, and GPT-4 responses generates accurate answers to user queries.

Chat History Management: The system supports multi-session chats and stores chat history in a database for future reference.

Logging: The system logs every interaction to provide insights into user behavior and track session details.

Usage
To run the project:

Set up the necessary environment variables as shown in the installation section.

Load your documents (PDF, DOCX) into the /content/docs directory.

Execute the main notebook code (project_rag_openai_qa.ipynb), which will guide you through the process of loading documents, splitting, embedding, and querying.

Ask questions to the system, and it will return relevant answers based on the documents loaded.

Example:

question = "What is CAG?"
response = rag_chain.invoke({"input": question, "chat_history": chat_history})['answer']
print(f"Answer: {response}")

File Structure

project_rag_openai_qa/
├── docs/                    # Folder to store PDF and DOCX files
├── rag_chain.py             # The main RAG chain implementation
├── requirements.txt         # List of dependencies
├── application_logs.db      # SQLite database for logging user interactions
├── project_rag_openai_qa.ipynb # Jupyter Notebook to run the code
└── README.md                # This file

Contributors
SREE AVINASH B

