import os
import pandas as pd

def get_collection_statistics(dataset_collections_path, dataset_collection, collection_stats):

    collection_path = os.path.join(dataset_collections_path, dataset_collection)
    csv_files = [f for f in os.listdir(collection_path) if f.endswith('.csv')]
    n_tables = len(csv_files)

    total_rows = 0.0
    total_columns = 0.0

    for table in csv_files:
        table_path = os.path.join(collection_path, table)
        print(table)

        df = pd.read_csv(table_path, skipinitialspace=True)
        total_rows += len(df)
        total_columns += len(df.columns)
        
    avg_rows = total_rows / n_tables if n_tables > 0 else 0
    avg_columns = total_columns / n_tables if n_tables > 0 else 0

    collection_stats[dataset_collection] = {
        'Number of tables': n_tables,
        'Avg number of rows': avg_rows,
        'Avg number of columns': avg_columns
    }

    return collection_stats

def dataset_collection_analysis(dataset_collections_path):
    
    dataset_collections = [folder for folder in os.listdir(dataset_collections_path) if os.path.isdir(os.path.join(dataset_collections_path, folder))]
    collection_stats = {}
    
    for dataset_collection in dataset_collections:
        print(f"Calculating metrics for {dataset_collection}...")
        collection_stats = get_collection_statistics(dataset_collections_path, dataset_collection, collection_stats)

    collection_stats_df = pd.DataFrame.from_dict(collection_stats, orient='index')
    collection_stats_df.index.name = 'Dataset Collection'

    return collection_stats_df

if __name__ == "__main__":

    print("\nCalculating metrics for each dataset collection...")
    dataset_collections_path = "evaluations/data_collections"
    collection_stats_df = dataset_collection_analysis(dataset_collections_path)

    print("\nStatistics found: ")
    print(collection_stats_df)