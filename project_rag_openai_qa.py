# -*- coding: utf-8 -*-
"""project_rag_openai_qa.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/gist/sreeavinashbesiahgari/6f6dde312c1de377f3561ab2219c85d1/project_rag_openai_qa.ipynb

# Install Dependencies
"""

#!pip install -q langchain langchain-openai langchain-core langchain_community docx2txt pypdf langchain_chroma sentence_transformers

"""# Open AI API Setup

"""

import os
os.environ['OPENAI_API_KEY'] ='YOUR_OPENAI_API_KEY'

"""# Langchain and LangSmith using API Setup"""

os.environ['LANGCHAIN_TRACING_V2'] = 'true'

os.environ['LANGCHAIN_API_KEY'] = 'your_langchain_api_key'
os.environ['LANGCHAIN_PROJECT'] = 'PROJECT_RAG_OPENAI_QA'

"""# Testing LLM and Langchain Connections using simple LLM CALL

You should see the api calls in OpenAI API usage and Langsmith
"""

from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model_name="gpt-4o-mini")

llm_response = llm.invoke(["Tell me a joke"])

llm_response

"""# Creating custom prompt templete using System Message and Human Message"""

#Create a template using ChatPromptTemplate
from langchain_core.prompts import ChatPromptTemplate
template = ChatPromptTemplate(
    [
        ("system", "You are a helpful assistant that tells jokes."),
        ("human", "Tell me about {topic}")
    ]
)

prompt_value = template.invoke({"topic": "cars"})

prompt_value

#template.invoke({"topic": "cars"})

"""Invoke the LLM ( Send the prompt to LLM )"""

llm.invoke(prompt_value)

#!pip install pypdf docx2txt unstructured

"""# LOAD, SPLIT, EMBED, STORE"""

import os
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import PyPDFLoader, Docx2txtLoader
from langchain.schema import Document
from typing import List
from re import split


# simple function to load pdf and docx

def load_documents(folder_path: str) -> List[Document]:
    """Loads PDF and DOCX documents from a folder and returns a list of Documents."""
    documents = []
    processed_files = set()
    # Iterate over files in the folder
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)

        # Check file type and load accordingly
        if filename.endswith(".pdf"):
            loader = PyPDFLoader(file_path)  # Load PDF files
        elif filename.endswith(".docx"):
            loader = Docx2txtLoader(file_path)  # Load DOCX files
        else:
            print(f"Skipping unsupported file: {filename}")
            continue

        # Load document content and append it to the list
        documents.extend(loader.load())

        processed_files.add(filename)  # Store the filename

        print(f"no of Processed files: {len(processed_files)}")

    return documents

# Define the folder path where documents are stored
folder_path = "/content/docs"

# Load documents
documents = load_documents(folder_path)


print(f"Number of documents pages loaded: {len(documents)}")

"""SPLIT THE DOCS INTO CHUNKS"""

# Create text splitter with chunking configuration
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=2000,
    chunk_overlap=200,
    length_function=len
)

# split the document into the chunks
splits = text_splitter.split_documents(documents)

print(f"Number of text chunks created: {len(splits)}")

splits[0].page_content

splits[36].page_content

"""# EMBEDDING USING OPENAI"""

from langchain_openai import OpenAIEmbeddings

embeddings = OpenAIEmbeddings()

document_embeddings = embeddings.embed_documents([split.page_content for split in splits])


print(f"Number of document embeddings: {len(document_embeddings)}")

"""# STORE THE EMBEDDED VECTORS INTO CHROMEDB"""

from langchain.vectorstores import Chroma
from langchain.embeddings.openai import OpenAIEmbeddings

# Initialize OpenAI Embeddings
embedding_function = OpenAIEmbeddings()

# Define collection name and persistence directory
collection_name = "my_collection"
persist_directory = "./chroma_db"  # Directory to store the vectors

# Create Chroma vector store
vectorstore = Chroma.from_documents(
    documents=splits,  # List of text chunks (Ensure 'splits' is populated)
    embedding=embedding_function,
    persist_directory=persist_directory  # Persistent storage
)

print(f"Vector is stored in {persist_directory}")

"""# SIMILARITY SEARCH"""

# Similazrity search in vector db
query = "what is CAG?"
search_results = vectorstore.similarity_search(query,k=2)
search_results

for i , result in enumerate(search_results):
  print(f"Result {i+1}:")
  print(f"Source :{result.metadata.get('source','Unknown')}" )
  print(result.page_content)

retriever = vectorstore.as_retriever(search_kwargs={"k":2})

retriever.invoke("what is CAG?")

"""# Converting Content into Single Context"""

def docs2str(docs):
  return "\n\n".join([doc.page_content for doc in docs])
#

from langchain.schema.runnable import RunnablePassthrough
from langchain_core.prompts import ChatPromptTemplate

