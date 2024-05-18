import warnings
import os
import sys
import constants
from langchain_community.document_loaders import DocxLoader
from langchain.indexes import VectorstoreIndexCreator
import ssl
import socket
import streamlit as st

# Suppress all warnings
warnings.filterwarnings("ignore")

# Set environment variable
os.environ["OPENAI_API_KEY"] = constants.API_KEY

# Get query from command-line argument
query = sys.argv[1]

# Load document file
file_path = "/Users/sharosmassaebi/PycharmProjects/pythonProject/Regression_Retro.docx"

if os.path.exists(file_path):
    loader = DocxLoader(file_path)

    # Create vector store index
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
    st.error("The specified file does not exist.")
