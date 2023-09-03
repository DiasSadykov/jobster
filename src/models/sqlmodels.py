from datetime import datetime
from typing import Optional
from sqlmodel import TEXT, TIMESTAMP, Column, Field, SQLModel, func

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
    created_at: Optional[datetime] = Field(sa_column=Column(TIMESTAMP, nullable=False, server_default=func.now()), default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(sa_column=Column(TIMESTAMP, nullable=False), default_factory=datetime.utcnow)
