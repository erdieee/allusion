import logging
from pathlib import Path
from typing import Any, Dict

from allusion.utils import store_dict_to_json

logger = logging.getLogger(__name__)


def create_config(args: Dict[str, Any]) -> None:
    config = {
        "not-headless": False,
        "data-folder": f"{Path.cwd()}/data",
        "sports": ["FOOTBALL"],
        "countries": ["England", "Spain", "Italy", "Germany"],
        "leagues": [
            "Premier League",
            "Champions League",
            "LaLiga",
            "Serie A",
            "Bundesliga",
        ],
    }

    store_dict_to_json(config, args["config"])
    logger.info(f'Created new config file at: {args["config"]}')
