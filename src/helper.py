import os
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_groq import ChatGroq
from dotenv import load_dotenv
from src.prompt import *
import streamlit as st



# Load environment variables
load_dotenv()

os.environ['LANGCHAIN_TRACING_V2'] = 'true'
LANGCHAIN_API_KEY = os.getenv('LANGCHAIN_API_KEY')


def get_prompt(person_name):
    variable_name = f"{person_name.lower()}"
    print(variable_name)
    return globals().get(variable_name, None)


class ResponseLLM:
    def __init__(self, model=None, embeddings=None):
        # Initialize the model and embeddings, using defaults if none provided
        self.model = model or ChatGroq(temperature=0.7, model="llama3-70b-8192", api_key=os.environ['GORQ_API_KEY'])
        self.embeddings = embeddings or GoogleGenerativeAIEmbeddings(model="models/embedding-001")

    def load_ebooks(self, ebooks):
        # Load documents from a directory of PDF files
        loader = PyPDFDirectoryLoader(ebooks)
        documents = loader.load()
        return documents

    def split_text(self, documents):
        # Split documents into smaller chunks
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=200)
        split_text = text_splitter.split_documents(documents)
        return split_text

    def create_embeddings(self, split_text, persona_name):
        # Create embeddings for the text chunks and save them to a local FAISS index
        vector_store = FAISS.from_documents(split_text, embedding=self.embeddings)
        vector_store.save_local(f"data/{persona_name}/faiss_index_{persona_name}")
        return vector_store

    def response(self, user_response, persona_name):
        # Generate a response to the user's question
        prompt_template = get_prompt(persona_name)
        
        if not prompt_template:
            raise ValueError(f"No prompt found for {persona_name}")
        # Load the FAISS index based on the persona name
        new_db = FAISS.load_local(f"data/{persona_name}/faiss_index_{persona_name}", self.embeddings, allow_dangerous_deserialization=True)
        # Perform a similarity search with the user's question
        docs = new_db.similarity_search(user_response)
        # Create the prompt with context
        prompt = PromptTemplate(template=prompt_template, input_variables=["user_response", 'context'])
        print(prompt)
        # Chain the prompt with the model and output parser
        chain = prompt | self.model | StrOutputParser()
        # Generate the response
        response = chain.invoke({"context": docs, "user_response": user_response})
        return response

    def translate_output(self, response, language):
        prompt_template = '''translate following text english to {language} 
        convert text : {response}'''
        prompt = PromptTemplate(template=prompt_template, input_variables=["language",'response'])
        chain = prompt | self.model | StrOutputParser()
        translation= chain.invoke({"language": language, 'response':response})
        return translation

    def prompt_generator(self, name):
        # Create a prompt template for predicting the next question
        prompt_template = """
        build a prompt by giving the name of freedom fighter {name} you created a prompt  for that person as per given format:
        
        Model Prompt 1 
        You are Swatantryaveer Vinayak Damodar Savarkar, an Indian freedom fighter, writer, and revolutionary. I will provide you with data and context about your life and work. Your responses should be forceful, impactful, and clear, using powerful and direct language, much like your fiery oratory style. Avoid vague or hidden meanings.

Context: {context}

When the user asks a question based on their perspective, respond as if you are Savarkar, providing answers that are direct, clear, and full of conviction, as if spoken by you.

User's Question: {user_question}

        Model Prompt 2
        
        You are Sardar Vallabhbhai Patel, a prominent Indian freedom fighter, statesman, and the first Deputy Prime Minister and Home Minister of India. Known as the "Iron Man of India," your efforts in uniting the princely states and ensuring the country's integrity are legendary. Your responses should reflect your pragmatic, firm, and determined personality, showcasing your unwavering commitment to national unity and strength.

Context: {context}

When the user asks a question based on their perspective, respond as if you are Sardar Patel, providing answers that are clear, firm, and resolute, embodying the spirit of unity and strong leadership.

User's Question: {user_question}

        """
        
        # Create the prompt and LLM chain
        prompt = PromptTemplate(template=prompt_template, input_variables=["name"])
        
        chain = prompt | self.model | StrOutputParser()
        
        # Use the chain to predict the next question
        final_prompt = chain.invoke(name)
        
        return final_prompt