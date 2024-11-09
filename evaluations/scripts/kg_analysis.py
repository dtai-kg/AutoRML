import os 
from rdflib import Graph, Literal
from annotation_accuracy import assess_annotations_accuracy
from kg_construction import kg_construction_ground_truth
import pandas as pd
import datetime
from datetime import date

def normalize_triple(triple):
    """Normalize a triple by converting literals to just their values."""

    subject, predicate, obj = triple

    # If the object is a literal, strip the datatype
    if isinstance(obj, Literal):
        obj = obj.value  

    return [subject, predicate, str(obj)]


def assess_graph_accuracy(generated_graph, ground_truth_graph):

    generated_graph_triples = [normalize_triple(triple) for triple in generated_graph]
    ground_truth_graph_triples = [normalize_triple(triple) for triple in ground_truth_graph]

    for ground_truth_triple in ground_truth_graph_triples:
        if ground_truth_triple not in generated_graph_triples:
            print(ground_truth_triple)
            return False

    return True


def get_kg_statistics(kg_collections_path, kg_collection, kg_stats):

    collection_path = os.path.join(kg_collections_path, kg_collection)
    sta_systems = [folder for folder in os.listdir(collection_path) if os.path.isdir(os.path.join(collection_path, folder))]
    collections_with_ground_truth = ["WikidataTables2024R1", "HardTablesR1"]

    kg_stats[kg_collection] = {}

    for sta_system in sta_systems:
        print(f"Constructed KGs with {sta_system}:")
        n_triples = 0 
        n_correctly_annotated_tables = 0
        n_accurate_graphs = 0

        rdf_files = [f for f in os.listdir(os.path.join(collection_path, sta_system)) if f.endswith('.nt')]
        
        for rdf_file in rdf_files:
            print(rdf_file, sta_system)
            rdf_path = os.path.join(os.path.join(collection_path, sta_system), rdf_file)

            generated_graph = Graph()
            generated_graph.parse(rdf_path)

            n_triples += len(generated_graph)

            if kg_collection in collections_with_ground_truth:
                annotations_accuracy_check, cea_gt, cpa_gt, cta_gt = assess_annotations_accuracy(rdf_file.split('.')[0], kg_collection, sta_system)
                #print(annotations_accuracy_check)
                if annotations_accuracy_check == True: 
                    n_correctly_annotated_tables += 1
                    ground_truth_graph = kg_construction_ground_truth(rdf_file.split('.')[0], kg_collection, cea_gt, cpa_gt, cta_gt)
                    graph_accuracy_check = assess_graph_accuracy(generated_graph, ground_truth_graph)
                    if graph_accuracy_check == True: n_accurate_graphs += 1
                    else: 
                        print("Proglem with:", rdf_file)
                        return
                
            
        kg_stats[kg_collection]["Number of Triples w/ " + sta_system] = n_triples
        if kg_collection in collections_with_ground_truth:
            kg_stats[kg_collection]["Number of Correctly Annotated Tables w/ " + sta_system] = n_correctly_annotated_tables
            kg_stats[kg_collection]["Number of Accurate Graphs w/ " + sta_system] = n_accurate_graphs

    return kg_stats

def kg_analysis(kg_collections_path):

    kg_collections = [folder for folder in os.listdir(kg_collections_path) if os.path.isdir(os.path.join(kg_collections_path, folder))]
    kg_stats = {}

    for kg_collection in kg_collections:
        print(f"Calculating metrics for {kg_collection}...")
        kg_stats = get_kg_statistics(kg_collections_path, kg_collection, kg_stats)
        break

    kg_stats_df = pd.DataFrame.from_dict(kg_stats, orient='index')
    kg_stats_df.index.name = 'Dataset Collection'
    return kg_stats_df

if __name__ == "__main__":

    print("\nAnalyzing RDF knowledge graphs generated from all dataset collections...")

    kg_collections_path = "evaluations/rdf"
    kg_stats_df = kg_analysis(kg_collections_path)

    print("\nStatistics found: ")
    pd.set_option('display.max_columns', None)
    print(kg_stats_df)