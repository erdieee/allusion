from pathlib import Path


ARGS_COMMON = ["verbose", "not-headless", "reload-file-data", "config"]
ARGS_PATH = [
    "sports-file",
    "countries-file",
    "leagues-file",
    "scraped-data-file",
    "data-folder",
]
ARGS_LIST = ["data-type"]
ARGS_CONFIG = ["config"]


class Args:
    def __init__(self, *args, **kwargs) -> None:
        self.args = args
        self.kwargs = kwargs


ARGUMENTS = {
    "verbose": Args(
        "-v",
        "--verbose",
        help="Verbose mode",
        action="count",
        default=0,
    ),
    "not-headless": Args(
        "--not-headless",
        help="Brower mode. Default: `%(default)s`",
        action="store_false",
        default=True,
    ),
    "reload-file-data": Args(
        "--reload-file-data",
        help="Reload data in file.",
        choices=["all", "sports", "countries", "leagues"],
    ),
    "sports-file": Args(
        "--sports-file",
        help="Specify the path containing sports:urls.",
        metavar="PATH",
    ),
    "countries-file": Args(
        "--countries-file",
        help="Specify the path containing sports:country:urls.",
        metavar="PATH",
    ),
    "leagues-file": Args(
        "--leagues-file",
        help="Specify the path containing sports:country:leagues:urls.",
        metavar="PATH",
    ),
    "scraped-data-file": Args(
        "--scraped-data-file",
        help="Path to scraped data file. Should end with csv",
        metavar="PATH",
    ),
    "data-folder": Args(
        "--data-folder",
        help="Path to data folder.",
        metavar="PATH",
    ),
    "data-type": Args(
        "--data-type",
        help="Reload data in file. Default: `%(default)s`",
        choices=["sports", "countries", "leagues"],
        default="leagues",
    ),
    "config": Args(
        "--config",
        help=f"Specify config file name.\n Default: `%(default)s`",
        metavar="PATH",
        default=f"{Path.cwd()}/config.json",
    ),
}
