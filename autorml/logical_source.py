import pandas as pd
import os
from urllib.parse import urlparse


def define_source(mappings, table, cea, primary_annotations):

    df = load_table(table)
    # avoid yatter 'type' error translation
    df.columns = df.columns.str.replace('type', 'typ', regex=True)
    df.columns = df.columns.str.replace('Type', 'typ', regex=True)
    # avoid yatter '()' error translation
    df.columns = df.columns.str.replace(r'\(.*?\)', '', regex=True)
    col_names = df.columns.to_list()

    if cea == []:
        mappings["sources"] = {}

        mappings["sources"]["table"] = {}
        mappings["sources"]["table"]["access"] = table.replace("\\", "\\\\")
        mappings["sources"]["table"]["referenceFormulation"] = "csv"
        mappings["sources"]["table"]["iterator"] = "$"

    else:
        df = generate_sem_table(table, df, cea, primary_annotations)

        mappings["sources"] = {}

        mappings["sources"]["table"] = {}
        mappings["sources"]["table"]["access"] = table.replace("\\", "\\\\")
        mappings["sources"]["table"]["referenceFormulation"] = "csv"
        mappings["sources"]["table"]["iterator"] = "$"

        mappings["sources"]["sem-table"] = {}
        mappings["sources"]["sem-table"]["access"] =\
            table.replace(".csv", "-semantic.csv").replace("\\", "\\\\")
        mappings["sources"]["sem-table"]["referenceFormulation"] = "csv"
        mappings["sources"]["sem-table"]["iterator"] = "$"

    return mappings, col_names


def generate_sem_table(table, df, cea, primary_annotations):

    ne_cols = []
    for i in range(len(primary_annotations)):
        if primary_annotations[i] == "NE":
            ne_cols.append(i)

    for row_idx, col_idx, value in cea:
        df.iat[int(row_idx)-1, int(col_idx)] = value

    # Replace invalid URLs with None
    for idx in ne_cols:
        column = df.columns[idx]
        df[column] =\
            df[column].apply(lambda x: x if pd.isna(x) or is_valid_url(x)
                             else None)

    df.to_csv(os.path.abspath(table.replace(".csv", "-semantic.csv")),
              index=False)

    return


def load_table(file_path):

    """Load CSV input file"""

    # Read the first line
    with open(file_path, 'r', encoding='utf-8') as file:
        first_line = file.readline().strip()

    # Check if the first line is entirely integers
    if all(item.isdigit() for item in first_line.split(',')):
        # Skip the first line if it contains only integers
        df = pd.read_csv(file_path, encoding='utf-8', skiprows=1,
                         quotechar='"', skipinitialspace=True)
    else:
        # Read the file normally
        df = pd.read_csv(file_path, encoding='utf-8', quotechar='"',
                         skipinitialspace=True)

    return df


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
