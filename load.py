import numpy as np
import pandas as pd
from py2neo import Graph, Node, NodeMatcher, Relationship

from elasticsearch import Elasticsearch

DATA_FILE = "data.csv"

NATIONALITY = "GB"


def load_data():
    df = pd.read_csv(DATA_FILE)
    df.replace({np.nan: None}, inplace=True)

    g = Graph()
    matcher = NodeMatcher(g)

    es = Elasticsearch()

    # Creating organizations first

    tx = g.begin()

    n = 0

    for i, row in df.drop_duplicates("group_id").iterrows():
        doc = row[["group_id", "group"]].to_dict()
        group = Node("Organization", **doc)

        es.index("organization", doc)

        tx.create(group)

        n += 1

    tx.commit()

    print(f"Added {n+1} organizations")

    # Creating people and membership records

    tx = g.begin()

    n = 0

    for i, row in df.drop_duplicates("id").iterrows():
        doc = row[["id", "name", "sort_name", "email"]].to_dict()

        person = Node("Person", **doc, nationality=NATIONALITY)

        try:
            es.index("person", doc)
        except:
            print(doc)
            print(person)

        group = matcher.match("Organization", group_id=row["group_id"]).first()

        rel = Relationship(person, "Membership", group)
        tx.create(rel)

        n += 1

    tx.commit()

    print(f"Added {n+1} people records")


if __name__ == "__main__":
    load_data()
