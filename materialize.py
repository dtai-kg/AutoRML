import morph_kgc
import configparser
import os

def rdf_generation(config_path, rml_path):

    create_ini_file(config_path, rml_path)
    rdf_graph = morph_kgc.materialize(config_path)
    rdf_graph.serialize(destination=os.path.abspath(os.path.dirname(config_path) + '/kg.ttl'))

    return


def create_ini_file(config_path, rml_path):
    # Create a ConfigParser object
    config = configparser.ConfigParser()

    # Add a section and set a key-value pair
    config['CONFIGURATION'] = {'logging_level': 'INFO',
                               'output_file': os.path.abspath(os.path.dirname(config_path) + '/kg.ttl'),
                               'output_format': 'N-TRIPLES'}
    config['DataSource1'] = {'mappings': rml_path}

    # Write the configuration to a .ini file
    with open(config_path, 'w') as configfile:
        config.write(configfile)