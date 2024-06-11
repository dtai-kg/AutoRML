from subject_map import define_subject_column_subject_map, define_object_column_subject_map 
from predicate_object_map import define_subject_column_po_map

def define_term_maps(mappings, subject_column, primary_annotations, secondary_annotations, cea, cpa, cta, col_names):

    mappings["mappings"] = {}
    mappings["mappings"]["subjectTM"] = {"sources": ["sem-table"]} if cea else {"sources": ["table"]}
    mappings["mappings"]["subjectTM"] = define_subject_column_subject_map(
                                        mappings["mappings"]["subjectTM"], 
                                        subject_column, secondary_annotations, 
                                        cea, 
                                        col_names)
    mappings["mappings"]["subjectTM"] = define_subject_column_po_map(
                                        mappings["mappings"]["subjectTM"], 
                                        subject_column, primary_annotations, secondary_annotations, 
                                        cea, cpa, cta,
                                        col_names)

    if type(subject_column) == int:
        for column in range(len(primary_annotations)):
            if column != subject_column and primary_annotations[column] == "NE":
                mappings["mappings"][col_names[column]+"TM"] = {"sources": ["sem-table"]} if cea else {"sources": ["table"]}
                mappings["mappings"][col_names[column]+"TM"] = define_object_column_subject_map(
                    mappings["mappings"][col_names[column]+"TM"], column, primary_annotations, secondary_annotations, cea, col_names[column])
    
    elif type(subject_column) == list:
        for column in range(len(primary_annotations)):
            if column not in subject_column and primary_annotations[column] == "NE":
                mappings["mappings"][col_names[column]+"TM"] = {"sources": ["sem-table"]} if cea else {"sources": ["table"]}
                mappings["mappings"][col_names[column]+"TM"] = define_object_column_subject_map(
                    mappings["mappings"][col_names[column]+"TM"], column, primary_annotations, secondary_annotations, cea, col_names[column])


    return mappings