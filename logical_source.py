import pandas as pd
import os

def define_source(mappings, table, cea):

    if cea == []:
        mappings["sources"] = {"table": "[{}~csv]".format(table)}
    else:
        generate_sem_table(table, cea)
        mappings["sources"] = {"table": "[{}~csv]".format(table),
                               "sem-table": "[{}~csv]".format(table.replace(".","-semantic."))}

    return mappings

def generate_sem_table(table, cea):

    df = pd.read_csv(table)
    for col_idx, row_idx, value in cea:
        df.iat[int(row_idx), int(col_idx)] = value

    table_folder = os.path.dirname(table)
    print(table_folder)
    df.to_csv(table_folder + '{}-semantic.csv'.format(table.split(".")[0]), index=False)