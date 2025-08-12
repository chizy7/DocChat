import streamlit as st
import os
import openai
from dotenv import load_dotenv
import PyPDF2
import io

# Load environment variables
load_dotenv()

st.title("DocChat - Simple Start")

# 1. API Key Validation
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    st.error("Please add OPENAI_API_KEY to your .env file")
    st.info("Get your key from: https://platform.openai.com/api-keys")
    st.stop()

# Set OpenAI API key
openai.api_key = api_key
st.success("OpenAI API key loaded!")

# 2. File Upload
st.header("Upload Document")
uploaded_file = st.file_uploader("Choose a PDF file", type=['pdf'])

if uploaded_file:
    st.success(f"Uploaded: {uploaded_file.name}")
    
    # Save file to documents folder
    os.makedirs("documents", exist_ok=True)
    file_path = f"documents/{uploaded_file.name}"
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    # 3. PDF Text Extraction
    st.header("Extract Text")
    if st.button("Extract Text from PDF"):
        try:
            # Read PDF content
            pdf_reader = PyPDF2.PdfReader(uploaded_file)
            text_content = ""
            
            # Extract text from all pages
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text_content += page.extract_text() + "\n"
            
            if text_content.strip():
                st.success(f"Extracted text from {len(pdf_reader.pages)} pages")
                
                # Show preview of extracted text
                with st.expander("Preview extracted text"):
                    st.text_area("Content preview:", text_content[:1000] + "...", height=200)
                
                # Store in session state for Q&A
                st.session_state['document_text'] = text_content
                st.session_state['document_name'] = uploaded_file.name
                
            else:
                st.warning("Could not extract text from this PDF")
                
        except Exception as e:
            st.error(f"Error extracting text: {str(e)}")

# 4. Basic Q&A with OpenAI
if 'document_text' in st.session_state:
    st.header("Ask Questions")
    st.info(f"Ready to answer questions about: {st.session_state['document_name']}")
    
    question = st.text_input("What would you like to know about your document?", 
                            placeholder="e.g., What is this document about?")
    
    if st.button("Ask Question") and question:
        with st.spinner("Thinking..."):
            try:
                # Prepare prompt with document context
                prompt = f"""
                Based on the following document content, please answer the question.
                
                Document: {st.session_state['document_name']}
                Content: {st.session_state['document_text'][:3000]}...
                
                Question: {question}
                
                Answer based only on the document content:
                """
                
                # Call OpenAI API
                response = openai.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=500,
                    temperature=0
                )
                
                answer = response.choices[0].message.content
                
                # Display the answer
                st.subheader("Answer:")
                st.write(answer)
                
                # Store in chat history
                if 'chat_history' not in st.session_state:
                    st.session_state['chat_history'] = []
                st.session_state['chat_history'].append((question, answer))
                
            except Exception as e:
                st.error(f"Error getting answer: {str(e)}")
    
    # Show chat history
    if 'chat_history' in st.session_state and st.session_state['chat_history']:
        st.header("Chat History")
        for i, (q, a) in enumerate(st.session_state['chat_history']):
            with st.expander(f"Q{i+1}: {q[:50]}..."):
                st.write(f"**Question:** {q}")
                st.write(f"**Answer:** {a}")

# Instructions for users
if 'document_text' not in st.session_state:
    st.header("How to Use")
    st.markdown("""
    1. **Upload a PDF** using the file uploader above
    2. **Extract text** by clicking the "Extract Text from PDF" button  
    3. **Ask questions** about your document content
    4. **Get AI answers** based on what's in your document
    
    **Example questions to try:**
    - "What is the main topic of this document?"
    - "Can you summarize the key points?"
    - "What conclusions are mentioned?"
    """)

# Clear data button
if st.sidebar.button("Clear All Data"):
    # Clear session state
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    
    # Clear documents folder
    if os.path.exists("documents"):
        import shutil
        shutil.rmtree("documents")
    
    st.success("🧹 All data cleared!")
    st.experimental_rerun()