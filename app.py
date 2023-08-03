import os, openai
import streamlit as st
from build_index import generate_embeddings, query_chroma, generate_or_return_embeddings
from langchain.llms import OpenAI
from dotenv import load_dotenv
load_dotenv()

openai.organization = os.getenv('OPENAI_ORGANIZATION')
openai.api_key = os.getenv('OPENAI_API_KEY')

#Generate basic interface
st.title("IX Search Engine")
st.header("Search Across Documents in Natural Language")

def generate_response(query):
    index = generate_or_return_embeddings()
    #llm = OpenAI(temperature=0.5, openai_api_key=openai_api_key)
    response = query_chroma(index, query)
    st.markdown(response)

with st.form('my_form'):
        query = st.text_area("Ask something", placeholder="Tell me about Pavise.")
        submitted = st.form_submit_button('Submit')

        if submitted:
              with st.spinner("Searching across documents..."):
                   generate_response(query)
            