from datetime import datetime
from typing import Optional
from sqlmodel import TEXT, Column, Field, SQLModel

class Company(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(sa_column=Column(TEXT))
    description: Optional[str] = Field(sa_column=Column(TEXT), default=None)
    company_type: Optional[str] = Field(sa_column=Column(TEXT), default=None)
    industry: Optional[str] = Field(sa_column=Column(TEXT), default=None)
    stack: Optional[str] = Field(sa_column=Column(TEXT), default=None)
    logo_url: Optional[str] = Field(sa_column=Column(TEXT), default=None)
    website_url: Optional[str] = Field(sa_column=Column(TEXT), default=None)
    reviwed: Optional[bool] = Field(default=False)
    created_at: Optional[int] = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: Optional[int] = Field(default_factory=datetime.utcnow, nullable=False)

