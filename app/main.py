import sys
import os

# Add the parent directory to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from chatbot.chatbot import ChatBot
import streamlit as st
import base64

# Initialize chatbot
bot = ChatBot()

st.set_page_config(page_title="Personal Investment Advisor", layout="centered")
st.title("💰 Personal Investment Advisor Chatbot")
st.markdown("Ask me anything about investments, SIP, FD, mutual funds, or stock prices!")

# Keep conversation in session
if "messages" not in st.session_state:
    st.session_state.messages = []

# User input
user_input = st.text_input("You:", placeholder="e.g., Where should I invest ₹5000?")

if user_input:
    # Append user message
    st.session_state.messages.append(("user", user_input))

    # Get bot response (could be str or (text, image_base64))
    bot_response = bot.get_response(user_input)
    st.session_state.messages.append(("bot", bot_response))

# Display chat history
for sender, msg in st.session_state.messages:
    if sender == "user":
        st.markdown(f"**You:** {msg}")
    else:
        # If handler returned a tuple (text, image_base64)
        if isinstance(msg, tuple):
            text, img_b64 = msg
            st.markdown(f"**Bot:**\n\n{text}")
            if img_b64:
                st.image(
                    base64.b64decode(img_b64),
                    use_container_width=True
                )
        else:
            st.markdown(f"**Bot:** {msg}")
