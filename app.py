import time
from typing import List, Optional

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse

from elasticsearch import Elasticsearch
from elasticsearch.exceptions import ConnectionError
from load import load_data
from models import Organization, Person

app = FastAPI(docs_url="/")

es = Elasticsearch(["elastic:9200"])


@app.exception_handler(ConnectionError)
async def elastic_error_handler(request: Request, exc: ConnectionError):
    return JSONResponse(
        status_code=412,
        content={
            "message": "Elasticsearch cluster is not up yet. Try again in a few seconds"
        },
    )


@app.get("/load")
def import_data():
    """Import data from the csv file"""

    n_orgs, n_people = load_data(es)
    return {"Success": True, "Organizations added": n_orgs, "People added": n_people}


def get_list(index, q):
    if q:
        query_body = {"query": {"query_string": {"query": q}}}
    else:
        query_body = None
    res = es.search(
        body=query_body, index=index, filter_path=["hits.hits._source"], size=10000
    )
    records = [r["_source"] for r in res["hits"]["hits"]]
    return records


def get_item(index, query={}):
    res = es.search(index=index, body={"query": {"match": query}}, size=1)
    if res["hits"]["total"]["value"] == 0:
        raise HTTPException(status_code=404, detail="Record not found")
    return res["hits"]["hits"][0]["_source"]


@app.get("/person", response_model=List[Person])
def person_list(q: Optional[str] = None):
    return get_list("person", q)


@app.get("/person/{person_id}", response_model=Person)
def person_by_id(person_id: str):
    return get_item("person", query={"id": person_id})


@app.get("/organization", response_model=List[Organization])
def organization_list(q: Optional[str] = None):
    return get_list("organization", q)


@app.get("/organization/{organization_id}", response_model=Organization)
def organization_by_id(organization_id: str):
    return get_item("organization", query={"group_id": organization_id})
