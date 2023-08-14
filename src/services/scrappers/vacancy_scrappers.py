from .hh.hh_scrapper import HHKZVacancyScrapper
from .hh.hh_checker import HHKZVacancyChecker

START_HOUR = 21
START_MINUTE = 40
ALL_SCRAPPERS = [
                    HHKZVacancyScrapper("search/vacancy?text=Qa&from=suggest_post&salary=&ored_clusters=true&area=40&items_on_page=20&", "hh.kz qa", hour=START_HOUR, minute=START_MINUTE+2),
                    HHKZVacancyScrapper("search/vacancy?text=Product+Manager&salary=&no_magic=true&ored_clusters=true&area=40&items_on_page=20&", "hh.kz product manager", hour=START_HOUR, minute=START_MINUTE+4),
                    HHKZVacancyScrapper("search/vacancy?text=Devops&from=suggest_post&salary=&no_magic=true&ored_clusters=true&area=40&items_on_page=20&", "hh.kz devops", hour=START_HOUR, minute=START_MINUTE+6),
                    HHKZVacancyScrapper("search/vacancy?text=Data+analyst&salary=&no_magic=true&ored_clusters=true&area=40&items_on_page=20&", "hh.kz data analyst", hour=START_HOUR, minute=START_MINUTE+8),
                    HHKZVacancyScrapper("search/vacancy?text=Data+scientist&from=suggest_post&salary=&no_magic=true&ored_clusters=true&area=40&items_on_page=20&", "hh.kz data scientist", hour=START_HOUR, minute=START_MINUTE+10),
                    HHKZVacancyScrapper("vacancies/programmist?", "hh.kz programmer", hour=START_HOUR, minute=START_MINUTE+12),
                    HHKZVacancyScrapper("vacancies/dizajner-interfejsov?", "hh.kz designer", hour=START_HOUR, minute=START_MINUTE+14),
                    HHKZVacancyScrapper("vacancies/sistemnyy_administrator?", "hh.kz sysadmin", hour=START_HOUR, minute=START_MINUTE+16),
                    HHKZVacancyChecker()
            ]