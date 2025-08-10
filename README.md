# DocChat - Personal Document Q&A Assistant

A simple RAG (Retrieval-Augmented Generation) application that lets you upload documents and ask questions about their content using OpenAI's API.

## Features

- Upload PDF documents via web interface
- Ask questions about your documents
- Get AI-powered answers based on document content
- Simple, clean Streamlit interface

## Quick Start

### 1. Clone & Setup
```bash
git clone https://github.com/chizy7/DocChat.git
cd DocChat
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure API Key
```bash
# Copy the example file
cp .env.example .env

# Edit .env and add your OpenAI API key
OPENAI_API_KEY=sk-your-actual-key-here
```

### 4. Run the App
```bash
streamlit run app.py
```

Visit `http://localhost:8501` in your browser!

## Getting an OpenAI API Key

1. Go to [OpenAI Platform](https://platform.openai.com/api-keys)
2. Sign in or create an account
3. Click "Create new secret key"
4. Copy the key and add it to your `.env` file

## Built With

- [Streamlit](https://streamlit.io/) - Web interface
- [OpenAI API](https://platform.openai.com/) - Language model
- [PyPDF2](https://pypdf2.readthedocs.io/) - PDF processing
- Python 3.8+

## Usage

1. **Upload Documents**: Use the file uploader to add PDF files
2. **Ask Questions**: Type questions about your uploaded documents
3. **Get Answers**: The AI will respond based on document content

## Coming Soon

- [ ] Vector embeddings for better retrieval
- [ ] Support for more file formats (TXT, DOCX)
- [ ] Chat history
- [ ] Source citations
- [ ] Document management features

## License

[TODO]