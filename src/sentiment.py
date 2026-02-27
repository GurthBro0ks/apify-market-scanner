"""
News sentiment fetcher using Finnhub API.
Fetches news and calculates sentiment scores for stocks.
"""
import asyncio
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

import requests


FINNHUB_API_BASE = "https://finnhub.io/api/v1"


# Sentiment keywords for basic analysis
POSITIVE_KEYWORDS = [
    'surge', 'soar', 'rally', 'gain', 'profit', 'beat', 'upgrade', 'bullish',
    'growth', 'increase', 'rise', 'higher', 'positive', 'optimistic', 'breakout'
]
NEGATIVE_KEYWORDS = [
    'crash', 'plunge', 'drop', 'fall', 'loss', 'miss', 'downgrade', 'bearish',
    'decline', 'decrease', 'lower', 'negative', 'pessimistic', 'sell', 'warning'
]


async def fetch_sentiment(
    api_key: str,
    tickers: List[str],
    max_results: int = 100
) -> List[Dict[str, Any]]:
    """
    Fetch news sentiment for given stock tickers from Finnhub.
    
    Args:
        api_key: Finnhub API key
        tickers: List of stock ticker symbols
        max_results: Maximum number of news items per ticker
        
    Returns:
        List of sentiment data dictionaries
    """
    if not api_key or not tickers:
        return []
    
    headers = {
        'Accept': 'application/json',
        'User-Agent': 'PredictionMarketScanner/1.0'
    }
    
    results = []
    
    # Calculate date range (last 7 days)
    end_date = datetime.now()
    start_date = end_date - timedelta(days=7)
    
    for ticker in tickers:
        try:
            # Fetch company news
            url = f"{FINNHUB_API_BASE}/news"
            params = {
                'category': 'general',
                'token': api_key,
                'symbol': ticker.upper()
            }
            
            response = requests.get(url, params=params, headers=headers, timeout=30)
            response.raise_for_status()
            news_data = response.json()
            
            if not news_data or not isinstance(news_data, list):
                continue
            
            # Analyze sentiment
            headlines = [item.get('headline', '') for item in news_data[:max_results]]
            sentiment_score = calculate_sentiment(headlines)
            
            results.append({
                'ticker': ticker.upper(),
                'sentiment_score': sentiment_score,
                'sentiment_label': get_sentiment_label(sentiment_score),
                'news_count': len(headlines),
                'headlines': headlines[:10],  # Top 10 headlines
                'latest_headline': headlines[0] if headlines else None,
                'timestamp': datetime.now().isoformat()
            })
            
            # Rate limit delay
            await asyncio.sleep(0.5)
            
        except requests.RequestException as e:
            # Log but continue with other tickers
            continue
    
    return results


def calculate_sentiment(headlines: List[str]) -> float:
    """
    Calculate sentiment score from headlines.
    
    Args:
        headlines: List of news headlines
        
    Returns:
        Sentiment score between -1 (very negative) and 1 (very positive)
    """
    if not headlines:
        return 0.0
    
    positive_count = 0
    negative_count = 0
    
    for headline in headlines:
        headline_lower = headline.lower()
        
        for keyword in POSITIVE_KEYWORDS:
            if keyword in headline_lower:
                positive_count += 1
                break
        
        for keyword in NEGATIVE_KEYWORDS:
            if keyword in headline_lower:
                negative_count += 1
                break
    
    total = positive_count + negative_count
    if total == 0:
        return 0.0
    
    # Score between -1 and 1
    score = (positive_count - negative_count) / max(len(headlines), 1)
    return max(-1.0, min(1.0, score))


def get_sentiment_label(score: float) -> str:
    """
    Get human-readable sentiment label from score.
    
    Args:
        score: Sentiment score
        
    Returns:
        Sentiment label string
    """
    if score >= 0.3:
        return 'Bullish'
    elif score >= 0.1:
        return 'Slightly Bullish'
    elif score <= -0.3:
        return 'Bearish'
    elif score <= -0.1:
        return 'Slightly Bearish'
    else:
        return 'Neutral'


async def fetch_market_news(api_key: str, category: str = 'general') -> List[Dict[str, Any]]:
    """
    Fetch general market news from Finnhub.
    
    Args:
        api_key: Finnhub API key
        category: News category (general, forex, crypto, merger)
        
    Returns:
        List of market news items
    """
    headers = {
        'Accept': 'application/json',
        'User-Agent': 'PredictionMarketScanner/1.0'
    }
    
    try:
        url = f"{FINNHUB_API_BASE}/news"
        params = {
            'category': category,
            'token': api_key
        }
        
        response = requests.get(url, params=params, headers=headers, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        return [
            {
                'headline': item.get('headline'),
                'source': item.get('source'),
                'url': item.get('url'),
                'datetime': item.get('datetime')
            }
            for item in data[:20]
        ]
        
    except requests.RequestException:
        return []
