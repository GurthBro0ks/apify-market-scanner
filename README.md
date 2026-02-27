# Prediction Market Scanner

An Apify Actor that scrapes prediction market data from Kalshi, cryptocurrency prices from CoinGecko, and news sentiment from Finnhub.

## Features

- **Kalshi Integration**: Fetch public prediction market odds and volumes
- **Crypto Prices**: Real-time cryptocurrency prices from CoinGecko
- **Sentiment Analysis**: News-based sentiment scoring for stocks via Finnhub

## Input Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `scanKalshi` | boolean | true | Whether to scan prediction markets |
| `kalshiCategories` | array | ["Economics", "Politics", "Climate and Weather"] | Categories to filter |
| `scanCrypto` | boolean | true | Whether to fetch crypto prices |
| `cryptoSymbols` | array | ["bitcoin", "ethereum", "solana"] | Crypto symbols to fetch |
| `scanSentiment` | boolean | false | Whether to fetch news sentiment |
| `finnhubApiKey` | string | "" | Finnhub API key (required for sentiment) |
| `sentimentTickers` | array | ["AAPL", "NVDA", "TSLA", "META"] | Stock tickers for sentiment |
| `maxResults` | integer | 100 | Maximum results per source |

## Getting Started

### Running Locally

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run with sample input:
```bash
python src/main.py
```

### Running on Apify

1. Push to your Apify account:
```bash
apify push prediction-market-sentiment-scanner
```

2. Run via API or Apify Console:
```json
{
  "scanKalshi": true,
  "scanCrypto": true,
  "scanSentiment": false,
  "cryptoSymbols": ["bitcoin", "ethereum", "solana"],
  "maxResults": 50
}
```

## Output Format

```json
{
  "kalshi_markets": [
    {
      "ticker": "KALSHI:ECON",
      "title": "Will CPI exceed 3.5%?",
      "yes_bid": 0.45,
      "yes_ask": 0.47,
      "no_bid": 0.53,
      "no_ask": 0.55,
      "volume_24h": 125000,
      "status": "active"
    }
  ],
  "crypto_prices": [
    {
      "symbol": "BTC",
      "name": "Bitcoin",
      "price": 67500.00,
      "change_24h": 2.5,
      "volume": 35000000000,
      "rank": 1
    }
  ],
  "sentiment": [
    {
      "ticker": "AAPL",
      "sentiment_score": 0.25,
      "sentiment_label": "Bullish",
      "news_count": 15,
      "headlines": [...]
    }
  ],
  "errors": []
}
```

## API Keys

### CoinGecko
- **Free tier**: 10-30 calls/minute
- **No API key required** for basic usage

### Finnhub
- **Free tier**: 60 calls/minute
- Get key at: https://finnhub.io/

### Kalshi
- **Public API**: No authentication required
- Rate limits apply

## Revenue Strategy

### Tiered Access Model

1. **Free Tier** (Apify Free)
   - Limited to 3 major crypto prices
   - Basic sentiment (last 5 headlines)
   - Limited market data

2. **Pro Tier** ($9.99/month)
   - Full crypto portfolio tracking
   - Complete sentiment analysis
   - All prediction markets
   - Webhook notifications
   - 10,000 API runs/month

3. **Enterprise Tier** ($49.99/month)
   - Custom market categories
   - Historical data access
   - Priority support
   - 100,000 API runs/month
   - Custom integrations

### Use Cases for Paying Users

- **Trading Bots**: Automated signal generation
- **Research Tools**: Market sentiment analysis
- **Portfolio Trackers**: Real-time crypto + prediction markets
- **Trading Desks**: Multi-source market intelligence

### Pricing Page Ideas

- Show ROI potential from better market timing
- Feature comparison with competitors (PredictIt, Polymarket APIs)
- Free trial for Pro tier (100 runs)

## License

MIT License - See LICENSE file for details.

## Disclaimer

This tool is for informational purposes only. Not financial advice. 
No live trading - this is a data scraper only.
