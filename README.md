# EQA AI - Stock Analysis Tool

## Overview
EQA AI is a web-based application that provides a comprehensive stock analysis tool for investors. Using AI to analyze multiple aspects of stock data, including financial metrics, insider transactions, and market sentiment, EQA AI helps users make informed investment decisions.

The project is built with a Python backend (using FastAPI), a modern JavaScript/HTML/CSS front end, and integrates an AI model to generate insightful stock evaluations.

## Features
- **Stock Price Analysis**: Provides information on the current, high, low, and open prices of a stock.
- **Market Sentiment Analysis**: Analyzes recent news articles to gauge market sentiment.
- **Financial Data**: Analyzes key financial metrics like EPS growth, profitability ratios, and more.
- **Insider Trading Activity**: Displays recent insider transactions and activity.
- **AI-Generated Summary**: Uses an AI model (Claude by Anthropic) to create a user-friendly summary of the stock's outlook and assigns a score from 1-10.

## Tech Stack
- **Backend**: Python (FastAPI) 
- **Frontend**: HTML, CSS, JavaScript (Webflow styling used for a professional UI)
- **AI Integration**: Claude API by Anthropic
- **Financial Data**: Finnhub API
- **Deployment**: Uvicorn server for local development

## Installation
To run this project locally, follow these steps:

1. Clone the repository:
   ```sh
   git clone https://github.com/ShaunakMoghe/EQA-AI.git
   cd EQA-AI
   ```

2. Create a virtual environment:
   ```sh
   python -m venv venv
   ```

3. Activate the virtual environment:
   - On Windows:
     ```sh
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```sh
     source venv/bin/activate
     ```

4. Install the required dependencies:
   ```sh
   pip install -r requirements.txt
   ```

5. Run the backend server:
   ```sh
   uvicorn main:app --reload
   ```

6. Open `eqa.html` in your browser to view the front end and use the stock analysis tool.

## Usage
- Enter a stock symbol and its sector to receive an AI-generated analysis and score.
- The output will include a detailed financial breakdown, sentiment analysis, insider activity, and an overall stock rating.

## Folder Structure
- `backend/`: Contains the Python backend code.
- `frontend/`: Contains the HTML, CSS, and JavaScript files for the front end.
- `requirements.txt`: Lists the Python dependencies for the project.

## Important Notes
- The `.env` file, with placeholder API keys, is included in the repository for convenience.
- Replace the placeholders in `.env` with your own API keys to connect to Anthropic and Finnhub for the project to work.

## Contributing
Feel free to open issues or submit pull requests if you have suggestions or improvements.

## Contact
For any questions or suggestions, please contact [Shaunak Moghe](mailto:shaunakmoghe010@gmail.com).
