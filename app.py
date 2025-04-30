import streamlit as st
from textblob import TextBlob
import json
import random

# ─── Page setup ────────────────────────────────────────────────────────────────
st.set_page_config(page_title="🧠 EmpathAI - Mental Health Chatbot", layout="centered")
st.title("🧠 EmpathAI - Mental Health Chatbot")

# ─── Load data ─────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    with open("data/coping_strategies.json") as f:
        strategies = json.load(f)
    with open("data/resources.json") as f:
        resources = json.load(f)
    return strategies, resources

coping_strategies, resources = load_data()

# ─── Sentiment analysis ────────────────────────────────────────────────────────
def analyze_sentiment(text: str) -> str:
    polarity = TextBlob(text).sentiment.polarity
    if polarity > 0.1:
        return "positive"
    elif polarity < -0.1:
        return "negative"
    return "neutral"

# ─── Conversation state ───────────────────────────────────────────────────────
if "chat" not in st.session_state:
    st.session_state.chat = []

if st.button("🧹 Reset Chat"):
    st.session_state.chat = []
    st. rerun()

# ─── User form ─────────────────────────────────────────────────────────────────
with st.form("chat_form", clear_on_submit=True):
    user_input = st.text_input("How are you feeling today?")
    choice = st.radio(
        "What would you like to see?",
        ["Coping Strategy", "Resources", "Both"],
        index=0
    )
    submitted = st.form_submit_button("Send")

# ─── On submit ─────────────────────────────────────────────────────────────────
if submitted and user_input:
    # record user
    st.session_state.chat.append(("You", user_input))

    # detect emotion
    sentiment = analyze_sentiment(user_input)
    st.session_state.chat.append(
        ("EmpathAI", f"**Emotion detected:** *{sentiment}*")
    )

    # coping strategy
        # ─── Coping strategy ────────────────────────────────────────────────────
    if choice in ("Coping Strategy", "Both"):
        strat = random.choice(
            coping_strategies.get(sentiment, ["Take a deep breath."])
        )

        # if your JSON entry is a dict, pull out its fields…
        if isinstance(strat, dict):
            text     = strat.get("text", "")
            category = strat.get("category", None)
            duration = strat.get("duration", None)
            tags     = strat.get("tags", [])

            # format the main advice in bold
            msg = f"- 💡 **{text}**\n"
            # then list any metadata inline
            meta = []
            if category: meta.append(f"Category: {category}")
            if duration: meta.append(f"Duration: {duration}")
            if tags:     meta.append(f"Tags: {', '.join(tags)}")
            if meta:
                msg += "    _" + "; ".join(meta) + "_"
        else:
            # fallback for plain‐string entries
            msg = f"- 💡 {strat}"

        st.session_state.chat.append(("EmpathAI", msg))

    # resources
    if choice in ("Resources", "Both"):
        links = resources.get(sentiment, [])
        if links:
            for r in links:
                st.session_state.chat.append(
                    ("EmpathAI", f"- 🔗 [{r['title']}]({r['url']})")
                )
        else:
            st.session_state.chat.append(("EmpathAI", "No resources found."))

# ─── Display ───────────────────────────────────────────────────────────────────
st.markdown("### Conversation:")
for speaker, message in st.session_state.chat:
    st.markdown(f"**{speaker}:**  {message}")
