from .hh.hh_scrapper import HHKZVacancyScrapper
from .hh.hh_checker import HHKZVacancyChecker

ALL_SCRAPPERS = [
                    HHKZVacancyScrapper("search/vacancy?text=Qa&from=suggest_post&salary=&ored_clusters=true&area=40&items_on_page=20&", "hh.kz qa", hour=23, minute=00),
                    HHKZVacancyScrapper("search/vacancy?text=Product+Manager&salary=&no_magic=true&ored_clusters=true&area=40&items_on_page=20&", "hh.kz product manager", hour=23, minute=5),
                    HHKZVacancyScrapper("search/vacancy?text=Devops&from=suggest_post&salary=&no_magic=true&ored_clusters=true&area=40&items_on_page=20&", "hh.kz devops", hour=23, minute=10),
                    HHKZVacancyScrapper("search/vacancy?text=Data+analyst&salary=&no_magic=true&ored_clusters=true&area=40&items_on_page=20&", "hh.kz data analyst", hour=23, minute=15),
                    HHKZVacancyScrapper("search/vacancy?text=Data+scientist&from=suggest_post&salary=&no_magic=true&ored_clusters=true&area=40&items_on_page=20&", "hh.kz data scientist", hour=23, minute=20),
                    HHKZVacancyScrapper("vacancies/programmist?", "hh.kz programmer", hour=23, minute=25),
                    HHKZVacancyScrapper("vacancies/dizajner-interfejsov?", "hh.kz designer", hour=23, minute=30),
                    HHKZVacancyScrapper("vacancies/sistemnyy_administrator?", "hh.kz sysadmin", hour=23, minute=35),
                    HHKZVacancyChecker()
            ]