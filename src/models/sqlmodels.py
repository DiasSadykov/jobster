from datetime import datetime
from typing import Optional
from sqlmodel import INTEGER, TEXT, TIMESTAMP, Column, Field, SQLModel, func

class Company(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(sa_column=Column(TEXT, nullable=False))
    description: Optional[str] = Field(sa_column=Column(TEXT), default=None)
    headcount: Optional[int] = Field(sa_column=Column(TEXT), default=None)
    type: Optional[str] = Field(sa_column=Column(TEXT), default=None)
    industry: Optional[str] = Field(sa_column=Column(TEXT), default=None)
    tech_stack: Optional[str] = Field(sa_column=Column(TEXT), default=None)
    logo_url: Optional[str] = Field(sa_column=Column(TEXT), default=None)
    website_url: Optional[str] = Field(sa_column=Column(TEXT), default=None)
    reviwed_at: Optional[datetime] = Field(sa_column=Column(TIMESTAMP), default=None)
    created_at: datetime = Field(sa_column=Column(TIMESTAMP, nullable=False, server_default=func.now()), default_factory=datetime.utcnow)
    updated_at: datetime = Field(sa_column=Column(TIMESTAMP, nullable=False), default_factory=datetime.utcnow)

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(sa_column=Column(TEXT, nullable=False, unique=True))
    password: str = Field(sa_column=Column(TEXT, nullable=False))
    user_type: str = Field(sa_column=Column(TEXT, nullable=False))
    balance: int = Field(sa_column=Column(INTEGER), default=0)
    created_at: datetime = Field(sa_column=Column(TIMESTAMP, nullable=False, server_default=func.now()), default_factory=datetime.utcnow)

class Vacancy(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(sa_column=Column(TEXT, nullable=False))
    description: str = Field(sa_column=Column(TEXT))
    url: str = Field(sa_column=Column(TEXT))
    salary: str = Field(sa_column=Column(TEXT))
    company: str = Field(sa_column=Column(TEXT))
    city: str = Field(sa_column=Column(TEXT))
    source: str = Field(sa_column=Column(TEXT))
    tags: str = Field(sa_column=Column(TEXT))
    created_by: int = None
    created_at: datetime = Field(sa_column=Column(TIMESTAMP, nullable=False, server_default=func.now()), default_factory=datetime.utcnow)
    is_new: bool = False

    def __init__(self, **kw):
        super().__init__(**kw)
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
    tags += extract_tag_by_keywords(vacancy, ["java"], "java_")
    tags += extract_tag_by_keywords(vacancy, ["c++"], "c++")
    tags += extract_tag_by_keywords(vacancy, ["c#"], "c#")
    tags += extract_tag_by_keywords(vacancy, ["php"], "php")
    tags += extract_tag_by_keywords(vacancy, ["javascript", "js"], "javascript")
    tags += extract_tag_by_keywords(vacancy, ["react"], "react")
    tags += extract_tag_by_keywords(vacancy, ["node"], "node")
    tags += extract_tag_by_keywords(vacancy, ["sql"], "sql")

    if "javascript" in tags and "java_" in tags:
        tags.remove("java_")
    return tags

def check_words_in_title(title: str, words: list[str]):
    return any(word in title.lower() for word in words)

def extract_tag_by_keywords(vacancy: Vacancy, keywords: list[str], tag: str):
    if check_words_in_title(vacancy.title, keywords):
        return [tag]
    return []
