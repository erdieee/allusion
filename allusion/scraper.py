import asyncio
import logging
import re
import time
from datetime import datetime
from typing import Any, Dict, List

import pandas as pd
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright
from playwright.sync_api import sync_playwright

from allusion.constants import countries as available_countries
from allusion.constants import sports as available_sports
from allusion.utils import (
    flatten_dicts,
    load_json_to_dict,
    parse_date,
    store_dict_to_json,
)

logger = logging.getLogger(__name__)


class Scraper:
    main_url = "https://www.oddsportal.com"

    def __init__(self, config) -> None:
        self._config = config
        self._sports_file: str = self._config.get("sports_file")
        self._countries_file: str = self._config.get("countries_file")
        self._leagues_file: str = self._config.get("leagues_file")
        self._sports: Dict[str, str] = {}
        self._countries: Dict[str, Dict[str, str]] = {}
        self._leagues: Dict[str, Dict[str, Dict[str, str]]] = {}
        self.headless = self._config.get("not_headless", True)
        self._force_reload = False

        self.loop = asyncio.get_event_loop()
        asyncio.set_event_loop(self.loop)

    def __repr__(self) -> str:
        return f"Scraper of {self.main_url}"

    @property
    def get_sports(self):
        if not self._sports:
            self._load_sports()
        return self._sports

    @property
    def get_countries(self):
        if not self._countries:
            self._load_countries()
        return self._countries

    @property
    def get_leagues(self):
        if not self._leagues:
            self._load_leagues()
        return self._leagues

    def _load_sports(self) -> None:
        if (
            self._config.get("reload_file_data", None)
            in [
                "all",
                "sports",
            ]
            or self._force_reload
        ):
            logger.info("Reloading sports data...")
            self._sports = self.scrape_sports()
            self._force_reload = True
            self._load_countries()
            return
        try:
            self._sports = load_json_to_dict(self._sports_file)
        except:
            logger.warning(f"File {self._sports_file} not found. Scraping sports now..")
            self._sports = self.scrape_sports()

    def _load_countries(self) -> None:
        if (
            self._config.get("reload_file_data", None)
            in [
                "all",
                "countries",
            ]
            or self._force_reload
        ):
            logger.info("Reloading countries data...")
            self._countries = self.scrape_countries()
            self._force_reload = True
            self._load_leagues()
            return
        try:
            self._countries = load_json_to_dict(self._countries_file)
        except:
            logger.warning(
                f"File {self._countries_file} not found. Scraping sports in countries now.."
            )
            self._countries = self.scrape_countries()

    def _load_leagues(self) -> None:
        if (
            self._config.get("reload_file_data", None)
            in [
                "all",
                "leagues",
            ]
            or self._force_reload
        ):
            logger.info("Reloading leagues data...")
            self._leagues = self.scrape_leagues()
            self._force_reload = False
            return
        try:
            self._leagues = load_json_to_dict(self._leagues_file)
        except:
            logger.warning(
                f"File {self._leagues_file} not found. Scraping leagues now.."
            )
            self._leagues = self.scrape_leagues()

    def scrape_sports(self) -> Dict[str, str]:
        logger.info(f"Getting sports urls and saving into {self._sports_file}")
        sports = {}
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=self.headless)
            context = browser.new_context()
            page = context.new_page()
            page.goto(self.main_url)
            page.wait_for_load_state("networkidle")
            # page.get_by_role("button", name="I Accept").click()
            for sport in page.get_by_role("navigation").locator("li").all():
                try:
                    loc = sport.get_by_role("link")
                    s = loc.inner_text()
                    if s in available_sports and s in self._config["sports"]:
                        sports[s] = f'{self.main_url}{loc.get_attribute("href")}'
                except:
                    break
        store_dict_to_json(sports, self._sports_file)
        return sports

    def scrape_countries(self):
        if not self._sports:
            self._load_sports()
        sports = self._sports
        logger.info(
            f"Getting sports in countries urls and saving into {self._countries_file}"
        )
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=self.headless)
            context = browser.new_context()
            page = context.new_page()
            data = {}
            for sport, sport_url in sports.items():
                page.goto(sport_url)
                page.wait_for_load_state("networkidle")
                # page.get_by_role("button", name="I Accept").click()
                data[sport] = {}
                try:
                    for link in page.get_by_role("link").all():
                        country = link.inner_text()
                        if (
                            country in available_countries
                            and country in self._config["countries"]
                        ):
                            data[sport][
                                country
                            ] = f'{self.main_url}{link.get_attribute("href")}'
                except Exception as e:
                    logger.warning(e)
                    continue
        store_dict_to_json(data, self._countries_file)
        return data

    def scrape_leagues(self):
        if not self._countries:
            self._load_countries()
        data = self._countries
        logger.info(f"Getting leagues and saving into {self._leagues_file}")
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=self.headless)
            context = browser.new_context()
            page = context.new_page()
            temp = {}
            for sport, countries in data.items():
                temp[sport] = {}
                for country, url in countries.items():
                    page.goto(url)
                    page.wait_for_load_state("networkidle")
                    # page.get_by_role("button", name="I Accept").click()
                    temp[sport][country] = {}
                    try:
                        main_div = page.get_by_role("main")
                        for link in main_div.get_by_role("link").all():
                            league = link.inner_text()
                            # print(league)
                            # this should probably be done with a reg expression !!
                            if "(" in league and ")" in league:
                                league = league.split("(")[0].strip()
                                if league not in self._config["leagues"]:
                                    continue
                                temp[sport][country][
                                    league
                                ] = f'{self.main_url}{link.get_attribute("href")}'
                    except Exception as e:
                        logger.warning(e)
                        continue
        store_dict_to_json(temp, self._leagues_file)
        return temp

    async def _get_odds_from_league(self, url, page, sport, country, league, context):
        logger.info(f"Getting odds from {url}")
        await page.goto(url)
        await page.wait_for_load_state("networkidle")
        # page.get_by_role("button", name="I Accept").click()
        main_div = page.get_by_role("main")
        matches = []
        for link in await main_div.get_by_role("link").all():
            match_await = await link.inner_text()
            match = match_await.strip()
            link_await = await link.get_attribute("href")
            # print(match)
            # if re.match(r"^\d", match):
            if re.search(r"-", link_await) and re.search(r"\d", link_await):
                matches.append(f"{self.main_url}{link_await}")
        tmp = {"sport": sport, "country": country, "league": league}
        await page.close()
        tasks = []
        for match in matches:
            page = await context.new_page()
            tasks.append(self._get_odds_from_match(match, page, tmp))
        return await asyncio.gather(*tasks)

    async def _parse_match(self, content, extra_data) -> List[Dict[str, Any]]:
        soup = BeautifulSoup(content, "html.parser")
        data = []
        play_time = (
            "flex text-xs font-normal text-gray-dark font-main item-center gap-1"
        )
        players = "min-md:bg-white-main bg-gray-light mb-3 flex h-auto w-full items-center truncate py-2"
        books = "flex text-xs border-b h-9 border-l border-r"
        time = None
        try:
            time = soup.find("div", class_=play_time).find_all("p")  # type: ignore
            time = "".join([t.text.strip() for t in time])
            time = time.split(",")[1:]
            time = ",".join(time)
            time = parse_date(time)
            match_players = soup.find("div", class_=players).find("p").text  # type: ignore
            parse_home_away = match_players.split("-")
            home_player = parse_home_away[0].strip()
            away_player = parse_home_away[1].strip()
            extra_data.update(
                {
                    "match_time": time,
                    "match": match_players,
                    "home": home_player,
                    "away": away_player,
                }
            )
            books = soup.find_all("div", class_=books)
            for book in books:
                temp = {}
                odds_type = iter(["home_odds", "draw_odds", "away_odds"])
                book_name = ""
                for a in book.find_all("a"):
                    try:
                        book_name = a.find("p").text.split(".")[0]
                    except:
                        continue
                if not book_name:
                    continue
                temp["book"] = book_name.lower()
                temp["update_time"] = datetime.utcnow().isoformat()
                odds = book.find_all("p")
                if any([("line-through" in odd["class"]) for odd in odds]):
                    logger.info(
                        f"Odds for book {book_name} on match {match_players} is outdated. Skipping these odds.."
                    )
                    continue
                for odd in odds:
                    tmp = odd.text
                    if book_name in tmp:
                        continue
                    temp[next(odds_type)] = float(tmp)
                temp.update(extra_data)
                data.append(temp)
        except Exception as e:
            logger.warning(e)
            return []
        return data

    async def _get_odds_from_match(
        self, match, page, extra_data
    ) -> List[Dict[str, Any]]:
        try:
            logger.info(f"Scraping {match}...")
            await page.goto(match)
            await page.wait_for_load_state("networkidle")
            if (
                not await page.locator("span")
                .filter(has_text="1X2")
                .locator("div")
                .is_visible()
            ):
                logger.warning(f"No data found for {match}")
                await page.close()
                return []
            await page.locator("span").filter(has_text="1X2").locator("div").click()
            await page.get_by_text("Full Time", exact=True).click()
            await page.wait_for_load_state("networkidle")
            await page.wait_for_selector("div[data-v-4905fa49]")

            content = await page.content()
            await page.close()
            return await self._parse_match(content, extra_data)

        except Exception as e:
            logger.warning(f"Unable to fetch data from {match}. Returning")
            return []

    async def _scrape_odds(self):
        logger.info("Scraping odds now...")
        data = self._leagues
        logger.debug(f"Getting odds for: {data}")
        results = []
        async with async_playwright() as playwright:
            browser = await playwright.chromium.launch(headless=self.headless)
            context = await browser.new_context()
            for sport, countries in data.items():
                for country, leagues in countries.items():
                    tasks = []
                    for league, url in leagues.items():
                        page = await context.new_page()
                        tasks.append(
                            self._get_odds_from_league(
                                url=url,
                                page=page,
                                sport=sport,
                                country=country,
                                league=league,
                                context=context,
                            )
                        )
                    res = await asyncio.gather(*tasks)
                    results.append(res)

        return results

    def get_odds(self) -> pd.DataFrame:
        if (reload := self._config.get("reload_file_data", None)) is not None:
            if reload == "all":
                self._load_sports()
            else:
                getattr(self, f"_load_{reload}")()
        if not self._leagues:
            self._load_leagues()
        try:
            start_scrape = time.perf_counter()
            odds = self.loop.run_until_complete(self._scrape_odds())
            # print(odds)
            store_dict_to_json(odds, "gather_res.json")  # type: ignore
            end_scrape = time.perf_counter()
            logger.info(f"Scraping odds took {end_scrape - start_scrape:3f} seconds.")
        except Exception as e:
            logger.warning(e)
            return pd.DataFrame()

        odds = flatten_dicts(odds)
        try:
            df = pd.DataFrame(odds)
            logger.debug(f"Datafram after scraping odds:\n {df}")
            return df
        except Exception as e:
            logger.warning(
                f"Could not create dataframe from retrived odds. Error: {e}."
            )
            return pd.DataFrame()
