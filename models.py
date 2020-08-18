from pydantic import BaseModel


class Person(BaseModel):
    id: str
    name: str
    sort_name: str
    email: str


class Organization(BaseModel):
    group_id: str
    name: str