template = """ Use the following pieces of context to answer the question at the end. If you don't know the answer, just say that you don't know,
{context}

Question: {question}

Answer:   """


prompt = ChatPromptTemplate.from_template(template)



rag_chain = (
    {"context": retriever | docs2str, "question": RunnablePassthrough()}
    | prompt
)

rag_chain.invoke("what is CAG?")
#

"""# RAG_CHATBOT_QA_CHAIN"""

from langchain.schema.output_parser import StrOutputParser
from langchain.schema.runnable import RunnablePassthrough
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model_name="gpt-4o-mini")
rag_chain = (
    {"context":retriever | docs2str , "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

question = "what is CAG?"
response = rag_chain.invoke(question)

print(response)

"""# CONVERSATIONAL_QA_CHATBOT

Saving the Chat History
"""

from langchain_core.messages import HumanMessage, AIMessage
chat_history = []
chat_history.extend([HumanMessage(content=question), AIMessage(content=response)])

"""Reformulating the question using chat history"""

from langchain_core.prompts import MessagesPlaceholder
contextualize_q_system_prompt = (
    "Given the chat history and the latest user question"
    "which might reference context in the chat history,"
    "formulate a standalone question which can be understood"
    "without the chat history. Do Not answer the latest user question."
    "just reformulate it if needed and otherwise return as it is."

)

contextualize_q_prompt =  ChatPromptTemplate.from_messages(
    [
        ("system", contextualize_q_system_prompt),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}")
    ]
)

contextualize_chain = contextualize_q_prompt | llm | StrOutputParser()

contextualize_chain.invoke({"input": "how is it implemented?" , "chat_history": chat_history})
#

from langchain.chains import create_history_aware_retriever

history_aware_retriever = create_history_aware_retriever(
    llm,
    retriever,
    contextualize_q_prompt

)

history_aware_retriever.invoke({"input":"how is it implemented?","chat_history": chat_history})
#
#


#

from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain

qa_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant that answer the user's question."),
    ("system","Context:{context}"),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{input}")
])

question_answer_chain = create_stuff_documents_chain(
    llm,
    qa_prompt,

)

rag_chain = create_retrieval_chain(
    history_aware_retriever,
    question_answer_chain)

rag_chain.invoke({"input":"how is it implemented?","chat_history": chat_history})

"""# MultiUser ChatBot"""

import sqlite3
from datetime import datetime

DB_NAME = "rag_app.db"


def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def create_application_logs():
    conn = get_db_connection()
    conn.execute('''CREATE TABLE IF NOT EXISTS application_logs
                    (id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT,
                    user_query TEXT,
                    gpt_response TEXT,
                    model TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')

    conn.close()


def insert_application_logs(session_id, user_query, gpt_response, model):
    conn = get_db_connection()
    conn.execute('INSERT INTO application_logs (session_id, user_query, gpt_response,model) VALUES (?,?,?,?)',
                  (session_id,user_query,gpt_response,model)  )
    conn.commit()
    conn.close()

def get_chat_history(session_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT user_query, gpt_response FROM application_logs WHERE session_id = ? ORDER BY created_at', (session_id,))
    messages = []
    for row in cursor.fetchall():
        messages.extend([
            {"role": "human", "content": row['user_query']},
            {"role": "ai", "content": row['gpt_response']}
        ])
    conn.close()
    return messages

# Initialize database
create_application_logs()

import uuid
session_id = str(uuid.uuid4())
chat_history = get_chat_history(session_id)
print(chat_history)
question1 = "what is CAG?"
answer1 = rag_chain.invoke({"input":question,"chat_history":chat_history}) ['answer']
insert_application_logs(session_id,question1,answer1,"gpt-4o-mini")
print(f"Question: {question1}\nAnswer: {answer1}")
#

question2 = "how is it implemented?"
chat_history = get_chat_history(session_id)
print(chat_history)
answer2 = rag_chain.invoke({"input":question2,"chat_history":chat_history}) ['answer']
insert_application_logs(session_id,question2,answer2,"gpt-4o-mini")
print(f"Question: {question2}\nAnswer: {answer2}")
#

question3 = "why is it important?"
chat_history = get_chat_history(session_id)
print(chat_history)
answer3 = rag_chain.invoke({"input":question3,"chat_history":chat_history}) ['answer']
insert_application_logs(session_id,question3,answer3,"gpt-4o-mini")
print(f"Question: {question3}\nAnswer: {answer3}")

"""New User or New Chat"""

session_id = str(uuid.uuid4())
question = "what is CAG?"
chat_history = get_chat_history(session_id)
print(chat_history)
answer = rag_chain.invoke({"input":question,"chat_history":chat_history}) ['answer']
insert_application_logs(session_id,question,answer,"gpt-4o-mini")
print(f"Question: {question}\nAnswer: {answer}")