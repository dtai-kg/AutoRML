# Definition of the Subject Map for the Subject Column of the table
def define_subject_column_subject_map(subjectTM, subject_column,
                                      secondary_annotations, cea, col_names):

    # If no Subject Column within table, no subject defined which
    # will lead to the creation of blank nodes for subject
    if subject_column == -1 or subject_column is None:
        subjectTM["s"] = [{"value": "Blank", "type": "blank"}]
        return subjectTM

    # Define the reference of the subject column(s) in YARRRML
    if isinstance(subject_column, int):
        subject_column_ref = "$({})".format(col_names[subject_column])
    else:
        subject_column_ref = ""
        for i in range(len(subject_column)):
            subject_column_ref += "$({})".format(col_names[subject_column[i]])
            if i < len(subject_column) - 1:
                subject_column_ref += "/"

    # If Subject Column is of IRI type, we can use a reference to the IRIs, 
    # since subject columns are always Named Entity Columns
    primary_condition = isinstance(subject_column, int)
    secondary_condition = secondary_annotations[subject_column] == "URL"
    if primary_condition and secondary_condition and cea == []:
        subjectTM["s"] = subject_column_ref
        return subjectTM

    # If CEA are available, a reference to the annotation IRIs is used
    if cea:
        subjectTM["s"] = subject_column_ref
        return subjectTM

    # If CEA are not available, a dummy template value is used 
    # This can then be manually processed, be replaced with a blank node 
    # or a mapping function that calls a service for retrieving CEA
    else:
        entity_template_prefix = "http://example.com/entity/"
        subjectTM["s"] = entity_template_prefix + subject_column_ref
        return subjectTM


# Definition of the Subject Map for the Named Entity Object Columns of the
# table
def define_object_column_subject_map(objectTM, object_column,
                                     primary_annotations,
                                     secondary_annotations, cea, col_name):

    # If Object Column is a Named Entity Column and is of IRI type,
    # we can use a reference to the IRIs
    primary_condition = primary_annotations[object_column] == "NE"
    secondary_condition = secondary_annotations[object_column] == "URL"
    if primary_condition and secondary_condition:
        objectTM["s"] = "$({})".format(col_name)
        return objectTM

    # If CEA are available, a reference to the annotation IRIs is used
    if cea:
        objectTM["s"] = "$({})".format(col_name)
        return objectTM

    # If CEA are not available, a dummy template value is used 
    # This can be manually processed by the user or be replaced with 
    # a mapping function that calls a service for retrieving CEA
    else:
        entity_template_prefix = "http://example.com/entity/"
        objectTM["s"] = entity_template_prefix + "$({})".format(col_name)
        return objectTM
