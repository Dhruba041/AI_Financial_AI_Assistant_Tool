from langchain_ollama import ChatOllama
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
load_dotenv()
import os
import streamlit as st
from langchain_openai import ChatOpenAI


finance_llm = ChatOllama(
    model="gemma4:e2b",  #this is to test the model locally before exposing to GPT model
    temperature=0
)

llama_llm = ChatOllama(
    model="llama3.1:latest",  #this is to test the model locally before exposing to GPT model
    temperature=0
)

gemini_llm = ChatGoogleGenerativeAI(
    model="gemini-3.8-flash"#, #Had to switch as usage limit was reached for gemini-3.8-flash model, so using gemini-3.7-flash model for now
    #model="gemini-3.7-flash", #Switching again for question 4
    #model="Gemini 3.1 Flash-Lite",
    #api_key=os.getenv("GOOGLE_API_KEY") 
)

gpt_llm = ChatOpenAI(
    model_name="gpt-4o-mini", 
    temperature=0,
    api_key=st.secrets["OPENAI_API_KEY"]
)