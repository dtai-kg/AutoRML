import pandas as pd
import os
from urllib.parse import urlparse

def define_source(mappings, table, cea, primary_annotations):

    df = pd.read_csv(table)
    col_names = df.columns.to_list()

    if cea == []:
        mappings["sources"] = {}

        mappings["sources"]["table"] = {}
        mappings["sources"]["table"]["access"] = os.path.abspath(table)
        mappings["sources"]["table"]["referenceFormulation"] = "csv"
        mappings["sources"]["table"]["iterator"] = "$"
    
    else:
        df = generate_sem_table(table, df, cea, primary_annotations)

        mappings["sources"] = {}

        mappings["sources"]["table"] = {}
        mappings["sources"]["table"]["access"] = os.path.abspath(table)
        mappings["sources"]["table"]["referenceFormulation"] = "csv"
        mappings["sources"]["table"]["iterator"] = "$"

        mappings["sources"]["sem-table"] = {}
        mappings["sources"]["sem-table"]["access"] = os.path.abspath(table.replace(".csv","-semantic.csv"))
        mappings["sources"]["sem-table"]["referenceFormulation"] = "csv"
        mappings["sources"]["sem-table"]["iterator"] = "$"

    return mappings, col_names

def generate_sem_table(table, df, cea, primary_annotations):

    ne_cols = []
    for i in range(len(primary_annotations)):
        if primary_annotations[i] == "NE":
            ne_cols.append(i)

    for col_idx, row_idx, value in cea:
        df.iat[int(row_idx), int(col_idx)] = value

    # Replace invalid URLs with None
    for idx in ne_cols:
        column = df.columns[idx]
        df[column] = df[column].apply(lambda x: x if is_valid_url(x) else None)

    df.to_csv(os.path.abspath(table.replace(".csv","-semantic.csv")), index=False)

    return 

# Function to validate a URL
def is_valid_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False
    
def delete_semantic_table(semantic_table_path):

    semantic_table_path = semantic_table_path
    if os.path.exists(semantic_table_path):
        os.remove(semantic_table_path)

    return