import asyncio
import click
from services.scrappers.vacancy_scrappers import ALL_SCRAPPERS

@click.group()
def cli():
    pass

@click.command()
def scrap_now():
    for scrapper in ALL_SCRAPPERS:
        click.echo(f"Running {scrapper.log_tag}")
        asyncio.run(scrapper.run_now())

cli.add_command(scrap_now)

if __name__ == '__main__':
    cli()
    