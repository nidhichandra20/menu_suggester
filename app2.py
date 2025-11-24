import streamlit as st
import os
from dotenv import load_dotenv
from groq import Groq

# Load environment variables
load_dotenv()
api_key = os.getenv("Grok_API_KEY")

client = Groq(api_key=api_key)

# Initialize session state for messages
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are a  chef , who suggest 3 course menu for the cuisine given by the user , give the response in simple way."}
    ]

# Define the chat function
def llama_chat(messages,
               model="llama-3.3-70b-versatile",
               temperature=0.0,
               max_tokens=1024):

    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens
    )
    return response.choices[0].message.content

# Streamlit UI
st.set_page_config(page_title="🦙 LLaMA Chat", layout="centered")
st.title("🦙 LLaMA Chatbot")
st.markdown("Ask anything and continue the conversation with the LLaMA model!")

# Display chat history
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"**You:** {msg['content']}")
    elif msg["role"] == "assistant":
        st.markdown(f"**LLaMA:** {msg['content']}")

# Input box
prompt = st.text_area("Enter your message:", height=150)

# Generate button
if st.button("Send"):
    if prompt.strip():
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.spinner("Thinking..."):
            response = llama_chat(st.session_state.messages)
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.success("Response:")
        st.write(response)
        
    else:
        st.warning("Please enter a message to continue.")