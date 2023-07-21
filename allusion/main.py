import logging
import sys
from typing import List, Optional

from allusion.cli import cli

# sports_file = "./data/sports.json"
# countries_file = "./data/countries.json"
# leagues_file = "./data/leagues.json"
# main_url = "https://www.oddsportal.com"
# df_file = "./data/dataframe.csv"


logger = logging.getLogger("allusion")


# def get_urls():
#     try:
#         sports = load_json_to_dict(sports_file)
#         print(f"Loaded sport urls from {sports_file}")
#     except:
#         print(f"Could not find {sports_file}, loading data..")
#         sports = Scraper.get_sports(Scraper.main_url, sports_file)
#     # sports = dict(list(sports.items())[0:1])
#     print(f"Using sports: {sports}")
#     try:
#         data = load_json_to_dict(countries_file)
#         print(f"Loaded data urls from {countries_file}")
#     except:
#         print(f"Could not find {countries_file}, loading data..")
#         data = get_sports_in_country(sports)
#     temp = {}
#     for sport, countries in data.items():
#         if sport in ["FOOTBALL"]:
#             temp[sport] = {}
#             for country, url in countries.items():
#                 if country in ["England", "Germany", "Italy", "Spain"]:
#                     temp[sport][country] = url
#     data = temp
#     print(f"Using data: {data}")
#     try:
#         leagues = load_json_to_dict(leagues_file)
#         print(f"Loaded data urls from {leagues_file}")
#     except:
#         print(f"Could not find {leagues_file}, loading data..")
#         leagues = get_leagues(data)
#     print(f"Using leagues: {leagues}")
#     return leagues


def main(sysargv: Optional[List] = None):
    # data = get_urls()
    # print(f"Available leagues {data}")
    # temp = {}
    # for sport, countries in data.items():
    #     if sport in ["FOOTBALL"]:
    #         temp[sport] = {}
    #         for country, leagues in countries.items():
    #             if country in ["Italy", "Spain", "England"]:
    #                 temp[sport][country] = {}
    #                 for league, url in leagues.items():
    #                     if league in ["Serie A", "LaLiga", "Premier League"]:
    #                         temp[sport][country][league] = url
    # data = temp
    # print(f"Using leagues {data}")
    # try:
    #     df = pd.read_csv(df_file)
    # except:
    #     df = get_odds(data)
    #     if df.empty:
    #         return
    #     print(df)
    #     df.to_csv("dataframe.csv", index=False)
    # df = get_df_best_odds(df)
    # print(df)
    # df = check_arbitrage(df)
    # if df.empty:
    #     print("no arbitrage found")
    #     return
    # print(df)
    try:
        args = vars(cli(sysargv))
        LOGFORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        logging.basicConfig(level=20, format=LOGFORMAT)
        # print(args)
        if "func" in args:
            args["func"](args)
        else:
            raise Exception(
                "Command is needed\n"
                "Run allusion --help to view all available commands."
            )
    except KeyboardInterrupt:
        logger.info("SIGINT received, aborting ...")
    except Exception as e:
        logger.warning(e)
    finally:
        sys.exit()


if __name__ == "__main__":
    main()
