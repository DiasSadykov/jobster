import asyncio
import time
from services.scrappers.vacancy_scrappers import ALL_SCRAPPERS

async def run_scrapping():
    await asyncio.gather(*[scrapper.run() for scrapper in ALL_SCRAPPERS])



