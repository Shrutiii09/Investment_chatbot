
# 💬 Personal Investment Advisor Chatbot

An interactive, intelligent chatbot built with **Python**, **Streamlit**, and **NLP** that helps users with investment queries like SIP returns, FD interest, stock prices, gold rates, and mutual fund NAVs.

---

## 🚀 Features

✅ Natural language understanding using spaCy + ML  
✅ Get **stock prices** (e.g., TCS, Reliance, Infosys)  
✅ Fetch **gold prices** using web scraping  
✅ Calculate **SIP returns** with growth chart  
✅ Estimate **Fixed Deposit maturity**  
✅ Check **Mutual Fund NAVs** (Axis, HDFC, SBI, etc.)  
✅ Clean and interactive **chat UI** with Streamlit  

---

## 🗂️ Project Structure

Investment_chatbot/
│
├── app/
│ └── main.py # Streamlit UI entry point
│
├── chatbot/
│ ├── chatbot.py # Chatbot logic handler
│ ├── nlp_engine.py # NLP/ML intent classifier
│
├── finance/
│ └── api_handler.py # Handles SIP/FD calculations, NAV scraping, stock/gold price fetch
│
├── data/
│ ├── intents.json # Chatbot intents & responses
│ └── AMFI_NAV.txt # Mutual fund NAVs (downloaded from AMFI)
│
└── README.md # This file

## 🛠️ Installation

1. **Clone the repo**  
```bash
git clone https://github.com/your-username/Investment_chatbot.git
cd Investment_chatbot

Create virtual environment

bash
Copy code
python -m venv venv
venv\Scripts\activate     # On Windows
Install dependencies

bash
Copy code
pip install -r requirements.txt
Download NLTK tokenizer

bash
Copy code
python -c "import nltk; nltk.download('punkt')"
Download latest NAV file
Download NAVAll.txt
→ Save as: data/AMFI_NAV.txt

💻 Run the App
bash
Copy code
streamlit run app/main.py


💬 Example Queries
vbnet
Copy code
You: Where should I invest ₹5000?
Bot: Can you tell me your risk profile and investment duration?

You: SIP for 2000 per month for 5 years at 12%
Bot: Total returns will be ₹164972 with chart 📈

You: FD ₹10000 at 7% for 3 years
Bot: Your FD will grow to ₹12250

You: Stock price of TCS
Bot: ₹ XYZ.XX (as of today)

You: NAV of Axis Bluechip Fund
Bot: ₹42.73 as on 28-Jun-2025


📦 Dependencies
streamlit
pandas
requests
scikit-learn
spacy
nltk
matplotlib
beautifulsoup4

🙌 Acknowledgments
AMFI India for NAV data

Yahoo Finance for stock prices

Streamlit for interactive UI

NLTK and spaCy for NLP