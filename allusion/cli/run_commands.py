from typing import Any, Dict
from allusion import scraper

from allusion.configuration import Configuration
from allusion.scraper import Scraper
from allusion.utils import get_df_best_odds, check_arbitrage


def scrape_once(args: Dict[str, Any]) -> None:
    config = Configuration(args).get_config()
    scraper = Scraper(config)
    df = scraper.get_odds()
    df = get_df_best_odds(df)
    print(df)
    df.to_csv(config.get("scraped_data_file"), index=False)
    df = check_arbitrage(df)
    if df.empty:
        print("No arbitrage at the moment")
    else:
        print(df)
