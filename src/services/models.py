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

@dataclass
class Employer:
    db_name: str
    shown_name: str
    logo: str
