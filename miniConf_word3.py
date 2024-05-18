import sys
import warnings
import os
import constants
import streamlit as st
from docx import Document  # Import Document from python-docx for Word files
from langchain.indexes import VectorstoreIndexCreator
from langchain_community.document_loaders import TextLoader
import ssl
import socket
import io  # Import io module

# Suppress all warnings
warnings.filterwarnings("ignore")

# Set environment variable
os.environ["OPENAI_API_KEY"] = constants.API_KEY

# Get query from command-line argument
if len(sys.argv) > 1:
    query = sys.argv[1]
else:
    query = "summerize document"  # Default query if not provided

# Load Word file
st.title("Upload Word Document")
uploaded_file = st.file_uploader("Upload a Word document", type=["docx"])

if uploaded_file is not None:
    st.write("File Uploaded Successfully!")
    file_contents = uploaded_file.read()

    # Extract text content from Word document
    doc = Document(io.BytesIO(file_contents))  # Use io.BytesIO to create a file-like object
    text = ""
    for paragraph in doc.paragraphs:
        text += paragraph.text + "\n"

    # Create text loader and vector store index
    loader = TextLoader(text)
    index = VectorstoreIndexCreator().from_loaders([loader])

    # Query index
    try:
        result = index.query(query)
        if result:
            st.write("Result:", result)
        else:
            st.write("No result found for the query.")
    except Exception as e:
        st.error(f"An error occurred: {e}")
    finally:
        # Explicitly close the SSL context after use to avoid ResourceWarning
        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
        ssl_socket = context.wrap_socket(socket.socket(socket.AF_INET), suppress_ragged_eofs=True, server_hostname="")
        ssl_socket.close()

        # Reset warnings after executing potentially problematic code
        warnings.resetwarnings()
else:
    st.error("Please upload a Word document.")
