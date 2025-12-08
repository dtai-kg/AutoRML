import morph_kgc
import configparser
import os


def rdf_generation(config_path, rml_path, kg_name):

    create_ini_file(config_path, rml_path, kg_name)
    rdf_graph = morph_kgc.materialize(config_path)
    rdf_graph.serialize(destination=os.path.join
                        (os.path.abspath
                         (os.path.dirname(config_path)), kg_name),
                        format="nt", encoding="utf-8")

    return


def create_ini_file(config_path, rml_path, kg_name):
    # Create a ConfigParser object
    config = configparser.ConfigParser()

    # Add a section and set a key-value pair
    config['CONFIGURATION'] = {'logging_level': 'INFO',
                               'output_file': os.path.join(
                                   os.path.abspath(
                                       os.path.dirname(config_path)), kg_name),
                               'output_format': 'N-TRIPLES'}
    config['DataSource1'] = {'mappings': rml_path}

    # Write the configuration to a .ini file
    with open(config_path, 'w') as configfile:
        config.write(configfile)
