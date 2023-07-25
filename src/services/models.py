from dataclasses import dataclass

@dataclass
class Vacancy:
    title: str
    url: str
    salary: str = None
    company: str = None
    city: str = None
    source: str = None
    created_at: int = None

@dataclass
class Employer:
    name: str
    logo: str
