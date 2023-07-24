import logging
import sys
from typing import List, Optional

from allusion.cli import cli


logger = logging.getLogger("allusion")


def main(sysargv: Optional[List] = None):
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
