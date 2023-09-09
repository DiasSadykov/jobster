import asyncio
import sentry_sdk
from services.scrappers.vacancy_scrappers import ALL_CHECKERS, ALL_SCRAPPERS

sentry_sdk.init(
    dsn="https://fad90a96deef9d5a0e009d3d1075414f@o4505853118054400.ingest.sentry.io/4505853119299584",
    traces_sample_rate=1.0,
    profiles_sample_rate=1.0,
)

async def run_scrapping():
    await asyncio.gather(*[scrapper.run() for scrapper in ALL_SCRAPPERS+ALL_CHECKERS])

if __name__ == "__main__":
    asyncio.run(run_scrapping())
