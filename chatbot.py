from dotenv import load_dotenv
import streamlit as st
import google.generativeai as genai
import os

load_dotenv()
genai.configure(api_key= os.getenv("API_KEY"))

#Function to load gemini flash model and get response
model = genai.GenerativeModel("gemini-pro")
chat = model.start_chat(history=[])

def get_gemini_response(question):
    response = chat.send_message(question,stream=True)
    return response

#Frontend Streamlit
st.set_page_config(page_title="Chatbot_using_Gemini_API")
st.header("Gemini LLM Application")

#Intialize session state in chat history
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

input = st.text_input("Input:",key = "input")
submit = st.button("Ask the Question")

if submit and input:
    response = get_gemini_response(input)
    #Add Query to chat history
    st.session_state["chat_history"].append(("You",input))
    st.subheader("The Response is:")
    for word in response:
        st.write(word.text)
        st.session_state["chat_history"].append(("BOT",word.text))
st.subheader("Chat History:")

for role,text in st.session_state["chat_history"]:
    st.write(f"{role}:{text}")

if st.button("Clear Chat"):
    st.session_state.messages = []