import warnings
import os
import sys
import constants
from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import TextLoader
from langchain_community.document_loaders import DirectoryLoader
from langchain.indexes import VectorstoreIndexCreator
from langchain_community.chat_models import ChatOpenAI
from langchain_community.llms import OpenAI
import ssl
import socket

# Suppress all warnings
warnings.filterwarnings("ignore")

# Set environment variable
os.environ["OPENAI_API_KEY"] = constants.API_KEY

# Get query from command-line argument
query = sys.argv[1]

# Load text from file
loader = TextLoader('putin.txt')

# Create vector store index
index = VectorstoreIndexCreator().from_loaders([loader])

# Query index
try:
    # Instantiate LLMChain with ChatOpenAI
    llm_chain = OpenAI()  # Assuming OpenAI class implements Runnable interface
#   print(index.query(query, llm=llm_chain))
    print(index.query(query, llm=ChatOpenAI()))

finally:
    # Explicitly close the SSL context after use to avoid ResourceWarning
    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE
    ssl_socket = context.wrap_socket(socket.socket(socket.AF_INET), suppress_ragged_eofs=True, server_hostname='')
    ssl_socket.close()

    # Reset warnings after executing potentially problematic code
    warnings.resetwarnings()