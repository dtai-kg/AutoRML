import os 
import yaml
import pandas as pd


def get_mappings_metrics(yaml_file):

    with open(yaml_file, 'r') as file:
        data = yaml.safe_load(file)
        mappings = data.get('mappings', {})
        n_term_maps = len(mappings)
        n_po_maps = 0

        for tm in mappings:
            po = mappings[tm]["po"]
            n_po_maps += len(po)

        search_string = "example.com"
        mappings_str = str(mappings)

        if search_string in mappings_str: automated = False
        else: automated = True

        return n_term_maps, n_po_maps, automated
    

def get_mapping_collection_statistics(mappings_collections_path, mapping_collection, mapping_stats):

    collection_path = os.path.join(mappings_collections_path, mapping_collection)
    sta_systems = [folder for folder in os.listdir(collection_path) if os.path.isdir(os.path.join(collection_path, folder))]

    mapping_stats[mapping_collection] = {}

    for sta_system in sta_systems:
        n_term_maps_total = 0
        n_po_maps_total = 0
        n_automated = 0
        n_semi_automated = 0

        yml_files = [f for f in os.listdir(os.path.join(collection_path, sta_system)) if f.endswith('.yml')]

        for mappings in yml_files:
            #print(mappings)
            mappings_path = os.path.join(os.path.join(collection_path, sta_system), mappings)
            n_term_maps, n_po_maps, automated = get_mappings_metrics(mappings_path)  
            
            if automated == True: n_automated += 1
            elif automated == False: n_semi_automated += 1

            n_term_maps_total += n_term_maps
            n_po_maps_total += n_po_maps
        
        mapping_stats[mapping_collection]["Number of TMs w/ " + sta_system] = n_term_maps_total
        mapping_stats[mapping_collection]["Number of POMs w/ " + sta_system] = n_po_maps_total
        mapping_stats[mapping_collection]["Number of Automated Constructed Tables w/ " + sta_system] = n_automated
        mapping_stats[mapping_collection]["Number of Semi-Automated Constructed Tables w/ " + sta_system] = n_semi_automated

    return mapping_stats

def mappings_analysis(mappings_collections_path):

    mappings_collections = [folder for folder in os.listdir(mappings_collections_path) if os.path.isdir(os.path.join(mappings_collections_path, folder))]
    mapping_stats = {}

    for mapping_collection in mappings_collections:
        print(f"Calculating metrics for {mapping_collection}...")
        mapping_stats = get_mapping_collection_statistics(mappings_collections_path, mapping_collection, mapping_stats)

    mapping_stats_df = pd.DataFrame.from_dict(mapping_stats, orient='index')
    mapping_stats_df.index.name = 'Dataset Collection'

    return mapping_stats_df


if __name__ == "__main__":

    print("\nAnalyzing declarative mappings generated from all dataset collections...")

    mappings_collections_path = "evaluations/mappings"
    mapping_stats_df = mappings_analysis(mappings_collections_path)

    print("\nStatistics found: ")
    print(mapping_stats_df)

