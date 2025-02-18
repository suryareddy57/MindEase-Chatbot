import streamlit as st
import google.generativeai as genai
from textblob import TextBlob
import time

# Configure Gemini API
GOOGLE_API_KEY = 'AIzaSyCh8tGbmK96jHphvqL1KZ1bVv2hPR3pFck'
genai.configure(api_key=GOOGLE_API_KEY)

# Custom CSS for better styling
st.markdown("""
    <style>
    .chat-container {
        border-radius: 10px;
        padding: 10px;
        margin: 10px 0;
    }
    .user-message {
        background-color: #2e7bf3;
        color: white;
        text-align: right;
        padding: 15px;
        border-radius: 15px 15px 0 15px;
        margin: 5px 0;
        max-width: 80%;
        margin-left: auto;
    }
    .bot-message {
        background-color: #383838;
        color: white;
        text-align: left;
        padding: 15px;
        border-radius: 15px 15px 15px 0;
        margin: 5px 0;
        max-width: 80%;
        margin-right: auto;
    }
    .stTextInput>div>div>input {
        border-radius: 20px;
        background-color: #2b2b2b;
        color: white;
        border: 1px solid #4e4e4e;
    }
    .stButton>button {
        border-radius: 20px;
        width: 100%;
        background-color: #2e7bf3;
        color: white;
    }
    /* Dark theme adjustments */
    .stApp {
        background-color: #1a1a1a;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state['messages'] = []

def generate_response(prompt):
    try:
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(
            f"As a mental health support assistant: {prompt}"
        )
        return response.text.strip()
    except Exception as e:
        return f"An error occurred: {str(e)}. Please make sure you have set up your Gemini API key correctly."

def analyze_sentiment(text):
    analysis = TextBlob(text)
    polarity = analysis.sentiment.polarity
    if polarity > 0.5:
        return "Very Positive", "😊"
    elif 0.1 < polarity <= 0.5:
        return "Positive", "🙂"
    elif -0.1 <= polarity <= 0.1:
        return "Neutral", "😐"
    elif -0.5 < polarity < -0.1:
        return "Negative", "😔"
    else:
        return "Very Negative", "😢"

# Main UI
st.title("🌟 Mental Health Support Assistant")
st.markdown("##### I'm here to listen and support you. How are you feeling today?")

# Chat interface
with st.container():
    for message in st.session_state['messages']:
        if message['role'] == 'user':
            st.markdown(
                f"""<div class="user-message">{message["content"]}</div>""", 
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                f"""<div class="bot-message">{message["content"]}</div>""", 
                unsafe_allow_html=True
            )

# Input form
with st.form(key='chat_form', clear_on_submit=True):
    user_message = st.text_input("Share your thoughts...", key="user_input")
    col1, col2 = st.columns([4, 1])
    with col2:
        submit_button = st.form_submit_button("Send 📤")

if submit_button and user_message:
    # Add user message to chat
    st.session_state['messages'].append({"role": "user", "content": user_message})

    # Show typing animation
    with st.spinner("Thinking... 💭"):
        # Analyze sentiment
        sentiment, emoji = analyze_sentiment(user_message)
        
        # Generate response
        response = generate_response(user_message)
        
        # Add bot response to chat
        st.session_state['messages'].append({"role": "assistant", "content": f"{response} {emoji}"})
    
    # Rerun to update the chat display
    st.rerun()

# Sidebar with resources
with st.sidebar:
    st.markdown("### 🆘 Emergency Resources")
    st.markdown("""
    If you need immediate help:
    
    🚨 **National Crisis Hotline**
    - Call: 988
    - Text: HOME to 741741
    
    🌍 **International Resources**
    - [Find Help Near You](https://www.iasp.info/resources/Crisis_Centres/)
    
    💡 **Self-Care Tips**
    - Take deep breaths
    - Practice mindfulness
    - Stay hydrated
    - Connect with loved ones
    - Get enough rest
    """)

    # Professional disclaimer
    st.markdown("---")
    st.markdown("""
    <small>⚠️ **Disclaimer**: This is an AI assistant and not a replacement for professional mental health care. 
    If you're experiencing a serious mental health crisis, please contact a qualified mental health professional.</small>
    """, unsafe_allow_html=True)