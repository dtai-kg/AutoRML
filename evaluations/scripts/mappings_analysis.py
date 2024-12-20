import os 
import yaml
import pandas as pd
from dataset_collection_analysis import dataset_collection_analysis
from utils import save_pkl


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
    

def get_mapping_collection_statistics(mappings_collections_path, mapping_collection, construction_stats, automation_stats, total_tables_dict):

    collection_path = os.path.join(mappings_collections_path, mapping_collection)
    sta_systems = [folder for folder in os.listdir(collection_path) if os.path.isdir(os.path.join(collection_path, folder))]

    construction_stats[mapping_collection] = {}
    automation_stats[mapping_collection] = {}

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
        
        construction_stats[mapping_collection]["Number of Constructed KGs w/ " + sta_system] = n_semi_automated + n_automated
        construction_stats[mapping_collection]["Number of TMs w/ " + sta_system] = n_term_maps_total
        construction_stats[mapping_collection]["Number of POMs w/ " + sta_system] = n_po_maps_total

        automation_stats[mapping_collection]["Number of Automated Constructed KGs w/ " + sta_system] = n_automated
        automation_stats[mapping_collection]["Number of Semi-Automated Constructed KGs w/ " + sta_system] = n_semi_automated
        automation_stats[mapping_collection]["Number of Failed Constructions w/ " + sta_system] = total_tables_dict[mapping_collection] - n_automated - n_semi_automated

    return construction_stats, automation_stats

def mappings_analysis(mappings_collections_path):

    mappings_collections = [folder for folder in os.listdir(mappings_collections_path) if os.path.isdir(os.path.join(mappings_collections_path, folder))]
    construction_stats = {}
    automation_stats = {}

    dataset_stats_df = dataset_collection_analysis(dataset_collections_path)
    total_tables_dict = dataset_stats_df["Number of tables"].to_dict()

    for mapping_collection in mappings_collections:
        print(f"Calculating mappings metrics for {mapping_collection}...")
        construction_stats, automation_stats = get_mapping_collection_statistics(mappings_collections_path, mapping_collection, construction_stats, automation_stats, total_tables_dict)

    construction_stats_df = pd.DataFrame.from_dict(construction_stats, orient='index')
    construction_stats_df.index.name = 'Dataset Collection'

    #Get avg TMs and POMs
    construction_stats_df["Number of TMs w/ mtab"] = construction_stats_df["Number of TMs w/ mtab"] / construction_stats_df["Number of Constructed KGs w/ mtab"]
    construction_stats_df["Number of POMs w/ mtab"] = construction_stats_df["Number of POMs w/ mtab"] / construction_stats_df["Number of Constructed KGs w/ mtab"]
    construction_stats_df["Number of TMs w/ torchictab"] = construction_stats_df["Number of TMs w/ torchictab"] / construction_stats_df["Number of Constructed KGs w/ torchictab"]
    construction_stats_df["Number of POMs w/ torchictab"] = construction_stats_df["Number of POMs w/ torchictab"] / construction_stats_df["Number of Constructed KGs w/ torchictab"]

    automation_stats_df = pd.DataFrame.from_dict(automation_stats, orient='index')
    automation_stats_df.index.name = 'Dataset Collection'

    return construction_stats_df, automation_stats_df


if __name__ == "__main__":

    print("\nAnalyzing declarative mappings generated from all dataset collections...")

    mappings_collections_path = "evaluations/mappings"
    dataset_collections_path = "evaluations/data_collections"
    automation_stats_path = "evaluations/stats/automations_stats.pkl"
    construction_stats_df, automation_stats_df = mappings_analysis(mappings_collections_path)
    save_pkl(automation_stats_path, automation_stats_df)

    pd.set_option('display.max_columns', None)
    print(construction_stats_df)
    # print(automation_stats_df)

