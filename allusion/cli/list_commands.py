import sys
from typing import Any, Dict

from rich import print

from allusion.configuration import Configuration
from allusion.scraper import Scraper
from allusion.utils import load_json_to_dict


def print_data(data, data_type) -> None:
    if data_type == "sports":
        print("[bold red]Sports")
        print("------")
        print(list(data.keys()))
    if data_type == "countries":
        for sport, countries in data.items():
            print(f"[bold red]Sport: {sport}")
            print(list(countries.keys()))
            print("-" * 20)
    if data_type == "leagues":
        for sport, countries in data.items():
            print(f"[bold red]Sport: {sport}")
            print("-" * 30)
            for country, leagues in countries.items():
                print(f"[bold blue]Country: {country}")
                print(list(leagues.keys()))
                print("-" * 10)


def reload_data(config) -> None:
    scraper = Scraper(config)
    reload_type = config.get("reload_file_data", None)
    if reload_type == "all":
        scraper._load_sports()
        scraper._load_countries()
        scraper._load_leagues()
    else:
        getattr(scraper, f"_load_{reload_type}")()


def list_data(args: Dict[str, Any]) -> None:
    config = Configuration(args).get_config()
    if config.get("reload_file_data", None):
        reload_data(config)
    data_type = config.get("data_type")
    path = config.get(f"{data_type}_file", "")
    try:
        data = load_json_to_dict(path)
        print(f"Showing data from {path}")
        print_data(data, data_type)
    except:
        print(
            f"Could not load [bold red]{data_type}[/bold red] data.\n"
            f"Either provide --data-type (default: leagues) and "
            f"make sure the file {path} exists or retry with --reload-file-data"
        )
        sys.exit()
