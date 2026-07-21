# 🎾 Wimbledon 2025 AI Analytics Platform

> **Project 14 of 100** — *Built live during the Wimbledon 2025 fortnight to bring real-time AI intelligence to the lawn.*

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://iamxkhushi1726-svg-wimbledon-ai-dashboard-app-j4bukc.streamlit.app/)
[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)](https://streamlit.io/)
[![Plotly](https://img.shields.io/badge/Plotly-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)](https://plotly.com/)
[![LangChain](https://img.shields.io/badge/LangChain-121011?style=for-the-badge&logo=chainlink&logoColor=white)](https://www.langchain.com/)
[![Groq](https://img.shields.io/badge/Groq-F05023?style=for-the-badge&logo=lightning&logoColor=white)](https://groq.com/)

---

## 🌟 Overview

Welcome to the **Wimbledon 2025 AI Analytics Platform**! 

Instead of browsing endless statistical tables, this dashboard brings structured player data to life using interactive visual models and Llama-3-powered natural language insights. Built with full native light and dark mode compatibility, it translates raw tournament metrics into actionable, broadcast-style tactical previews.

---

## 🚀 Live Demo

Experience the dashboard live in your browser:  
👉 **[Launch the Wimbledon AI Dashboard](https://iamxkhushi1726-svg-wimbledon-ai-dashboard-app-j4bukc.streamlit.app/)**

---

## ✨ Key Features

- 🎾 **Contender Profile Cards:** Instant statistical summaries for top Men's and Women's singles contenders.
- 📊 **Interactive Parameter Segmentation:** Filter and rank players across surface efficiency, aces per match, and Grand Slam titles.
- ⚖️ **Bilateral Head-to-Head Mapping:** Side-by-side metric breakdown with automatic winner highlighting and normalized Plotly radar/spider charts.
- 🎙️ **BBC Sport Style Tactical Briefings:** AI-generated match analyses powered by **Llama 3.3 (via Groq)** that simulate expert broadcast commentary.
- 🔮 **Predictive Bracket Models:** AI-driven tournament winner predictions with technical justifications and calculated win probability densities.
- 🌗 **Native Theme Adaptation:** Built with dynamic CSS variables to instantly match Streamlit’s native Light and Dark mode settings.

---

## 🛠️ Tech Stack

| Category | Technologies Used |
| :--- | :--- |
| **Frontend & UI** | Streamlit, Custom CSS Injection |
| **Data & Viz** | Pandas, Plotly Express, Plotly Graph Objects |
| **AI & Orchestration** | LangChain Core, Groq API |
| **Environment** | Python-dotenv |

---

## 💻 Local Setup

Want to run this app locally on your machine? Follow these simple steps:

### 1. Clone the repository
```bash
git clone [https://github.com/iamxkhushi1726-svg/wimbledon-ai-dashboard.git](https://github.com/iamxkhushi1726-svg/wimbledon-ai-dashboard.git)
cd wimbledon-ai-dashboard

```

### 2. Set up a virtual environment

```bash
python -m venv venv

# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate

```

### 3. Install dependencies

```bash
pip install -r requirements.txt

```

### 4. Configure API Key

Create a `.env` file in the root folder and add your Groq API Key:

```env
GROQ_API_KEY=your_actual_groq_api_key_here

```

### 5. Launch the app

```bash
streamlit run app.py

```

---

## 🧠 Key Takeaways & Learnings

1. **Native Streamlit CSS Binding:** Binding custom HTML components directly to Streamlit's native root CSS variables (`var(--text-color)`, `var(--secondary-background-color)`) ensures high contrast in both Light and Dark modes.
2. **Grounded LLM Prompting:** Injecting structured Pandas data directly into LangChain prompts enforces factual, stats-backed commentary without hallucinations.
3. **Multi-Variable Data Visualization:** Leveraging Plotly (`go.Scatterpolar`) to normalize metrics across serve speeds, win rates, and titles into clean radar comparisons.
4. **Building in Public:** Pairing real-time major sporting events with data engineering applications to build practical, engaging tools.

---

## 🏆 Part of the 100 Projects Challenge

This repository is **Project 14** of my personal challenge to build **100 distinct applications**, focusing on AI, data engineering, and clean web interfaces.

👨‍💻 **Follow my journey on GitHub:** [@iamxkhushi1726-svg](https://github.com/iamxkhushi1726-svg)

---

## 🤝 Contributing & Collaboration

Got ideas to make this platform even better? Contributions, bug reports, and feature requests are always welcome!

1. **Fork** the project repository.
2. **Create** a feature branch (`git checkout -b feature/AmazingFeature`).
3. **Commit** your changes (`git commit -m 'Add some AmazingFeature'`).
4. **Push** to your branch (`git push origin feature/AmazingFeature`).
5. **Open a Pull Request**!

Feel free to reach out or connect on [GitHub](https://github.com/iamxkhushi1726-svg) if you want to collaborate on future projects in AI and data engineering!

