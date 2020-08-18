from typing import List

from fastapi import FastAPI, HTTPException

from elasticsearch import Elasticsearch
from models import Organization, Person

app = FastAPI()
es = Elasticsearch()


def get_list(index):
    res = es.search(index=index, filter_path=["hits.hits._source"],)
    records = [r["_source"] for r in res["hits"]["hits"]]
    return records


def get_item(index, query={}):
    res = es.search(index=index, body={"query": {"match": query}})
    if res["hits"]["total"]["value"] == 0:
        raise HTTPException(status_code=404, detail="Record not found")
    return res["hits"]["hits"][0]["_source"]


@app.get("/person", response_model=List[Person])
def person_list():
    return get_list("person")


@app.get("/person/{person_id}", response_model=Person)
def person_by_id(person_id: str):
    return get_item("person", query={"id": person_id})


@app.get("/organization", response_model=List[Organization])
def organization_list():
    return get_list("organization")


@app.get("/organization/{organization_id}", response_model=Organization)
def organization_by_id(organization_id: str):
    return get_item("organization", query={"group_id": organization_id})
