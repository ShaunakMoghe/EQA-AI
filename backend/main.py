# Step 2: Import the Client and Initialize it in main.py
import finnhub
import os
import json
import anthropic
import re
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Load API keys from .env file
load_dotenv()
finnhub_api_key = os.getenv("FINHUB_API_KEY")
claude_api_key = os.getenv("CLAUDE_API_KEY")

# Initialize FastAPI app
app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the Finnhub client
finnhub_client = finnhub.Client(api_key=finnhub_api_key)

# Initialize the Anthropic client
anthropic_client = anthropic.Client(api_key=claude_api_key)

# Function to get user-friendly summary from Claude using the Messages API
def get_user_friendly_summary(raw_data):
    combined_data_str = json.dumps(raw_data)

    response = anthropic_client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1000,
        temperature=0,
        system="You are a highly intelligent assistant designed to transform complex financial data into concise, user-friendly summaries. Your role is to take detailed financial information, including stock prices, market sentiment, sector news, company financials, and insider transactions, and present it in a clear and easy-to-understand format. Focus on simplifying key points, providing context for each data type, and summarizing it in a way that would be accessible to a user without a financial background. Ensure the output is concise, engaging, and actionable, highlighting the most important insights from the data provided. You are to give a final number on a scale of 1-10 including decimal points to indicate your final analysis on the stock, with 5 being neutral outlook, 1 being bad outlook, and 10 being great outlook based on all the data. Use proper chain of thought when you make your decision.",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": f"Give an analysis based on this data: {combined_data_str}"
                    }
                ]
            }
        ]
    )

    # Extracting the content from the response
    if response.content and len(response.content) > 0:
        summary_response = response.content[0].text.strip()
        final_score = extract_final_score(summary_response)
        return summary_response, final_score
    else:
        return "Error: Unexpected response format from Claude.", None

# Function to extract final score from Claude's response
def extract_final_score(claude_response):
    # Use regex to find the score pattern
    match = re.search(r'Final Analysis Score: ([0-9]+(\.[0-9]+)?)/10', claude_response)
    if match:
        return float(match.group(1))
    return None

# Combined endpoint to collect all data and get a summary
@app.get("/combined-summary")
def get_combined_summary(symbol: str, sector: str):
    try:
        # Collect stock quote data
        stock_quote = finnhub_client.quote(symbol)
        stock_data = {
            "symbol": symbol,
            "current_price": stock_quote['c'],
            "high_price": stock_quote['h'],
            "low_price": stock_quote['l'],
            "open_price": stock_quote['o']
        }

        # Collect market sentiment data
        market_news = finnhub_client.general_news("general")[:10]  # Limit to 10 articles to reduce data size
        positive_count = 0
        negative_count = 0

        for article in market_news:
            content = article.get('summary', '').lower()
            if "positive" in content or "gain" in content or "rise" in content:
                positive_count += 1
            elif "negative" in content or "loss" in content or "fall" in content:
                negative_count += 1

        sentiment_score = (positive_count - negative_count) / len(market_news) if market_news else 0
        sentiment = "positive" if sentiment_score > 0 else "negative" if sentiment_score < 0 else "neutral"
        sentiment_data = {
            "total_articles": len(market_news),
            "positive_count": positive_count,
            "negative_count": negative_count,
            "sentiment": sentiment
        }

        # Collect sector-specific news data
        sector_news = finnhub_client.general_news(sector)[:10]  # Limit to 5 articles to reduce data size
        sector_data = {
            "sector": sector,
            "total_articles": len(sector_news),
            "articles": sector_news
        }

        # Collect company financials data
        financials = finnhub_client.company_basic_financials(symbol, 'all')
        financial_data = {
            "symbol": symbol,
            "financials": financials['metric']
        }

        # Collect insider transactions data
        transactions = finnhub_client.stock_insider_transactions(symbol)['data'][:10]  # Limit to 5 transactions to reduce data size
        insider_data = {
            "symbol": symbol,
            "insider_transactions": transactions
        }

        # Combine all data
        combined_data = {
            "stock_data": stock_data,
            "sentiment_data": sentiment_data,
            "sector_data": sector_data,
            "financial_data": financial_data,
            "insider_data": insider_data
        }

        # Get user-friendly summary from Claude
        user_friendly_summary, final_score = get_user_friendly_summary(combined_data)

        return {
            "raw_data": combined_data,
            "user_friendly_summary": user_friendly_summary,
            "final_score": final_score
        }
    except Exception as e:
        return {"error": str(e)}
