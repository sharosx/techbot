import warnings
import os
import sys
import constants
import torch
from transformers import AutoTokenizer, AutoModel
from langchain_community.document_loaders import TextLoader
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
loader = TextLoader('putin.txt')

# Load pre-trained model and tokenizer
tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased")
model = AutoModel.from_pretrained("distilbert-base-uncased")

# Tokenize input text
text = loader.load()
inputs = tokenizer(text, return_tensors="pt")

# Generate embeddings
with torch.no_grad():
    outputs = model(**inputs)
    embeddings = outputs.last_hidden_state.mean(dim=1)  # Take the mean of token embeddings

# Create vector store index with embeddings
index = VectorstoreIndexCreator().from_embeddings(embeddings.tolist())  # Convert embeddings to list

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
