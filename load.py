import pandas as pd
import py2neo

DATA_FILE = 'data.csv'

NATIONALITY = 'GB'


def load_data():
    df = pd.read_csv(DATA_FILE)

    for i, row in df.drop_duplicates('group_id').iterrows():
        print(row['group_id'])

    for i, row in df.drop_duplicates('id').iterrows():
        print(row['name'])


if __name__ == '__main__':
    load_data()
