import streamlit as st
from textblob import TextBlob
import json
import random

# Streamlit page config

st.set_page_config(page_title="🧠 EmpathAI – Mental Health Chatbot", layout="centered")
st.title("🧠 EmpathAI – Mental Health Chatbot")


# Load JSON data
@st.cache_data
def load_data():
    with open("data/coping_strategies.json") as f:
        strategies = json.load(f)
    with open("data/resources.json") as f:
        resources = json.load(f)
    return strategies, resources

coping_strategies, resources = load_data()




# TextBlob sentiment
def analyze_sentiment(text: str):
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity  # –1 to +1

    if polarity > 0.1:
        return "positive", polarity
    elif polarity < -0.1:
        return "negative", polarity
    else:
        return "neutral", polarity


# Build bot reply
def generate_response(user_text: str) -> str:
    sentiment, score = analyze_sentiment(user_text)
    strat = random.choice(coping_strategies.get(sentiment, ["Take a deep breath."]))
    links = resources.get(sentiment, [])
    resp = f"**Emotion detected:** *{sentiment}* (score {score:.2f})\n\n"
    resp += f"Here’s something that might help:\n- 💡 *{strat}*\n\n"
    if links:
        resp += "You can also explore these resources:\n"
        for r in links:
            resp += f"- 🔗 [{r['title']}]({r['url']})\n"
    return resp


# Session state for chat
if "chat" not in st.session_state:
    st.session_state.chat = []

# Reset button
if st.button("🧹 Reset Chat"):
    st.session_state.chat = []
    st.experimental_rerun()


# User input
user_input = st.text_input("How are you feeling today?", key="user_input")

if user_input:
    reply = generate_response(user_input)
    st.session_state.chat.append(("You", user_input))
    st.session_state.chat.append(("EmpathAI", reply))
    # Clear the input box
    st.session_state.user_input = ""

# Display conversation
st.markdown("### Conversation")
for who, msg in st.session_state.chat:
    st.markdown(f"**{who}:**  {msg}")
