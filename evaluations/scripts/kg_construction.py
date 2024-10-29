import os
from autorml_eval_mode import autorml_eval_mode

def kg_construction(dataset_collections_path, dataset_collection, available_sta_systems):

    collection_path = os.path.join(dataset_collections_path, dataset_collection)
    csv_files = [f for f in os.listdir(collection_path) if f.endswith('.csv')]

    mappings_collection, rdf_collection, annotation_collection = dataset_collection, dataset_collection, dataset_collection

    for table in csv_files:
        table_path = os.path.join(collection_path, table)

        for sta_system in available_sta_systems:

            if os.path.exists("evaluations/rdf/" + rdf_collection + "/" + sta_system + "/" + table.replace(".csv", ".nt")):
                print(f"Table {table} already annotated. Skipping...")
                continue
            autorml_eval_mode(table_path=table_path, 
                              mappings_collection=mappings_collection, 
                              rdf_collection=rdf_collection, 
                              annotation_collection=annotation_collection, 
                              sta_system=sta_system)

    return

if __name__ == "__main__":

    print("\nConstructing RDF knowledge graphs from all dataset collections...")

    dataset_collections_path = "evaluations/data_collections"
    available_sta_systems = ["mtab", "torchictab"]

    dataset_collections = [folder for folder in os.listdir(dataset_collections_path) if os.path.isdir(os.path.join(dataset_collections_path, folder))]
    for dataset_collection in dataset_collections:
        print(f"\nConstructing RDF knowledge graphs from {dataset_collection}...")
        kg_construction(dataset_collections_path, dataset_collection, available_sta_systems)
        

    