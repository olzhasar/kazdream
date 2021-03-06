from typing import Optional

from pydantic import BaseModel


class Person(BaseModel):
    id: str
    name: str
    alias: str
    email: Optional[str]
    group: Optional[str]
    group_id: Optional[str]


class Organization(BaseModel):
    group_id: str
    name: str
