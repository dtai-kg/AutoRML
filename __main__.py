from annotate import annotate_torchic_tab
from mapping_synthesis import mapping_synthesis, rml_generation
from materialize import rdf_generation

import argparse
import os

def define_args():

    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input_table",
                    required=True,
                    type=str,
                    help="Input table in CSV format")
    
    parser.add_argument("-oy", "--yarrml_output",
                    default="mappings.yml",
                    type=str,
                    help="Output YARRRML mappings")
    
    parser.add_argument("-or", "--rml_output",
                    default="mappings.rml.ttl",
                    type=str,
                    help="Output RML mappings")
    
    parser.add_argument("--mappings_folder",
                    default="mappings",
                    type=str,
                    help="Output mappings folder")
    
    parser.add_argument("-m", "--materialize",
                    action='store_true',
                    help="Generate RDF")
    
    parser.add_argument("--rdf_folder",
                    default="rdf",
                    type=str,
                    help="Output RDF folder")

    return parser

if __name__ == "__main__":

    print("AutoRML initialized!\n")
    args = define_args().parse_args()
    
    # Extract annotations from Semantic Annotation System
    # TorchicTab system is used, other annotation systems can be imported as well
    print("Annotating table using TorchicTab:", args.input_table, "...")
    (subject_column, primary_annotations, secondary_annotations, 
    cea, cpa, cta, cqa) = annotate_torchic_tab(args.input_table)
    print("Tabular annotation completed!\n")

    if not os.path.exists(args.mappings_folder):
        os.makedirs(args.mappings_folder)
        print(f"Folder '{args.mappings_folder}' created.")

    mapping_synthesis(args.input_table, 
                            os.path.join(args.mappings_folder, args.yarrml_output), 
                            subject_column, primary_annotations, secondary_annotations, 
                            cea, cpa, cta, cqa)
    
    rml_generation(os.path.join(args.mappings_folder, args.yarrml_output), 
                   os.path.join(args.mappings_folder, args.rml_output))
    
    if(args.materialize):

        if not os.path.exists(args.rdf_folder):
            os.makedirs(args.rdf_folder)
            print(f"Folder '{args.rdf_folder}' created.")

        rdf_generation(os.path.join(args.rdf_folder, 'config.ini'), os.path.abspath(str(os.path.join(args.mappings_folder, args.rml_output))))
    

