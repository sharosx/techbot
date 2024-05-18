import warnings
import os
import sys
import constants
import nltk
from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import TextLoader, DirectoryLoader  # Combine imports
from langchain.indexes import VectorstoreIndexCreator
import ssl
import socket

# Suppress all warnings
warnings.filterwarnings("ignore")

# Set environment variable
os.environ["OPENAI_API_KEY"] = constants.API_KEY

# Disable SSL certificate verification globally for NLTK download
ssl._create_default_https_context = ssl._create_unverified_context

# Attempt to import NLTK and initialize punkt tokenizer
try:
    nltk.data.find('tokenizers/punkt')
except (LookupError, FileNotFoundError):
    print("NLTK punkt tokenizer not found. Downloading...")
    nltk.download('punkt')

# Get query from command-line argument
query = sys.argv[1]

# Load text from file
loader = DirectoryLoader(".", glob="*.txt")

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
