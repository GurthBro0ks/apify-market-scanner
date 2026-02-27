"""
Crypto price fetcher using CoinGecko API.
Fetches current prices, 24h changes, and volume.
"""
import asyncio
from typing import Any, Dict, List

import requests


COINGECKO_API = "https://api.coingecko.com/api/v3"


# Map common symbols to CoinGecko IDs
SYMBOL_TO_ID = {
    'bitcoin': 'bitcoin',
    'btc': 'bitcoin',
    'ethereum': 'ethereum',
    'eth': 'ethereum',
    'solana': 'solana',
    'sol': 'solana',
    'dogecoin': 'dogecoin',
    'doge': 'dogecoin',
    'cardano': 'cardano',
    'ada': 'cardano',
    'ripple': 'ripple',
    'xrp': 'ripple',
    'polkadot': 'polkadot',
    'dot': 'polkadot',
    'litecoin': 'litecoin',
    'ltc': 'litecoin',
}


async def fetch_crypto_prices(symbols: List[str]) -> List[Dict[str, Any]]:
    """
    Fetch cryptocurrency prices from CoinGecko.
    
    Args:
        symbols: List of crypto symbols to fetch
        
    Returns:
        List of crypto price data dictionaries
    """
    if not symbols:
        return []
    
    # Convert symbols to CoinGecko IDs
    coin_ids = []
    for symbol in symbols:
        normalized = symbol.lower().strip()
        coin_id = SYMBOL_TO_ID.get(normalized, normalized)
        if coin_id not in coin_ids:
            coin_ids.append(coin_id)
    
    if not coin_ids:
        return []
    
    try:
        # Build the API call
        url = f"{COINGECKO_API}/coins/markets"
        params = {
            'vs_currency': 'usd',
            'ids': ','.join(coin_ids),
            'order': 'market_cap_desc',
            'per_page': len(coin_ids),
            'page': 1,
            'sparkline': 'false',
            'price_change_percentage': '24h'
        }
        
        headers = {
            'Accept': 'application/json',
            'User-Agent': 'PredictionMarketScanner/1.0'
        }
        
        response = requests.get(url, params=params, headers=headers, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        results = []
        for coin in data:
            results.append({
                'symbol': coin.get('symbol', '').upper(),
                'name': coin.get('name'),
                'price': coin.get('current_price'),
                'change_24h': coin.get('price_change_percentage_24h'),
                'volume': coin.get('total_volume'),
                'market_cap': coin.get('market_cap'),
                'image': coin.get('image'),
                'rank': coin.get('market_cap_rank')
            })
        
        return results
        
    except requests.RequestException as e:
        raise Exception(f"Failed to fetch from CoinGecko: {str(e)}")


async def fetch_single_crypto(symbol: str) -> Dict[str, Any]:
    """
    Fetch price for a single cryptocurrency.
    
    Args:
        symbol: Crypto symbol (e.g., 'bitcoin', 'BTC')
        
    Returns:
        Crypto price data dictionary
    """
    results = await fetch_crypto_prices([symbol])
    return results[0] if results else None
