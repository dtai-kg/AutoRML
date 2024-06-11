from torchic_tab_heuristic.task_calculation_wd import generate_annotations

#Call of TorchicTab to extract tabular annotations for a given table
def annotate_torchic_tab(file):

    # (subject_column, primary_annotations, secondary_annotations, 
    # cea_annotations, cpa_annotations, cta_annotations) = generate_annotations(file)

    # Test Annotations
    (subject_column, primary_annotations, secondary_annotations, 
    cea, cpa, cta, cqa) = (-1, #subject_column_index
                           ['NE', 'NE', 'NE'], #named_entity_columns_index
                           ['NE', 'CARDINAL', 'NE'], #datatype_index (for literal columns)
                           [['0', '0', 'http://www.wikidata.org/entity/Q15865202'], 
                            ['0', '1', 'http://www.wikidata.org/entity/Q56850065'], 
                            ['1', '0', 'http://www.wikidata.org/entity/Q20970432'], 
                            ['1', '1', 'http://www.wikidata.org/entity/Q20970432'], 
                            ['2', '0', 'http://www.wikidata.org/entity/Q651532'], 
                            ['2', '1', 'http://www.wikidata.org/entity/Q207659']], #cea
                           [['0', 1, 'http://www.wikidata.org/prop/direct/P2061'], 
                            ['0', 2, 'http://www.wikidata.org/prop/direct/P144']], #cpa
                           [['0', 'http://www.wikidata.org/entity/Q25110269'], 
                            ['1', 'http://www.wikidata.org/entity/Q20970434'], 
                            ['2', 'http://www.wikidata.org/entity/Q7725634']], #cta
                           [] #cqa
                           )

    return (subject_column, primary_annotations, secondary_annotations, 
            cea, cpa, cta, cqa)