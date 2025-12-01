from torchic_tab_heuristic.task_calculation_wd import generate_annotations #Closed source. Contact for access


#Call of TorchicTab to extract tabular annotations for a given table
def torchic_tab(file):

    es_index = False
    (subject_column, primary_annotations, secondary_annotations,
     cea, cpa, cta) = generate_annotations(file, es_index)
    cqa = []

    return (subject_column, primary_annotations, secondary_annotations, 
            cea, cpa, cta, cqa)
