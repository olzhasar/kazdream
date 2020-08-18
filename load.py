import pandas as pd
from py2neo import Graph, Node, NodeMatcher, Relationship

DATA_FILE = "data.csv"

NATIONALITY = "GB"


def load_data():
    df = pd.read_csv(DATA_FILE)

    g = Graph()
    matcher = NodeMatcher(g)

    # Creating organizations first

    tx = g.begin()

    n = 0

    for i, row in df.drop_duplicates("group_id").iterrows():
        group = Node("Organization", group_id=row["group_id"], name=row["group"])
        tx.create(group)
        n += 1

    tx.commit()

    print(f"Added {n+1} organizations")

    # Creating people and membership records

    tx = g.begin()

    n = 0

    for i, row in df.drop_duplicates("id").iterrows():
        person = Node(
            "Person",
            id=row["id"],
            name=row["name"],
            alias=row["sort_name"],
            email=row["email"],
            nationality="GB",
        )
        group = matcher.match("Organization", group_id=row["group_id"]).first()

        rel = Relationship(person, "Membership", group)
        tx.create(rel)

        n += 1

    tx.commit()

    print(f"Added {n+1} people records")


if __name__ == "__main__":
    load_data()
