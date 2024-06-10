from logical_source import define_source
from terms_maps import define_term_maps

from ruamel.yaml import YAML

def mapping_synthesis(table, yarrrml_output_location, rml_output_location,
                      subject_column, primary_annotations, secondary_annotations, 
                      cea, cpa, cta, cqa):
    
    #Initialize YAML file
    yaml=YAML(typ='safe', pure=True)
    yaml.default_flow_style = False
    yaml.indent(mapping=2, sequence=4, offset=2)

    mappings = {"authors": "AutoRML"}
    mappings = define_source(mappings, table, cea)
    mappings = define_term_maps(mappings, subject_column, primary_annotations, cea)
    # mappings = define_subject_maps(mappings, subject_column, cea)

    #Create the YARRRML mapping file with the dictionary assembled
    with open(yarrrml_output_location, 'w') as file:
        for section in mappings:
            yaml.dump({section: mappings[section]}, file)
            file.write('\n')
    

    return