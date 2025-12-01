from autorml.logical_source import define_source
from autorml.term_maps import define_term_maps

from ruamel.yaml import YAML
import yatter


def mapping_synthesis(table, yarrrml_output_location,
                      subject_column, primary_annotations,
                      secondary_annotations, cea, cpa, cta, cqa):

    # Initialize YAML file
    yaml = YAML(pure=True)
    yaml.default_flow_style = False
    yaml.indent(mapping=2, sequence=4, offset=2)

    mappings = {"authors": "AutoRML"}
    mappings, col_names = define_source(mappings, table, cea,
                                        primary_annotations)
    mappings = define_term_maps(mappings,
                                subject_column, primary_annotations,
                                secondary_annotations,
                                cea, cpa, cta,
                                col_names)
    # mappings = define_subject_maps(mappings, subject_column, cea)

    # Create the YARRRML mapping file with the dictionary assembled
    with open(yarrrml_output_location, 'w', encoding="utf-8") as file:
        for section in mappings:
            yaml.dump({section: mappings[section]}, file, )
            file.write('\n')

    print("YARRRML mappings succesfully created!")

    return


def rml_generation(yarrrml_output_location, rml_output_location):

    yaml = YAML(typ='safe', pure=True)
    rml_content = yatter.translate(yaml.load(open(yarrrml_output_location)))

    output_file = open(rml_output_location, "w")
    output_file.write(rml_content)
    output_file.close()
    print("RML mappings succesfully created!")

    return
