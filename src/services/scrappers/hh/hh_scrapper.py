import asyncio
import re
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

from services.reporting.telegram_reporting_service import TelegramReportingService
from services.scrappers.base.base_vacancy_scrapper import VacancyScrapperBase
from models.sqlmodels import Vacancy

MAX_PAGE = 100

class HHKZVacancyScrapper(VacancyScrapperBase):
    def __init__(self, query, log_tag, hour, minute):
        self.query = query
        super().__init__("https://hh.kz/{query}page={page}", "hh.kz", log_tag, hour=hour, minute=minute)

    async def scrap_page(self, page) -> int:
        url = self.url_base.format(query=self.query, page=page)
        response = await self.client.get(url, follow_redirects=True, timeout=2)
        if response.status_code != 200:
            await TelegramReportingService.send_message_to_private_channel(f"[{self.log_tag}] {response.status_code} on page {url}")
            raise Exception(f"Error {response.status_code} on page {url}")
        vacancies = await self.findData(response)
        return vacancies

    async def scrap(self):
        vacancies = []
        for page in range(0, MAX_PAGE):
            try:
                vacancies.extend(await self.scrap_page(page))
                await asyncio.sleep(1)
            except Exception as e:
                break
        return vacancies

    async def findData(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')
        # Changed the class selector to match the new layout
        vacancies_raw = soup.find_all("div", {"data-qa": re.compile("vacancy-serp__vacancy")})
        
        if not vacancies_raw:
            await TelegramReportingService.send_message_to_private_channel(f"[{self.log_tag}] did not find vacancies on page {response.url}")
            raise Exception(f"[{self.log_tag}] did not find vacancies on page {response.url}")
        
        vacancies = []
        for vacancy_raw in vacancies_raw:
            title_and_url = vacancy_raw.find("h2", {"data-qa": "bloko-header-2"})
            title_and_url = title_and_url.find("a")
            title = title_and_url.find("span", {"data-qa": "serp-item__title"}).text.strip()
            url = title_and_url.get("href")
            url = urljoin(url, urlparse(url).path)

            city = vacancy_raw.find("span", {"data-qa": "vacancy-serp__vacancy-address_narrow"})
            if city:
                city = city.text.strip()
            else:
                city = None
            company = vacancy_raw.find("a", {"data-qa": "vacancy-serp__vacancy-employer"})
            if company:
                company = company.text.strip()
            else:
                company = None
            salary = vacancy_raw.find("span", {"class": re.compile("compensation-text")})
            if salary:
                salary = salary.text.strip()
            else:
                salary = None
            remote = vacancy_raw.find("span", {"data-qa": "vacancy-label-remote-work-schedule"})
            tags = None
            if remote:
                tags = "remote"

            print(f"{title} - {url} - {salary} - {city} - {company} - {tags}")
            vacancies.append(Vacancy(title=title, url=url, salary=salary, company=company, city=city, tags=tags, source=self.source, is_new=True))
        return vacancies