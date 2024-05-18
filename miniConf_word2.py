import warnings
import os
import sys
import constants
from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import PyDocxLoader  # Import the loader for Word files
from langchain_community.document_loaders import AzureAIDocumentIntelligenceLoader
from langchain.indexes import VectorstoreIndexCreator
import ssl
import socket

# Suppress all warnings
warnings.filterwarnings("ignore")

# Set environment variable
os.environ["OPENAI_API_KEY"] = constants.API_KEY

# Get query from command-line argument
query = sys.argv[1]

# Load text from file
loader = PyDocxLoader('volvo.docx')  # Replace 'volvo.docx' with your Word document path
# Create vector store index
index = VectorstoreIndexCreator().from_loaders([loader])

# Query index
try:
    print(index.query(query))
finally:
    # Explicitly close the SSL context after use to avoid ResourceWarning
    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE
    ssl_socket = context.wrap_socket(socket.socket(socket.AF_INET), suppress_ragged_eofs=True, server_hostname='')
    ssl_socket.close()

    # Reset warnings after executing potentially problematic code
    warnings.resetwarnings()
