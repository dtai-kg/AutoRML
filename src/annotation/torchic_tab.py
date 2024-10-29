from torchic_tab_heuristic.task_calculation_wd import generate_annotations #Closed source. Contact for access

#Call of TorchicTab to extract tabular annotations for a given table
def torchic_tab(file):

    (subject_column, primary_annotations, secondary_annotations, 
    cea, cpa, cta) = generate_annotations(file)
    cqa = []

    # Test Annotations
    # (subject_column, primary_annotations, secondary_annotations, 
    # cea, cpa, cta, cqa) = (0, #subject_column_index
    #                        ['NE', 'L', 'NE'], #named_entity_columns_index
    #                        ['NE', 'Unknown', 'NE'], #datatype_index (for literal columns)
    #                        [['0', '0', 'http://www.wikidata.org/entity/Q15865202'], 
    #                         ['0', '1', 'http://www.wikidata.org/entity/Q56850065'], 
    #                         ['1', '0', 'http://www.wikidata.org/entity/Q20970432'], 
    #                         ['1', '1', 'http://www.wikidata.org/entity/Q20970432'], 
    #                         ['2', '0', 'http://www.wikidata.org/entity/Q651532'], 
    #                         ['2', '1', 'http://www.wikidata.org/entity/Q207659']], #cea
    #                        [['0', 1, 'http://www.wikidata.org/prop/direct/P2061'], 
    #                         ['0', 2, 'http://www.wikidata.org/prop/direct/P144']], #cpa
    #                        [['0', 'http://www.wikidata.org/entity/Q25110269'], 
    #                         ['1', 'http://www.wikidata.org/entity/Q20970434'], 
    #                         ['2', 'http://www.wikidata.org/entity/Q7725634']], #cta
    #                        [] #cqa
    #                        )

    # Test Annotations2
#     (subject_column, primary_annotations, secondary_annotations, 
#     cea, cpa, cta, cqa) = (0, 
# ['NE', 'NE', 'NE'], 
# ['NE', 'ORG', 'NE'], 
# [['0', '0', 'http://www.wikidata.org/entity/Q962677'], ['0', '1', 'http://www.wikidata.org/entity/Q5322348'], ['0', '2', 'http://www.wikidata.org/entity/Q906937'], ['1', '0', 'http://www.wikidata.org/entity/Q773662'], ['1', '1', 'http://www.wikidata.org/entity/Q773662'], ['1', '2', 'http://www.wikidata.org/entity/Q181912'], ['2', '0', 'http://www.wikidata.org/entity/Q4356221'], ['2', '1', 'http://www.wikidata.org/entity/Q2443635'], ['2', '2', 'http://www.wikidata.org/entity/Q21044913']], 
# [['0', 1, 'http://www.wikidata.org/prop/direct/P137'], ['0', 2, 'http://www.wikidata.org/prop/direct/P1']], 
# [['0', 'http://www.wikidata.org/entity/Q15056993'], ['1', 'http://www.wikidata.org/entity/Q46970'], ['2', 'http://www.wikidata.org/entity/Q4167410']], [])
    
    # print((subject_column, primary_annotations, secondary_annotations, 
    # cea, cpa, cta, cqa))
    return (subject_column, primary_annotations, secondary_annotations, 
            cea, cpa, cta, cqa)