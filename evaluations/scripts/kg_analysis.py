import os 
from rdflib import Graph

def count_triples(rdf_path):

    g = Graph()
    g.parse(rdf_path)

    return len(g)

def get_kg_statistics(kg_collections_path, kg_collection, kg_stats):

    collection_path = os.path.join(kg_collections_path, kg_collection)
    sta_systems = [folder for folder in os.listdir(collection_path) if os.path.isdir(os.path.join(collection_path, folder))]

    kg_stats[kg_collection] = {}

    for sta_system in sta_systems:
        n_triples = 0 

        rdf_files = [f for f in os.listdir(os.path.join(collection_path, sta_system)) if f.endswith('.nt')]
        
        for rdf_file in rdf_files:
            #print(rdf_file)
            rdf_path = os.path.join(os.path.join(collection_path, sta_system), rdf_file)
            n_triples += count_triples(rdf_path)


        kg_stats[kg_collection]["Number of Triples w/ " + sta_system] = n_triples

    print(kg_stats)

    return

def kg_analysis(kg_collections_path):

    kg_collections = [folder for folder in os.listdir(kg_collections_path) if os.path.isdir(os.path.join(kg_collections_path, folder))]
    kg_stats = {}

    for kg_collection in kg_collections:
        print(f"Calculating metrics for {kg_collection}...")
        get_kg_statistics(kg_collections_path, kg_collection, kg_stats)
        break



if __name__ == "__main__":

    print("\nAnalyzing RDF knowledge graphs generated from all dataset collections...")

    kg_collections_path = "evaluations/rdf"
    kg_analysis(kg_collections_path)