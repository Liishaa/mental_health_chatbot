import streamlit as st
from textblob import TextBlob
import json
import random

# Streamlit page config
st.set_page_config(page_title="EmpathAI - Mental Health Chatbot", layout="centered")
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
def analyze_sentiment(text: str) -> str:
    """Return 'positive', 'neutral', or 'negative' based on TextBlob polarity."""
    polarity = TextBlob(text).sentiment.polarity
    if polarity > 0.1:
        return "positive"
    if polarity < -0.1:
        return "negative"
    return "neutral"

# Build response
def generate_response(user_input: str) -> str:
    sentiment = analyze_sentiment(user_input)
    strategy = random.choice(
        coping_strategies.get(sentiment, ["Take a deep breath."])
    )
    resource_links = resources.get(sentiment, [])

    response = f"**Emotion detected:** *{sentiment}*\n\n"
    response += f"Here’s something you might find helpful:\n- 💡 *{strategy}*\n\n"
    if resource_links:
        response += "You can also explore these resources:\n"
        for res in resource_links:
            response += f"- 🔗 [{res['title']}]({res['url']})\n"
    return response

# Chat session state
if "chat" not in st.session_state:
    st.session_state.chat = []

if st.button("🧹 Reset Chat"):
    st.session_state.chat = []
    st.experimental_rerun()

# Input box
user_input = st.text_input("How are you feeling today?", key="input")
if user_input:
    st.session_state.chat.append(("You", user_input))
    st.session_state.chat.append(("EmpathAI", generate_response(user_input)))

# Display conversation
st.markdown("### Conversation")
for speaker, message in st.session_state.chat:
    st.markdown(f"**{speaker}:**  {message}")
