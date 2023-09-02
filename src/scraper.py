import asyncio
from db.utils import create_db_if_not_exists
from services.scrappers.vacancy_scrappers import ALL_CHECKERS, ALL_SCRAPPERS

async def run_scrapping():
    await asyncio.gather(*[scrapper.run() for scrapper in ALL_SCRAPPERS+ALL_CHECKERS])

if __name__ == "__main__":
    create_db_if_not_exists()
    asyncio.run(run_scrapping())
