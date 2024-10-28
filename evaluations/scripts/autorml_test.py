import sys
import os
import subprocess


def autorml(table_path, mappings_collection, rdf_collection, sta_system):

    src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'src'))
    sys.path.append(src_path)

    if src_path not in sys.path:
        sys.path.append(src_path)
    print(sys.path)

    table_name = table_path.split("/")[-1].split(".")[0]

    args = [
        "-i", table_path, 
        "--mappings_folder", "evaluations/mappings/" + mappings_collection,
        "-m", 
        "--rdf_folder", "evaluations/rdf/" + rdf_collection,
        "-oy", "mappings_" + table_name + ".yml",
        "-or", "mappings_" + table_name  + ".rml.ttl",
        "-okg", table_name + ".nt",
        "--sta_system", sta_system
    ]

    subprocess.run(["python", src_path] + args)

    return 



def test_autorml():

    #table_path = "/Users/ioannisdasoulas/Desktop/AutoRML/Data/Y3OHOKFF.csv"
    table_path = "/Users/ioannisdasoulas/Desktop/AutoRML/autoRML/evaluations/data_collections/test_collection_random/aircraft_models.csv"
    mappings_collection = "test_mappings"
    rdf_collection = "test_rdf"
    sta_system = "mtab"

    autorml(table_path, mappings_collection, rdf_collection, sta_system)

    return

test_autorml()