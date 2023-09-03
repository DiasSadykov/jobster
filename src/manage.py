import asyncio
import os
import click
from sqlmodel import SQLModel, create_engine
from services.scrappers.vacancy_scrappers import ALL_SCRAPPERS

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
def create_tables_legacy():
    from db.utils import create_db_if_not_exists
    create_db_if_not_exists()

@click.command()
def create_tables_sqlmodel():
    from models.sqlmodels import Company
    engine = create_engine(sqlite_url, echo=True)
    SQLModel.metadata.create_all(engine)

cli.add_command(scrap_now)
cli.add_command(create_tables_legacy)
cli.add_command(create_tables_sqlmodel)

if __name__ == '__main__':
    cli()
    