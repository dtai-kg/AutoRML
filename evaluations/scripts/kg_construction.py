import os
from autorml_eval_mode import autorml_eval_mode
import pandas as pd
from rdflib import Graph, Literal, RDF, URIRef
from rdflib.namespace import XSD
from datetime import datetime

def kg_construction_ground_truth(file_name, data_collection, cea_gt, cpa_gt, cta_gt):

    dataset_collections_path = "evaluations/data_collections"
    table_path = os.path.join(dataset_collections_path, data_collection, file_name + ".csv")

    df = pd.read_csv(table_path)
    cea_gt_df = pd.DataFrame(cea_gt, columns = ["Row", "Column", "Label"])
    cpa_gt_df = pd.DataFrame(cpa_gt, columns = ["Subject_Column", "Object_Column", "Label"])
    cta_gt_df = pd.DataFrame(cta_gt, columns = ["Column", "Label"])

    # print(df)
    # print(cea_gt_df)
    # print(cpa_gt_df)
    # print(cta_gt_df)

    ground_truth_graph = Graph()

    ne_columns = list(set(cea_gt_df["Column"].tolist()))

    so_column_pairs = {}
    for cpa_annotation in cpa_gt:
        subject_column_idx = cpa_annotation[0]
        object_column_idx = cpa_annotation[1]

        if subject_column_idx not in so_column_pairs:
            so_column_pairs[subject_column_idx] = [object_column_idx]
        else:
            so_column_pairs[subject_column_idx].append(object_column_idx)

    for cea_annotation in cea_gt:
        row_idx = cea_annotation[0]
        subject_column_idx = cea_annotation[1]
        cea_label_subject = cea_annotation[2]

        cea_label_subject_URI = URIRef(cea_label_subject)
        
        #Semantic type graph construction
        if subject_column_idx in cta_gt_df["Column"].tolist():
            cta_label_URI = URIRef(cta_gt_df.loc[cta_gt_df['Column'] == subject_column_idx, 'Label'].iloc[0])
            ground_truth_graph.add((cea_label_subject_URI, RDF.type, cta_label_URI))

        # #Graph construction using the rest of known properties 
        if subject_column_idx in so_column_pairs:
            for object_column_idx in so_column_pairs[subject_column_idx]:
                
                #Define property
                cpa_label = cpa_gt_df.loc[ (cpa_gt_df['Subject_Column'] == subject_column_idx) & (cpa_gt_df['Object_Column'] == object_column_idx), 'Label'].iloc[0]
                cpa_label_URI = URIRef(cpa_label)

                #Construction for NE object column
                if object_column_idx in ne_columns:
                    try: 
                        cea_label_object = cea_gt_df.loc[ (cea_gt_df['Row'] == row_idx) & (cea_gt_df['Column'] == object_column_idx), 'Label'].iloc[0]
                    except:
                        continue
                    cea_label_object_URI = URIRef(cea_label_object)
                    ground_truth_graph.add((cea_label_subject_URI, cpa_label_URI, cea_label_object_URI))

                #Construction for L object column
                else:
                    object_value = df.iloc[:, object_column_idx].tolist()[row_idx - 1]
                    if pd.isna(object_value): continue
                    ground_truth_graph.add((cea_label_subject_URI, cpa_label_URI, Literal(object_value, datatype=None)))

    return ground_truth_graph

def kg_construction_autorml(dataset_collections_path, failed_annotations_path, dataset_collection, available_sta_systems):

    collection_path = os.path.join(dataset_collections_path, dataset_collection)
    csv_files = [f for f in os.listdir(collection_path) if f.endswith('.csv')]

    mappings_collection, rdf_collection, annotation_collection = dataset_collection, dataset_collection, dataset_collection

    for table in csv_files:
        table_path = os.path.join(collection_path, table)

        for sta_system in available_sta_systems:
            if os.path.exists(os.path.join("evaluations/rdf/", rdf_collection, sta_system, table.replace(".csv", ".nt"))):
                print(f"Table {table} already annotated. Skipping...")
                continue
            elif os.path.exists(os.path.join(failed_annotations_path, dataset_collection, sta_system, table)):
                print(f"Table could not be annotated with {sta_system}. Skipping...")
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
    failed_annotations_path = "evaluations/failed_annotations"
    available_sta_systems = ["torchictab"]

    dataset_collections = [folder for folder in os.listdir(dataset_collections_path) if os.path.isdir(os.path.join(dataset_collections_path, folder))]
    for dataset_collection in dataset_collections:
        if "Kaggle" not in dataset_collection: continue
        print(f"\nConstructing RDF knowledge graphs from {dataset_collection}...")
        kg_construction_autorml(dataset_collections_path, failed_annotations_path, dataset_collection, available_sta_systems)
        

    