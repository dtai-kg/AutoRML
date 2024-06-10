from annotate import annotate_torchic_tab
from mapping_synthesis import mapping_synthesis

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
                      os.path.join(args.mappings_folder, args.rml_output),
                      subject_column, primary_annotations, secondary_annotations, 
                      cea, cpa, cta, cqa)
