from datetime import datetime

import yfinance as yf
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm


# Use local Ollama model
local_model = LiteLlm(model="ollama_chat/mistral:latest")


def get_stock_price(ticker: str) -> dict:
    """
    Fetch latest stock price using yfinance.

    This function:
    - Takes stock ticker like TSLA, AAPL
    - Fetches price from Yahoo Finance
    - Returns structured response
    """

    try:
        stock = yf.Ticker(ticker)

        # Try main price field
        current_price = stock.info.get("currentPrice")

        # Fallback if missing
        if current_price is None:
            current_price = getattr(stock.fast_info, "last_price", None)

        # If still missing
        if current_price is None:
            return {
                "status": "error",
                "ticker": ticker.upper(),
                "message": f"Could not fetch price for {ticker}",
            }

        # Current timestamp
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        return {
            "status": "success",
            "ticker": ticker.upper(),
            "price": current_price,
            "timestamp": current_time,
        }

    except Exception as e:
        return {
            "status": "error",
            "ticker": ticker.upper(),
            "message": f"Error fetching stock data: {str(e)}",
        }


# Create stock analyst agent
stock_analyst = Agent(
    name="stock_analyst",
    model=local_model,
    description="Agent that fetches stock prices using a tool.",
    instruction="""
You are a stock market assistant.

Your job:
When user asks about stock price:
- Extract correct ticker symbol
- Call get_stock_price tool

Important:
- Do not guess price yourself
- Always use tool for stock queries

Examples:
Apple -> AAPL
Tesla -> TSLA
Microsoft -> MSFT
Google -> GOOGL
Nvidia -> NVDA

After tool returns:
- Show ticker
- Show price
- Show timestamp

If tool fails:
- Tell user clearly
""",
    tools=[get_stock_price],
)


# REQUIRED for ADK Web
root_agent = stock_analyst