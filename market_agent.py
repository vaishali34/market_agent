import requests
import os
from groq import Groq

# ============ KEYS FROM ENVIRONMENT ============
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
BOT_TOKEN = os.environ.get("MARKET_BOT_TOKEN")
CHAT_ID = os.environ.get("MARKET_CHAT_ID")
# ===============================================

groq_client = Groq(api_key=GROQ_API_KEY)

def send_telegram(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": CHAT_ID, "text": text, "parse_mode": "HTML"})
    print("Message sent!")

def get_market_data():
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        url = "https://query1.finance.yahoo.com/v8/finance/chart/%5ENSEI?interval=1d"
        r = requests.get(url, headers=headers)
        nifty = r.json()["chart"]["result"][0]["meta"]["regularMarketPrice"]
        nifty = f"{nifty:,.2f}"
    except:
        nifty = "N/A"

    try:
        url2 = "https://query1.finance.yahoo.com/v8/finance/chart/%5EBSESN?interval=1d"
        r2 = requests.get(url2, headers=headers)
        sensex = r2.json()["chart"]["result"][0]["meta"]["regularMarketPrice"]
        sensex = f"{sensex:,.2f}"
    except:
        sensex = "N/A"

    try:
        url3 = "https://query1.finance.yahoo.com/v8/finance/chart/USDINR=X?interval=1d"
        r3 = requests.get(url3, headers=headers)
        usdinr = r3.json()["chart"]["result"][0]["meta"]["regularMarketPrice"]
        usdinr = f"{usdinr:,.2f}"
    except:
        usdinr = "N/A"

    return {"nifty": nifty, "sensex": sensex, "usdinr": usdinr}

def analyze_with_groq(data):
    response = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": f"""You are an Indian stock market expert.
Give a morning brief based on:
- Nifty 50: {data['nifty']}
- Sensex: {data['sensex']}
- USD/INR: {data['usdinr']}

Include:
1. Market sentiment (Bullish/Bearish/Neutral)
2. Key levels to watch
3. 2-3 things to watch today
Keep it under 150 words."""}]
    )
    return response.choices[0].message.content

def main():
    print("Fetching market data...")
    data = get_market_data()
    print(f"Nifty: {data['nifty']} | Sensex: {data['sensex']} | USD/INR: {data['usdinr']}")

    analysis = analyze_with_groq(data)

    message = f"""🌅 <b>Market Morning Brief</b>

📈 <b>Nifty 50:</b> {data['nifty']}
📊 <b>Sensex:</b> {data['sensex']}
💵 <b>USD/INR:</b> {data['usdinr']}

🤖 <b>AI Analysis:</b>
{analysis}"""

    send_telegram(message)
    print("Done!")

main()