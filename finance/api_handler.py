import yfinance as yf
import requests
from bs4 import BeautifulSoup
import datetime
import re
import matplotlib.pyplot as plt
import io
import base64


def get_gold_price():
    try:
        today = datetime.datetime.today().weekday()
        if today >= 5:  # 5 = Saturday, 6 = Sunday
            return "Markets are closed on weekends. Try again on a weekday for live gold prices."

        url = "https://www.mcxindia.com/market-data/commodity-futures"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        rows = soup.find_all("tr")
        for row in rows:
            if "GOLD" in row.text and "Mini" not in row.text:
                cols = row.find_all("td")
                if cols and len(cols) > 2:
                    contract = cols[0].text.strip()
                    last_price = cols[1].text.strip()
                    return f"The current MCX Gold ({contract}) price is ₹{last_price} per 10g."

        return "Sorry, couldn't find the gold price at the moment."

    except Exception as e:
        return "Sorry, I couldn't fetch the current gold price right now."

# Add more tickers if needed
name_to_symbol = {
    "RELIANCE": "RELIANCE.NS",
    "TCS": "TCS.NS",
    "INFOSYS": "INFY.NS",
    "HDFC": "HDFCBANK.NS",
    "HDFC BANK": "HDFCBANK.NS",
    "NIFTY": "^NSEI",
    "NIFTY 50": "^NSEI",
    "SENSEX": "^BSESN",
    "BSE": "^BSESN"
}

def get_stock_price(query):
    query = query.upper()

    # Try to find any known name inside the query
    for name, symbol in name_to_symbol.items():
        if name in query:
            try:
                stock = yf.Ticker(symbol)
                price = stock.history(period="1d")["Close"].iloc[-1]
                return f"The current price of {name} is ₹{round(price, 2)}."
            except:
                return f"Sorry, I couldn’t fetch the stock price for {name}."

    return "Sorry, I couldn’t understand which stock or index you’re asking about."

def calculate_sip(query):
    try:
        # Extract ₹ amount, years, interest
        numbers = [int(x) for x in re.findall(r'\d+', query)]
        if len(numbers) < 3:
            return "Please provide monthly investment, years, and interest rate like: ₹2000 per month for 5 years at 12%."

        monthly_investment = numbers[0]
        years = numbers[1]
        rate = numbers[2]

        r = rate / 100 / 12  # monthly interest
        n = years * 12       # total months

        # SIP formula
        fv = monthly_investment * (((1 + r) ** n - 1) * (1 + r)) / r
        total_invested = monthly_investment * n
        interest_earned = fv - total_invested

        # Generate month-wise values for chart
        values = []
        for i in range(1, n + 1):
            amount = monthly_investment * (((1 + r) ** i - 1) * (1 + r)) / r
            values.append(amount)

        # Plot chart using matplotlib
        plt.figure(figsize=(6, 4))
        plt.plot(range(1, n + 1), values, color='green')
        plt.title("SIP Growth Over Time")
        plt.xlabel("Months")
        plt.ylabel("Investment Value (₹)")
        plt.grid(True)

        # Convert plot to base64 to send to Streamlit
        buf = io.BytesIO()
        plt.tight_layout()
        plt.savefig(buf, format="png")
        buf.seek(0)
        image_base64 = base64.b64encode(buf.read()).decode("utf-8")
        buf.close()

        summary = (
            f"📈 SIP Investment Summary:\n\n"
            f"• Monthly Investment: ₹{monthly_investment}\n"
            f"• Duration: {years} years ({n} months)\n"
            f"• Expected Annual Return: {rate}%\n\n"
            f"✅ Total Invested: ₹{total_invested}\n"
            f"💰 Interest Earned: ₹{round(interest_earned, 2)}\n"
            f"🏁 Maturity Amount: ₹{round(fv, 2)}"
        )

        return summary, image_base64

    except Exception as e:
        return "Sorry, couldn't calculate SIP returns. Format: ₹2000 per month for 5 years at 12%."



def calculate_fd(query):
    try:
        # Parse numbers: principal, rate, years
        numbers = [float(x) for x in re.findall(r'\d+(?:\.\d+)?', query)]
        if len(numbers) < 3:
            return "Please provide principal, rate, and years. Ex: FD for ₹50000 at 6.5% for 5 years"

        principal, rate, years = numbers[0], numbers[1], numbers[2]

        # Compute maturity and interest
        r = rate / 100
        maturity = principal * ((1 + r) ** years)
        interest = maturity - principal

        # Build year-by-year balances
        balances = []
        for y in range(0, int(years) + 1):
            balances.append(principal * ((1 + r) ** y))

        # Plot
        plt.figure(figsize=(6, 4))
        plt.plot(range(0, int(years) + 1), balances)
        plt.title("FD Growth Over Time")
        plt.xlabel("Years")
        plt.ylabel("Balance (₹)")
        plt.grid(True)

        # Encode image
        buf = io.BytesIO()
        plt.tight_layout()
        plt.savefig(buf, format="png")
        buf.seek(0)
        img_b64 = base64.b64encode(buf.read()).decode("utf-8")
        buf.close()
        plt.close()

        # Text summary
        text = (
            f"🏦 Fixed Deposit Summary:\n\n"
            f"• Principal Amount: ₹{principal}\n"
            f"• Duration: {years} years\n"
            f"• Annual Interest Rate: {rate}%\n\n"
            f"✅ Interest Earned: ₹{round(interest, 2)}\n"
            f"💰 Maturity Amount: ₹{round(maturity, 2)}"
        )
        return text, img_b64

    except Exception:
        return ("Sorry, couldn't calculate FD. Try format: FD for ₹50000 at 6.5% for 5 years", None)
    
    
    # Pick last word as fallback
    last_word = words[-1]
    symbol = name_to_symbol.get(last_word, last_word)

    try:
        stock = yf.Ticker(symbol)
        price = stock.history(period="1d")["Close"].iloc[-1]
        return f"The current price of {symbol} is ₹{round(price, 2)}."
    except Exception as e:
        return "Sorry, I couldn’t fetch the stock price. Please check the name or try a different one."
