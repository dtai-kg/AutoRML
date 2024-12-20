# AutoRML

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0) 

**AutoRML** is a system that automatically generates declarative mappings ([YARRRML](https://rml.io/yarrrml/) and [RML](https://rml.io)) and constructs RDF knowledge graphs for tabular data. It does so by utilizing third-party semantic table annotation systems, mapping produced semantic annotations to declarative mapping rules. 

AutoRML can be used with different semantic table annotation systems. It has been tested with [MTab](https://mtab.kgraph.jp) and [TorchicTab](https://ceur-ws.org/Vol-3557/paper2.pdf) (closed-source). 

## Installation 

    pip install requirements.txt 

Python versions 3.9, 3.10, and 3.11 are tested and recommended.

## Usage

TODO

## Example usage 

You can find some tables to test AutoRML in the examples folder. To run AutoRML for one of the examples:

    cd autoRML
    python3 src -i "examples/tables/cities.csv" -m --mappings_folder "examples/mappings" --save_annotations --annotations_folder "examples/annotations" --rdf_folder "examples/rdf" -ds

The open-source version of AutoRML currently only supports MTab as a semantic table annotation system. MTab may often fail to provide annotations for large tables, due to failed API reqests. In that case try hosting your own semantic table annotation system or contact AutoRML authors to test your tables. 

## Evaluations

TODO

## Contact

TODO