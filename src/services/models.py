import uuid
from dataclasses import dataclass

@dataclass
class Vacancy:
    title: str
    url: str
    salary: str = None
    company: str = None
    city: str = None
    source: str = None
    is_new: bool = False
    created_at: int = None
    id: str = None
    tags: str = None

    def __post_init__(self):
        if self.tags:
            init_tags = self.tags.split(",")
            extracted_tags = extract_tags(self)
            self.tags = ",".join(list(set(init_tags + extracted_tags)))
        else:
            self.tags = ",".join(extract_tags(self))
        if not self.tags:
            self.tags = None

def extract_tags(vacancy: Vacancy):
    tags = []
    tags += extract_tag_by_keywords(vacancy, ["cтажер", "trainee", "intern"], "intern")
    tags += extract_tag_by_keywords(vacancy, ["junior"], "junior")
    tags += extract_tag_by_keywords(vacancy, ["senior"], "senior")
    tags += extract_tag_by_keywords(vacancy, ["middle"], "middle")
    tags += extract_tag_by_keywords(vacancy, ["lead", "руководитель"], "lead")
    tags += extract_tag_by_keywords(vacancy, ["product", "продакт", "продукт"], "product")
    tags += extract_tag_by_keywords(vacancy, ["analyst", "аналитик"], "analyst")
    tags += extract_tag_by_keywords(vacancy, ["fullstack", "full stack"], "fullstack")
    tags += extract_tag_by_keywords(vacancy, ["frontend", "front end"], "frontend")
    tags += extract_tag_by_keywords(vacancy, ["backend", "back end"], "backend")
    tags += extract_tag_by_keywords(vacancy, ["системный", "sre"], "sysadmin")
    tags += extract_tag_by_keywords(vacancy, ["devops", "dev ops"], "devops")
    tags += extract_tag_by_keywords(vacancy, ["qa", "q/a", "quality assurance", "тестировщик"], "qa")
    tags += extract_tag_by_keywords(vacancy, ["data"], "data")
    tags += extract_tag_by_keywords(vacancy, ["design", "дизайн", "ux", "ui"], "design")
    tags += extract_tag_by_keywords(vacancy, ["ios", "swift"], "ios")
    tags += extract_tag_by_keywords(vacancy, ["android", "kotlin"], "android")
    tags += extract_tag_by_keywords(vacancy, [".net"], ".net")
    tags += extract_tag_by_keywords(vacancy, ["golang", "go"], "golang")
    tags += extract_tag_by_keywords(vacancy, ["python"], "python")
    tags += extract_tag_by_keywords(vacancy, ["java"], "java")
    tags += extract_tag_by_keywords(vacancy, ["c++"], "c++")
    tags += extract_tag_by_keywords(vacancy, ["c#"], "c#")
    tags += extract_tag_by_keywords(vacancy, ["php"], "php")
    tags += extract_tag_by_keywords(vacancy, ["javascript", "js"], "javascript")
    tags += extract_tag_by_keywords(vacancy, ["react"], "react")
    tags += extract_tag_by_keywords(vacancy, ["node"], "node")
    tags += extract_tag_by_keywords(vacancy, ["sql"], "sql")
    return tags

def check_words_in_title(title: str, words: list[str]):
    return any(word in title.lower() for word in words)

def extract_tag_by_keywords(vacancy: Vacancy, keywords: list[str], tag: str):
    if check_words_in_title(vacancy.title, keywords):
        return [tag]
    return []

@dataclass
class Employer:
    db_name: str
    shown_name: str
    logo: str
