def define_term_maps(mappings, subject_column, primary_annotations, cea):

    mappings["mappings"] = {}
    mappings["mappings"]["subjectTM"] = {"sources": ["sem-table"]} if cea else {"sources": ["table"]}

    for column in range(len(primary_annotations)):
        if column != subject_column and primary_annotations[column] == "NE":
            mappings["mappings"]["column{}TM".format(str(column))] = {"sources": ["sem-table"]} if cea else {"sources": ["table"]}


    return mappings