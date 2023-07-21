import logging
import sys
from typing import Any, Dict, Optional
from pathlib import Path

from allusion.utils import load_json_to_dict

Config = Dict[str, Any]

logger = logging.getLogger(__name__)


class Configuration:
    def __init__(self, args: Dict[str, Any]) -> None:
        self.args = args
        self.config: Dict[str, Any] = {}

    def get_config(self):
        if not self.config:
            self.config = self.load_config()
        return self.config

    def load_config(self) -> Dict[str, Any]:
        config_file: str = self.args["config"]
        try:
            config: Config = load_json_to_dict(config_file)
        except:
            logger.error(
                f"No config file found.\n"
                f"Use the command create-config to get a templated config."
            )
            sys.exit()
        self._process_paths(config)
        self._process_common(config)
        self._process_list_commands(config)
        return config

    def _check_in_args(self, argname) -> bool:
        if argname in self.args and self.args[argname] is not None:
            return True
        return False

    def _args_to_config(
        self, config: Config, argname: str, prepend: Optional[str] = None
    ) -> None:
        if argname in self.args:
            if prepend:
                config.update({argname: f"{prepend}/{self.args[argname]}"})
            else:
                config.update({argname: self.args[argname]})

    def _process_paths(self, config: Config) -> None:
        if "data_folder" in self.args and self.args["data_folder"]:
            config.update({"data_folder": self.args["data_folder"]})
        else:
            config.update({"data_folder": f"{Path.cwd()}/data"})

        sports_file = "sports_file"
        countries_file = "countries_file"
        leagues_file = "leagues_file"
        scraped_data_file = "scraped_data_file"

        if self._check_in_args(sports_file):
            self._args_to_config(config, sports_file, config["data_folder"])
        else:
            config.update({sports_file: f'{config["data_folder"]}/{sports_file}.json'})
        if self._check_in_args(countries_file):
            self._args_to_config(config, countries_file, config["data_folder"])
        else:
            config.update(
                {countries_file: f'{config["data_folder"]}/{countries_file}.json'}
            )
        if self._check_in_args(leagues_file):
            self._args_to_config(config, leagues_file, config["data_folder"])
        else:
            config.update(
                {leagues_file: f'{config["data_folder"]}/{leagues_file}.json'}
            )
        if self._check_in_args(scraped_data_file):
            self._args_to_config(config, scraped_data_file, config["data_folder"])
        else:
            config.update(
                {scraped_data_file: f'{config["data_folder"]}/{scraped_data_file}.csv'}
            )

    def _process_common(self, config: Config) -> None:
        self._args_to_config(config, "not_headless")

    def _process_list_commands(self, config: Config) -> None:
        self._args_to_config(config, "reload_file_data")
        self._args_to_config(config, "data_type")
