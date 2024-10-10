import pandas as pd
import os
from ruamel.yaml.scalarstring import PreservedScalarString

def define_source(mappings, table, cea):

    df = pd.read_csv(table)
    col_names = df.columns.to_list()

    if cea == []:
        mappings["sources"] = {}

        mappings["sources"]["table"] = {}
        mappings["sources"]["table"]["access"] = os.path.abspath(table)
        mappings["sources"]["table"]["referenceFormulation"] = "csv"
        mappings["sources"]["table"]["iterator"] = "$"
    
    else:
        df = generate_sem_table(table, df, cea)

        mappings["sources"] = {}

        mappings["sources"]["table"] = {}
        mappings["sources"]["table"]["access"] = os.path.abspath(table)
        mappings["sources"]["table"]["referenceFormulation"] = "csv"
        mappings["sources"]["table"]["iterator"] = "$"

        mappings["sources"]["sem-table"] = {}
        mappings["sources"]["sem-table"]["access"] = os.path.abspath(table.replace(".","-semantic."))
        mappings["sources"]["sem-table"]["referenceFormulation"] = "csv"
        mappings["sources"]["sem-table"]["iterator"] = "$"

    return mappings, col_names

def generate_sem_table(table, df, cea):

    for col_idx, row_idx, value in cea:
        df.iat[int(row_idx), int(col_idx)] = value

    table_folder = os.path.dirname(table)
    df.to_csv(table_folder + '{}-semantic.csv'.format(table.split(".")[0].split("/")[-1]), index=False)

    return 