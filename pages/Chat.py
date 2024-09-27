import streamlit as st
from pymongo import MongoClient
from src.helper import *
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize your language model
llm = ResponseLLM()

# Ensure a character is selected before displaying the chat
if 'selected_cuisine' not in st.session_state:
    st.warning("Please select a cuisine from the home page.")
    st.stop()


# Title of the app
st.title("This is the chat box")

st.header(f"Chat with {st.session_state.selected_cuisine} Chef")

user_input = st.text_input("You: ", "")
cuisine = st.session_state.selected_cuisine
print(f"Chosen option by user {cuisine}")
# name = name[0].lower()
# print(f'first word after split{name}')

if st.button("Send"):
    if user_input:
        # Generate the response from the language model
        response = llm.response(user_input, cuisine)
        st.write(response)

        # # Prepare the data to be inserted into MongoDB
        # chat_entry = {
        #     "character": st.session_state.selected_fighter,
        #     "user_input": user_input,
        #     "response": response
        # }
        #
        # # Insert the chat entry into MongoDB
        # collection.insert_one(chat_entry)

        # st.success("Your question and the response have been stored.")

if st.button("Back"):
    st.switch_page("Home.py")
