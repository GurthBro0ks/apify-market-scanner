"""
Kalshi prediction market scraper.
Fetches public market data from the Kalshi Trade API.
"""
import asyncio
from typing import Any, Dict, List, Optional

import requests


KALSHI_API_BASE = "https://api.elections.kalshi.com/trade-api/v2"


async def fetch_kalshi_markets(
    categories: Optional[List[str]] = None,
    max_results: int = 100
) -> List[Dict[str, Any]]:
    """
    Fetch prediction market data from Kalshi.
    
    Args:
        categories: List of categories to filter by
        max_results: Maximum number of markets to return
        
    Returns:
        List of market data dictionaries
    """
    if categories is None:
        categories = ['Economics', 'Politics', 'Climate and Weather']
    
    markets = []
    
    try:
        # Fetch series first to get available markets
        series_url = f"{KALSHI_API_BASE}/series"
        headers = {
            'Accept': 'application/json',
            'User-Agent': 'PredictionMarketScanner/1.0'
        }
        
        response = requests.get(series_url, headers=headers, timeout=30)
        response.raise_for_status()
        series_data = response.json()
        
        # Filter series by category if specified
        filtered_series = []
        for series in series_data.get('series', []):
            series_cat = series.get('category', '')
            if any(cat.lower() in series_cat.lower() or series_cat.lower() in cat.lower() 
                   for cat in categories):
                filtered_series.append(series)
        
        # Fetch markets for each series
        for series in filtered_series[:10]:  # Limit to avoid rate limits
            series_ticker = series.get('ticker')
            if not series_ticker:
                continue
                
            try:
                markets_url = f"{KALSHI_API_BASE}/markets"
                params = {
                    'series_ticker': series_ticker,
                    'status': 'active',
                    'limit': min(max_results, 50)
                }
                
                resp = requests.get(markets_url, params=params, headers=headers, timeout=30)
                resp.raise_for_status()
                market_data = resp.json()
                
                for market in market_data.get('markets', []):
                    markets.append({
                        'ticker': market.get('ticker'),
                        'title': market.get('title'),
                        'yes_bid': market.get('yes_bid'),
                        'yes_ask': market.get('yes_ask'),
                        'no_bid': market.get('no_bid'),
                        'no_ask': market.get('no_ask'),
                        'volume_24h': market.get('volume_24h'),
                        'close_time': market.get('close_time'),
                        'status': market.get('status'),
                        'series_ticker': series_ticker
                    })
            except Exception as e:
                # Continue on individual market errors
                continue
            
            # Small delay to avoid rate limiting
            await asyncio.sleep(0.2)
            
    except requests.RequestException as e:
        raise Exception(f"Failed to fetch from Kalshi API: {str(e)}")
    
    # Sort by volume and limit results
    markets.sort(key=lambda x: x.get('volume_24h', 0), reverse=True)
    return markets[:max_results]


async def fetch_single_market(market_ticker: str) -> Optional[Dict[str, Any]]:
    """
    Fetch a single market by ticker.
    
    Args:
        market_ticker: The market ticker symbol
        
    Returns:
        Market data dictionary or None if not found
    """
    headers = {
        'Accept': 'application/json',
        'User-Agent': 'PredictionMarketScanner/1.0'
    }
    
    try:
        url = f"{KALSHI_API_BASE}/markets/{market_ticker}"
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        market = data.get('market', {})
        return {
            'ticker': market.get('ticker'),
            'title': market.get('title'),
            'yes_bid': market.get('yes_bid'),
            'yes_ask': market.get('yes_ask'),
            'no_bid': market.get('no_bid'),
            'no_ask': market.get('no_ask'),
            'volume_24h': market.get('volume_24h'),
            'close_time': market.get('close_time'),
            'status': market.get('status')
        }
    except requests.RequestException:
        return None
