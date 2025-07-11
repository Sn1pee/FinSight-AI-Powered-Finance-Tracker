# 💸 FinSight – AI-Powered Personal Finance Tracker

FinSight is a full-stack intelligent dashboard that analyzes your bank transactions (CSV or PDF), visualizes your spending, and delivers **AI-powered insights and savings tips**.

Built with ❤️ using Python, Streamlit, Pandas, Matplotlib, and OpenAI.

---

## 📸 Demo Preview

> *(Add a screenshot below named `demo_screenshot.png`)*

<img src="demo_screenshot.png" alt="FinSight Dashboard" width="800"/>

---

## 🚀 Features

| Feature                          | Description |
|----------------------------------|-------------|
| 📁 Upload CSV or PDF             | Supports bank statements in `.csv` or `.pdf` format |
| 🧠 AI Categorizer (LLM)          | Auto-tags transaction categories with OpenAI GPT-4 |
| 🧾 Rule-Based Categorizer        | Works offline with keyword rules |
| 📊 Multi-panel Visual Dashboard  | Pie chart, bar graph, daily trends, profit/loss comparison |
| 🤖 AI Money Coach                | Personalized insights, savings tips & motivational lines |
| 📤 Exportable CSV (PDF upload)   | Converts PDF text into structured CSV with AI |
| 🔒 Secure Temporary File Handling| Protects against path injection |
| 🌗 Dark Mode Visuals             | Enhanced readability & styling |

---

## 🧠 Tech Stack

- Python 🐍
- [Streamlit](https://streamlit.io/) (UI)
- Pandas (Data Wrangling)
- Matplotlib (Plots)
- pdfplumber (PDF text extraction)
- OpenAI (AI categorizer + insights)
- Hosted on: Streamlit Cloud / Local

---

## 📁 Folder Structure

```
finsight/
├── app.py                  ← Main Streamlit App
├── requirements.txt
├── logic/
│   ├── categorizer.py      ← Rule-based categorization
│   ├── ai_categorizer.py   ← LLM-powered categorization
│   ├── analyzer.py         ← Income/Expense logic
│   ├── insights.py         ← OpenAI-based advice
│   └── PDFtoCSV.py         ← Converts extracted PDF text → CSV using GPT
├── utils/
│   └── plotter.py          ← Dashboard visualizations
├── data/
│   └── sample.csv / pdf    ← Demo files (optional)
```

---

## 🛠️ Setup & Run

### 🧑‍💻 Local Dev:
```bash
git clone https://github.com/your-username/finsight.git
cd finsight
pip install -r requirements.txt
streamlit run app.py
```

### 🔐 Set Your API Key:
```bash
export FINSIGHT_API_KEY=your_openai_key
# or
export GITHUB_TOKEN=your_openai_key
```

---

## ☁️ Deploy on Streamlit Cloud

1. Push this repo to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect to your repo → Deploy  
4. Add your secret key to `Secrets` tab like:

```toml
FINSIGHT_API_KEY = "sk-..."
```

---

## 📈 Sample Usage

- Upload PDF → Extracted & parsed by GPT
- Toggle "Use AI Categorizer" → Transactions intelligently tagged
- Scroll for plots + "AI Money Coach" with savings advice

---

## 🧠 AI Prompt Logic (Quick Peek)

```text
Given the CSV:
Date, Description, Amount, Type

Add a new column: Category
Categories = Food, Transport, Income, Entertainment, Utilities, Shopping, Others
Return only CSV.
```

---

## 📄 License

MIT – free to use, remix, and share.  
Give credit if you build something cool 💙

---

## ✨ Credits

Built with 💻 by [Monish](https://github.com/your-github-url)  
Inspired by real-world financial stress 💀
