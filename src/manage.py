import asyncio
import os
import click
from sqlmodel import SQLModel, Session, create_engine
from models.sqlmodels import Vacancy
from services.reporting.telegram_reporting_service import TelegramReportingService
from services.scrappers.vacancy_scrappers import ALL_SCRAPPERS
from db.utils import engine

DATABASE_LOCATION = os.environ.get("DATABASE_LOCATION") or "db.sqlite3"
sqlite_url = f"sqlite:///{DATABASE_LOCATION}"

@click.group()
def cli():
    pass

@click.command()
def scrap_now():
    for scrapper in ALL_SCRAPPERS:
        click.echo(f"Running {scrapper.log_tag}")
        asyncio.run(scrapper.run_now())

@click.command()
def create_tables_sqlmodel():
    from db.utils import engine
    SQLModel.metadata.create_all(engine)

@click.command()
def send_announcement():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    with Session(engine) as session:
        loop.run_until_complete(TelegramReportingService.report_added_vacancies_by_company_sorted(session, private=True))
        session.query(Vacancy).update({Vacancy.is_new: False})
        session.commit()

cli.add_command(scrap_now)
cli.add_command(create_tables_sqlmodel)
cli.add_command(send_announcement)

if __name__ == '__main__':
    cli()
    