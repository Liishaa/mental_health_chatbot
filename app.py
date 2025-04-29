import streamlit as st
from textblob import TextBlob
import json
import random

# Streamlit page config

st.set_page_config(page_title="🧠 EmpathAI - Mental Health Chatbot", layout="centered")
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

# Analyze sentiment with TextBlob
def analyze_sentiment(text: str):
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    # simple thresholds

    if polarity > 0.1:
        label = "positive"
    elif polarity < -0.1:
        label = "negative"
    else:
        label = "neutral"
    return label, polarity


# Build response
def generate_response(user_input: str):
    label, score = analyze_sentiment(user_input)
    strategy = random.choice(coping_strategies.get(label, ["Take a deep breath."]))
    links = resources.get(label, [])

    response = f"**Emotion detected:** *{label}* (score {score:.2f})\n\n"
    response += f"Here’s something you might find helpful:\n- 💡 *{strategy}*\n\n"

    if links:
        response += "You can also explore these resources:\n"
        for r in links:
            response += f"- 🔗 [{r['title']}]({r['url']})\n"
    return response


# Chat history in session state

if "chat" not in st.session_state:
    st.session_state.chat = []

# Reset
if st.button("🧹 Reset Chat"):
    st.session_state.chat = []
    st.experimental_rerun()


# Input box
user_input = st.text_input("How are you feeling today?")

if user_input:
    st.session_state.chat.append(("You", user_input))
    reply = generate_response(user_input)
    st.session_state.chat.append(("EmpathAI", reply))
    st.experimental_rerun()

# Display
st.markdown("### Conversation:")
for speaker, msg in st.session_state.chat:
    st.markdown(f"**{speaker}:** {msg}")
