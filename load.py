import numpy as np
import pandas as pd
from py2neo import Graph, Node, NodeMatcher, Relationship

from elasticsearch import Elasticsearch

DATA_FILE = "data.csv"

NATIONALITY = "GB"


def load_data(es: Elasticsearch):
    df = pd.read_csv(DATA_FILE)
    df.replace({np.nan: None}, inplace=True)

    g = Graph("bolt://neo4j:7687")

    # Delete existing data if present

    g.delete_all()
    es.indices.delete(index="*", ignore=[400, 404])

    matcher = NodeMatcher(g)

    # Creating organizations first

    tx = g.begin()

    n_orgs = 0

    for i, row in df[["group", "group_id"]].drop_duplicates("group_id").iterrows():
        doc = {"name": row["group"], "group_id": row["group_id"]}
        group = Node("Organization", **doc)

        es.index("organization", doc)

        tx.create(group)

        n_orgs += 1

    tx.commit()

    es.indices.refresh("organization")

    print(f"Added {n_orgs} organizations")

    # Creating people and membership records

    tx = g.begin()

    n_people = 0

    for i, row in (
        df[["id", "name", "sort_name", "email", "group_id", "group"]]
        .drop_duplicates("id")
        .iterrows()
    ):
        es.index("person", row.to_dict())

        person = Node(
            "Person",
            **row.drop(["group_id", "group"]).to_dict(),
            nationality=NATIONALITY,
        )

        group = matcher.match("Organization", group_id=row["group_id"]).first()

        rel = Relationship(person, "Membership", group)
        tx.create(rel)

        n_people += 1

    tx.commit()

    es.indices.refresh("person")

    print(f"Added {n_people} people records")

    return n_orgs, n_people
