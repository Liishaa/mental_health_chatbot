import streamlit as st
import json
import random
from transformers import pipeline

# ─── 1) Init your BERT sentiment pipeline ───────────────────────────────────────
classifier = pipeline("sentiment-analysis")

# ─── 2) Streamlit page setup ───────────────────────────────────────────────────
st.set_page_config(page_title="EmpathAI - Mental Health Chatbot", layout="centered")
st.title("🧠 EmpathAI - Mental Health Chatbot")

# ─── 3) Load your JSON data (coping strategies + resources) ────────────────────
@st.cache_data
def load_data():
    with open("data/coping_strategies.json") as f:
        strategies = json.load(f)
    with open("data/resources.json") as f:
        resources = json.load(f)
    return strategies, resources

coping_strategies, resources = load_data()

# ─── 4) Helpers ─────────────────────────────────────────────────────────────────
def analyze_sentiment(text: str):
    """Return ('POSITIVE'|'NEGATIVE', score)."""
    out = classifier(text)[0]
    return out["label"], out["score"]

def generate_response(user_input: str):
    label, score = analyze_sentiment(user_input)
    key = label.lower()  # maps 'POSITIVE'→'positive', etc.

    strategy = random.choice(coping_strategies.get(key, ["Take a deep breath."]))
    resource_links = resources.get(key, [])

    resp = f"**Emotion detected:** *{key}* (confidence {score:.2f})\n\n"
    resp += f"Here’s something you might find helpful:\n- 💡 *{strategy}*\n\n"

    if resource_links:
        resp += "You can also explore these resources:\n"
        for r in resource_links:
            resp += f"- 🔗 [{r['title']}]({r['url']})\n"
    return resp

# ─── 5) Session-state for chat history ──────────────────────────────────────────
if "chat" not in st.session_state:
    st.session_state.chat = []

# ─── 6) Reset button (clears history) ───────────────────────────────────────────
if st.button("🧹 Reset Chat"):
    st.session_state.chat = []

# ─── 7) User input and appending to history ────────────────────────────────────
user_input = st.text_input("How are you feeling today?")
if user_input:
    # generate & save the exchange
    reply = generate_response(user_input)
    st.session_state.chat.append(("You", user_input))
    st.session_state.chat.append(("EmpathAI", reply))
    # clear the text_input (so it doesn't keep your last message)
    st.session_state["text_input_clear"] = True

# ─── 8) Display the conversation ───────────────────────────────────────────────
st.markdown("### Conversation:")
for speaker, message in st.session_state.chat:
    st.markdown(f"**{speaker}:** {message}")
