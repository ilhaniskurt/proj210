# This is the main script that runs the entire project
# Author: Ilhan Yavuz Iskurt

# Local imports
from utils.config import config
from utils.dl import data_exists
from scrapers import ilo

# International Labour Organization
print("ILO process started!")
if data_exists(config.ILO_DATA):
    print("[ILO] Data cached found! Skipping scrapping.")
else:
    print("[ILO] Data scrapping..")
    ilo.scrape()
    print("[ILO] Data scrapped!")
