# RAG QA Chatbot

A powerful Question-Answering chatbot built with FastAPI and Streamlit that uses RAG (Retrieval-Augmented Generation) to provide accurate answers based on your documents.

## Features

- 📄 Document Upload: Support for PDF and DOCX files
- 🤖 Intelligent Q&A: Powered by OpenAI's GPT model with RAG
- 💬 Interactive Chat Interface: Built with Streamlit
- 🔄 Chat History: Maintains conversation context
- 📊 Document Management: Upload, view, and delete documents
- 🔒 Session Management: Multi-user support with unique session IDs

## Tech Stack

- **Backend**: FastAPI
- **Frontend**: Streamlit
- **LLM**: OpenAI GPT
- **Vector Store**: ChromaDB
- **Document Processing**: LangChain
- **Database**: SQLite

## Prerequisites

- Python 3.8+
- OpenAI API key
- Virtual environment (recommended)

## Installation

1. Clone the repository:
```bash
git clone <your-repo-url>
cd RAG_QA_CHATBOT
```

2. Create and activate a virtual environment:
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# Linux/Mac
python -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the project root and add your OpenAI API key:
```
OPENAI_API_KEY=your-api-key-here
```

## Usage

1. Start the FastAPI backend:
```bash
python app.py
```
The backend will be available at `http://localhost:8000`

2. In a new terminal, start the Streamlit frontend:
```bash
streamlit run streamlit_app.py
```
The frontend will be available at `http://localhost:8501`

3. Use the application:
   - Upload documents using the sidebar
   - Ask questions about your documents in the chat interface
   - View and manage your uploaded documents
   - Clear chat history when needed

## API Endpoints

- `POST /upload`: Upload PDF or DOCX files
- `GET /documents`: List all uploaded documents
- `DELETE /documents/{filename}`: Delete a specific document
- `POST /chat`: Send questions and get answers

## Project Structure

```
RAG_QA_CHATBOT/
├── app.py                 # FastAPI backend
├── streamlit_app.py       # Streamlit frontend
├── requirements.txt       # Project dependencies
├── .env                  # Environment variables
├── docs/                 # Uploaded documents directory
├── chroma_db/           # Vector store directory
└── rag_app.db           # SQLite database
```

## Features in Detail

### Document Processing
- Supports PDF and DOCX files
- Automatic text chunking and embedding
- Vector storage for efficient retrieval

### Chat System
- Context-aware responses using RAG
- Maintains chat history per session
- Multi-user support
- Real-time responses

### User Interface
- Clean and intuitive design
- Document management sidebar
- Interactive chat interface
- File upload and deletion capabilities

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- OpenAI for the GPT models
- LangChain for the RAG implementation
- FastAPI and Streamlit communities 