from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

import openai
import streamlit as st

from dotenv import load_dotenv
load_dotenv()

import os

os.environ['LANGCHAIN_API_KEY'] = os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = "Simple_QA_Chatbot"


# Prompt for our model

prompt = ChatPromptTemplate.from_messages(
    [
        ("system","You are a helpful assitant. Please response to the user qureies"),
        ("user","Question:{question}")
    ]
)

def generate_response(question,llm,api_key,temparature,max_token):
    os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
    llm = ChatOpenAI(model=llm)
    output_parser = StrOutputParser()

    chain = prompt|llm|output_parser
    answer = chain.invoke({"question":question})

    return answer

# Setting up the Streamlit App

st.title("Q&A Chatbot with OpenAI")

st.sidebar.title("Setting")
api_key = st.sidebar.text_input("Enter your API key",type="password")
llm = st.sidebar.selectbox("Select an OpenAI Model",options=["gpt-4o", "gpt-4o-mini","gpt-4-turbo","gpt-4","gpt-3.5-turbo"])


temparature = st.sidebar.slider("Temparature",min_value=0.0,max_value=1.0,value=0.7)
max_token = st.sidebar.slider("Max Token",min_value=50,max_value=300,value=150)

st.write("Go ahead and ask your question")
user_input = st.text_input("What you have in your mind?")

if user_input:
    response = generate_response(user_input,llm,api_key,temparature,max_token)
    st.write(response)
else:
    st.write("Please provide the qurey")

