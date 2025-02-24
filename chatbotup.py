from dotenv import load_dotenv
import streamlit as st
import google.generativeai as genai
import os
import io
from PIL import Image

load_dotenv()
genai.configure(api_key= os.getenv("API_KEY"))

#Function to load gemini flash model and get response
model = genai.GenerativeModel("gemini-1.5-flash")
chat = model.start_chat(history=[])

def get_gemini_response(question):
    response = chat.send_message(question,stream=True)
    return response

def get_gemini_response_For_image(Image1):
    image = Image.open(Image1)
    
    # Convert the image to bytes
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format="JPEG")  # Convert to JPEG for compatibility
    img_bytes = img_byte_arr.getvalue()

    # Properly structured request
    response = chat.send_message([
        {"text": "Describe the contents of this image."},  # Text prompt is mandatory
        {"inline_data": {"mime_type": "image/jpeg", "data": img_bytes}}
    ])
    
    return response

#Frontend Streamlit
st.set_page_config(page_title="Chatbot_using_Gemini_API")
st.header("Gemini LLM Application")

#Intialize session state in chat history
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

input = st.text_input("Input:",key = "input")
For_Image = st.file_uploader("Image = ",key = "Image-input")
Submit_Image = st.button("Get Info From Image")
submit = st.button("Ask the Question")

if submit and input:
    response = get_gemini_response(input)
    #Add Query to chat history
    st.session_state["chat_history"].append(("You",input))
    st.subheader("The Response is:")
    for word in response:
        st.write(word.text)
        st.session_state["chat_history"].append(("BOT",word.text))
elif Submit_Image and For_Image:
    response = get_gemini_response_For_image(For_Image)
    st.session_state["chat_history"].append(("You","Image-Submitted"))
    st.subheader("The Response is:")
    for word in response:
        st.write(word.text)
        st.session_state["chat_history"].append(("BOT",word.text))

st.subheader("Chat History:")

for role,text in st.session_state["chat_history"]:
    st.write(f"{role}:{text}")

if st.button("Clear Chat"):
    st.session_state.messages = []
