from annotation.torchic_tab import torchic_tab
from annotation.mtab import mtab
from mapping_synthesis import mapping_synthesis, rml_generation
from materialize import rdf_generation
from logical_source import delete_semantic_table
import sys

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
    
    parser.add_argument("-okg", "--kg_output",
                    default="kg.nt",
                    type=str,
                    help="Output RDF file")
    
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
    
    parser.add_argument("--sta_system",
                    default="mtab",
                    type=str,
                    help="Used semantic table annotation system")

    return parser

def main():

    print("AutoRML initialized!\n")
    args = define_args().parse_args()
    
    # Extract annotations from Semantic Annotation System
    # TorchicTab system is used, other annotation systems can be imported as well
    if args.sta_system == "mtab":
        print("Annotating table using MTab:", args.input_table, "...")
        (subject_column, primary_annotations, secondary_annotations, cea, cpa, cta, cqa) = mtab(args.input_table)
    elif args.sta_system == "torchictab":
        print("Annotating table using TorchicTab:", args.input_table, "...")
        (subject_column, primary_annotations, secondary_annotations, cea, cpa, cta, cqa) = torchic_tab(args.input_table)
    else:
        sys.exit("Selected annotation system not supported. Exiting...")
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
    print("\nYARRRML and RML mappings succesfully generated!")
    
    if(args.materialize):

        if not os.path.exists(args.rdf_folder):
            os.makedirs(args.rdf_folder)
            print(f"Folder '{args.rdf_folder}' created.")

        rdf_generation(os.path.join(args.rdf_folder, 'config.ini'), os.path.abspath(str(os.path.join(args.mappings_folder, args.rml_output))), args.kg_output)
        print("\nRDF graph succesfully generated!")

    # Delete semantic table created for including semantic cell labels
    delete_semantic_table(os.path.abspath(args.input_table.replace(".csv","-semantic.csv")))

    return

if __name__ == "__main__":

    main()

    

