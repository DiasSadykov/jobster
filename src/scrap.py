import asyncio
from db.utils import create_db_if_not_exists
from cron.scrapping_cron import run_scrapping

if __name__ == "__main__":
    create_db_if_not_exists()
    asyncio.run(run_scrapping())

