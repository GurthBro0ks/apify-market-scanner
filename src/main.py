"""
Main entry point for the Prediction Market Scanner Apify Actor.
Orchestrates the different scrapers based on input configuration.
"""
import asyncio
import json
from typing import Any, Dict

from apify import Actor

from kalshi_scraper import fetch_kalshi_markets
from crypto_prices import fetch_crypto_prices
from sentiment import fetch_sentiment


async def main() -> None:
    """Main actor entry point."""
    async with Actor as actor:
        # Get input
        input_data = await actor.get_input() or {}
        
        # Extract configuration
        scan_kalshi = input_data.get('scanKalshi', True)
        kalshi_categories = input_data.get('kalshiCategories', ['Economics', 'Politics', 'Climate and Weather'])
        scan_crypto = input_data.get('scanCrypto', True)
        crypto_symbols = input_data.get('cryptoSymbols', ['bitcoin', 'ethereum', 'solana'])
        scan_sentiment = input_data.get('scanSentiment', False)
        finnhub_api_key = input_data.get('finnhubApiKey', '')
        sentiment_tickers = input_data.get('sentimentTickers', ['AAPL', 'NVDA', 'TSLA', 'META'])
        max_results = input_data.get('maxResults', 100)
        
        results: Dict[str, Any] = {
            'kalshi_markets': [],
            'crypto_prices': [],
            'sentiment': [],
            'errors': []
        }
        
        actor.log.info('Starting Prediction Market Scanner...')
        
        # Fetch Kalshi markets
        if scan_kalshi:
            try:
                actor.log.info('Fetching Kalshi markets...')
                kalshi_results = await fetch_kalshi_markets(
                    categories=kalshi_categories,
                    max_results=max_results
                )
                results['kalshi_markets'] = kalshi_results
                actor.log.info(f'Found {len(kalshi_results)} markets from Kalshi')
            except Exception as e:
                error_msg = f'Kalshi scrape error: {str(e)}'
                actor.log.error(error_msg)
                results['errors'].append(error_msg)
        
        # Fetch crypto prices
        if scan_crypto:
            try:
                actor.log.info('Fetching crypto prices from CoinGecko...')
                crypto_results = await fetch_crypto_prices(
                    symbols=crypto_symbols
                )
                results['crypto_prices'] = crypto_results
                actor.log.info(f'Fetched {len(crypto_results)} crypto prices')
            except Exception as e:
                error_msg = f'Crypto scrape error: {str(e)}'
                actor.log.error(error_msg)
                results['errors'].append(error_msg)
        
        # Fetch sentiment
        if scan_sentiment:
            if not finnhub_api_key:
                actor.log.warning('Finnhub API key not provided, skipping sentiment scan')
                results['errors'].append('Finnhub API key required for sentiment scan')
            else:
                try:
                    actor.log.info('Fetching news sentiment from Finnhub...')
                    sentiment_results = await fetch_sentiment(
                        api_key=finnhub_api_key,
                        tickers=sentiment_tickers,
                        max_results=max_results
                    )
                    results['sentiment'] = sentiment_results
                    actor.log.info(f'Fetched sentiment for {len(sentiment_results)} tickers')
                except Exception as e:
                    error_msg = f'Sentiment scrape error: {str(e)}'
                    actor.log.error(error_msg)
                    results['errors'].append(error_msg)
        
        # Save results to default dataset
        await actor.push_data(results)
        
        actor.log.info('Prediction Market Scanner completed')


if __name__ == '__main__':
    asyncio.run(main())
