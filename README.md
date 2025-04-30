# EmpathAI - Mental Health Chatbot

![EmpathAI Logo](https://raw.githubusercontent.com/Liishaa/mental_health_chatbot/main/.github/logo.png)

A simple yet powerful Streamlit-based chatbot designed to offer empathetic support by detecting user sentiment and providing tailored coping strategies and curated mental health resources.

---

## 📖 Table of Contents

- [Features](#-features)
- [Demo](#-demo)
- [Tech Stack](#-tech-stack)
- [Getting Started](#-getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Running Locally](#running-locally)
- [Data](#-data)
- [Configuration](#-configuration)
- [Enhancements](#-enhancements)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🚀 Features

- **Sentiment Analysis**: Uses TextBlob to classify input as `positive`, `neutral`, or `negative`.
- **Coping Strategies**: Provides randomized tips for emotional regulation; each tip can include metadata (category, duration, tags).
- **Resource Links**: Curated list of external hotlines, articles, and support services.
- **Interactive Flow**: Users can choose to view a coping strategy, resources, or both in each turn.
- **Stateful Chat**: Maintains conversation history across inputs and supports resetting at any time.

---

## 📺 Demo

![Screenshot of App](https://raw.githubusercontent.com/Liishaa/mental_health_chatbot/main/.github/demo.png)

Try it live on [Streamlit Cloud](https://mentalhealthchatbot-l.streamlit.app).

---

## 🛠 Tech Stack

- **Frontend**: [Streamlit](https://streamlit.io)
- **NLP**: [TextBlob](https://textblob.readthedocs.io)
- **Data**: JSON files for strategies and resources
- **Version Control**: Git & GitHub

---

## 🏁 Getting Started

### Prerequisites

- Python 3.8+
- `git` command line

### Installation

1. **Clone the repo**
   ```bash
   git clone https://github.com/Liishaa/mental_health_chatbot.git
   cd mental_health_chatbot
