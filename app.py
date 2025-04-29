import streamlit as st
from textblob import TextBlob
import json
import random

st.set_page_config(page_title="Mental Health Chatbot", layout="centered")
st.title("🧠 EmpathAI - Mental Health Chatbot")

# Load coping strategies and resources
@st.cache_data
def load_data():
    with open("data/coping_strategies.json", "r") as f:
        strategies = json.load(f)
    with open("data/resources.json", "r") as f:
        resources = json.load(f)
    return strategies, resources

coping_strategies, resources = load_data()

# Analyze sentiment
def analyze_sentiment(text):
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    if polarity > 0.1:
        return "positive"
    elif polarity < -0.1:
        return "negative"
    else:
        return "neutral"

# Generate chatbot response
def generate_response(user_input):
    sentiment = analyze_sentiment(user_input)
    strategy = random.choice(coping_strategies[sentiment])
    resource_links = resources[sentiment]

    response = f"**Emotion detected:** *{sentiment}*\n\n"
    response += f"Here’s something you might find helpful:\n- 💡 *{strategy}*\n\n"

    if resource_links:
        response += "You can also explore these resources:\n"
        for res in resource_links:
            response += f"- 🔗 [{res['title']}]({res['url']})\n"
    return response

# Session state to track conversation
if "chat" not in st.session_state:
    st.session_state.chat = []

# Chat reset button
if st.button("🧹 Reset Chat"):
    st.session_state.chat = []
    st.session_state.user_input = ""
    st.rerun()

# User input
user_input = st.text_input("How are you feeling today?", key="user_input")

if user_input:
    response = generate_response(user_input)
    st.session_state.chat.append(("You", user_input))
    st.session_state.chat.append(("EmpathAI", response))

# Display conversation
st.markdown("### Conversation:")
for speaker, message in st.session_state.chat:
    st.markdown(f"**{speaker}:**\n{message}")

