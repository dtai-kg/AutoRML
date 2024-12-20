import sys
import os
import subprocess


def autorml_eval_mode(table_path, mappings_collection, rdf_collection, annotation_collection, sta_system):

    src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'src'))
    sys.path.append(src_path)

    if src_path not in sys.path:
        sys.path.append(src_path)

    table_name = table_path.split("/")[-1].split(".")[0]

    args = [
        "-i", table_path, 
        "--mappings_folder", "evaluations/mappings/" + mappings_collection + "/" + sta_system,
        "-m", 
        "--rdf_folder", "evaluations/rdf/" + rdf_collection + "/" + sta_system,
        "-oy", table_name + ".yml",
        "-or", table_name  + ".rml.ttl",
        "-okg", table_name + ".nt",
        "--sta_system", sta_system, 
        "--save_annotations", 
        "--annotations_folder", "evaluations/annotations/" + annotation_collection + "/" + sta_system,
        "-oa", table_name + ".json",
        "-ds"
    ]

    subprocess.run(["python", src_path] + args)

    return 

def test_autorml_eval_mode():

    #table_path = "/Users/ioannisdasoulas/Desktop/AutoRML/Data/Y3OHOKFF.csv"
    #table_path = "/Users/ioannisdasoulas/Desktop/AutoRML/autoRML/evaluations/data_collections/Kaggle_Diverse_CSV_DS/addresses.csv"
    table_path = "/Users/ioannisdasoulas/Desktop/AutoRML/autoRML/evaluations/data_collections/GTFS-Madrid/FREQUENCIES.csv"
    mappings_collection = "test_mappings"
    rdf_collection = "test_rdf"
    annotation_collection = "test_annotations"
    sta_system = "torchictab"

    autorml_eval_mode(table_path, mappings_collection, rdf_collection, annotation_collection, sta_system)

    return

# test_autorml_eval_mode()