from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_ollama import OllamaLLM

import streamlit as st
import os


from dotenv import load_dotenv
load_dotenv()

os.environ['LANGCHAIN_API_KEY'] = os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = "Q&A with Ollama"


prompt = ChatPromptTemplate.from_messages(
    [
        ("system","You are a helpful assistance. Please response to the user qurey"),
        ("user","Question:{question}")
    ]
)

def generate_response(question,llm,temparature,max_token):
    llm = OllamaLLM(model=llm)
    outer_parser = StrOutputParser()

    chain = prompt|llm|outer_parser

    answer = chain.invoke({"question":question})
    return answer


st.title("Q&A with Ollama")

st.sidebar.title("Settings")
llm = st.sidebar.selectbox("Select an Ollama Model",options=["gemma2:2b"])

temparature = st.sidebar.slider("Temparature",min_value=0.0,max_value=1.0,value=0.7)
max_token = st.sidebar.slider("Max Tokens",min_value=50,max_value=300,value=150)

st.write("Go ahead and ask anything")
user_input = st.text_input("What is in your mind?")

if user_input:
    response = generate_response(user_input,llm,temparature,max_token)
    st.write(response)

else:
    st.write("Pleaase provide the qurey")
