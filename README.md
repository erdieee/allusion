# Sport betting scraper

Scrape all desired sports and odds from [Oddsportal](https://www.oddsportal.com/). Furthermore you can check for arbitrage opportunities.



## Example scraped data
Example output of scrape-once
![Example output of scrape-once](./img/example_scrape.png)

After saving the dataframe, you can take a deeper look and manipulate it in a jupyter notebook.

You can take a look at the process of scraping the odds by providing the `not-headless` option. Check out the commands 
## Commands
List available commands with

```bash
python3 allusion --help
```
Output:
```
usage: allusion [-h] [-V] {create-config,scrape-once,list-data} ...

Sport betting bot

positional arguments:
  {create-config,scrape-once,list-data}
    create-config       Create template config
    scrape-once         Get the data and exit.
    list-data           Show the available data.

options:
  -h, --help            show this help message and exit
  -V, --version         Show bots version and exit.
```

## Install
Clone the repo and run
```bash
python3 -m pip install -r requirements.txt
python3 -m playwright install
```

You will need to create a config file.

**Note**: It is recommended to use a [virtual environment](https://docs.python.org/3/library/venv.html).
