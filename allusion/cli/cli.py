import argparse
from typing import List, Optional, Union

from allusion import __version__
from allusion.cli.cli_options import (
    ARGUMENTS,
    ARGS_COMMON,
    ARGS_LIST,
    ARGS_PATH,
    ARGS_CONFIG,
)


def add_args(
    parser: Union[argparse.ArgumentParser, argparse._ArgumentGroup], options: List[str]
) -> None:
    for option in options:
        opt = ARGUMENTS[option]
        parser.add_argument(*opt.args, **opt.kwargs)


def cli(sysargv: Optional[List] = None):
    # Import here to avoid circular import
    from allusion.cli import create_config, list_data, scrape_once

    common_parser = argparse.ArgumentParser(add_help=False)
    common_group = common_parser.add_argument_group("Common arguments")
    add_args(common_group, ARGS_COMMON)

    path_parser = argparse.ArgumentParser(add_help=False)
    path_group = path_parser.add_argument_group("Path arguments")
    add_args(path_group, ARGS_PATH)

    parser = argparse.ArgumentParser(prog="allusion", description="Sport betting bot")
    parser.add_argument(
        "-V",
        "--version",
        help="Show bots version and exit.",
        action="version",
        version=f"%(prog)s {__version__}",
    )
    subparsers = parser.add_subparsers()

    create_config_command = subparsers.add_parser(
        "create-config",
        help="Create template config",
    )
    create_config_command.set_defaults(func=create_config)
    add_args(create_config_command, ARGS_CONFIG)

    scrape_once_command = subparsers.add_parser(
        "scrape-once",
        help="Get the data and exit.",
        parents=[common_parser, path_parser],
    )
    scrape_once_command.set_defaults(func=scrape_once)

    list_command = subparsers.add_parser(
        "list-data",
        help="Show the available data.",
        parents=[path_parser, common_parser],
    )
    list_command.set_defaults(func=list_data)
    add_args(list_command, ARGS_LIST)

    # run_command = subparsers.add_parser(
    #     "run", help="Start the bot.", parents=[common_parser, path_parser]
    # )

    args = parser.parse_args(sysargv)
    return args


if __name__ == "__main__":
    cli()
