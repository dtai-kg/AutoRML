import re


# Define the Predicate-Object Maps for the Subject Column
def define_subject_column_po_map(subjectTM, subject_column,
                                 primary_annotations, secondary_annotations,
                                 cea, cpa, cta, col_names):

    property_template_prefix = "http://example.com/property/"
    type_template_prefix = "http://example.com/entityType/"
    entity_template_prefix = "http://example.com/entity/"
    rdf_type_shortcut = "a"
    cta_label = None

    subjectTM["po"] = []

    # Definition of rdf:type Predicate-Object Map
    if subject_column == -1 or subject_column is None or not cta:
        # If the Subject Column does not exist or if we do not have
        # CTA information, we use a dummy template rdf type.
        # This can then be manually processed, be replaced with a blank node
        # or a mapping function that calls a service for retrieving CTA
        subjectTM["po"].append({"p": rdf_type_shortcut,
                                "o": type_template_prefix + "subjectType"})
    else:
        for cta_data in cta:
            first_pred = int(cta_data[0]) == subject_column
            second_pred = [int(cta_data[0])] == subject_column
            if first_pred or second_pred:
                cta_label = cta_data[1]
                break
        if cta_label:
            subjectTM["po"].append({"p": rdf_type_shortcut,
                                    "o": cta_label})
        else:
            subjectTM["po"].append({"p": rdf_type_shortcut,
                                    "o": type_template_prefix + "subjectType"})

    # Definition of the rest of Predicate-Object Maps for table without a
    # subject column
    # All columns can potentially be Object Columns. We decide according to
    # available information
    # CPA is not possible without a subject column so we use dummy constant
    # properties to define the predicate maps.
    # These can then be manually processed or retrieved by a mapping function
    if subject_column == -1 or subject_column is None:

        for i in range(len(primary_annotations)):

            # If a Named Entity Object Column is of type IRI, we can use its
            # IRIs as reference to define the object maps
            primary_if = primary_annotations[i] == "NE"
            secondary_if = secondary_annotations[i] == "URL"
            if primary_if and secondary_if and cea == []:
                subjectTM["po"].append({"p": property_template_prefix +
                                        "s-{}".format(
                                            ensure_valid_url(col_names[i])),
                                        "o": "$({})~iri".format(col_names[i])})
                continue

            # Named Entity Object Columns
            if primary_annotations[i] == "NE":
                # If CEA are available, a reference to the annotation IRIs is
                # used
                if cea:
                    subjectTM["po"].append({"p": property_template_prefix +
                                            "s-{}".format(
                                                ensure_valid_url(
                                                    col_names[i])),
                                            "o": [{"value": "$({})".format(
                                                ensure_valid_url(
                                                    col_names[i])),
                                                   "type": "iri"}]})

                # If CEA are not available, a dummy template value is used
                # This can then be manually processed, be replaced with a blank
                # node or a mapping function that calls a service for
                # retrieving CEA
                else:
                    value = entity_template_prefix + \
                            "$({})".format(ensure_valid_url(col_names[i]))
                    subjectTM["po"].append({"p": property_template_prefix +
                                            "s-{}".format(ensure_valid_url
                                                          (col_names[i])),
                                            "o": [{"value": value,
                                                   "type": "iri"}]})

            # Literal Object Columns
            elif primary_annotations[i] == "L":

                # For literal columns we can add a reference to the column.
                # This can be manually replaced with a template, according to
                # the use case.
                # If datatypes are also available we can add them as well.
                xsd_type = map_datatype_to_xsd(secondary_annotations[i])
                if xsd_type is None:
                    subjectTM["po"].append({"p": property_template_prefix +
                                            "s-{}".format(ensure_valid_url
                                                          (col_names[i])),
                                            "o": [{"value":  "$({})"
                                                   .format(col_names[i])}]})
                else:
                    subjectTM["po"].append({"p": property_template_prefix +
                                            "s-{}".format(ensure_valid_url
                                                          (col_names[i])),
                                            "o": [{"value":  "$({})"
                                                   .format(col_names[i]),
                                                   "datatype": xsd_type}]})

    # Else if the table has a subject column
    else:
        if isinstance(subject_column, int):
            subject_column = [subject_column]

        # If we have CPA annotations use them to define the predicate map
        if cpa:

            for s, o, p in cpa:

                # Check for missing annotations
                if p is None or p[-3:] == "/P1":
                    p = property_template_prefix + \
                        "{}-{}".format(ensure_valid_url(
                            col_names[int(s)]),
                                       ensure_valid_url(col_names[int(o)]))

                if int(s) in subject_column:

                    # If a Named Entity Object Column is of type IRI, we can
                    # use its IRIs as reference to define the object maps
                    primary_if = primary_annotations[int(o)] == "NE"
                    secondary_if = secondary_annotations[int(o)] == "URL"
                    if primary_if and secondary_if and cea == []:
                        subjectTM["po"].append({"p": p,
                                                "o": "$({})~iri"
                                                .format(col_names[int(o)])})
                        continue

                    # If the Object Column is a Named Entity Column
                    if primary_annotations[int(o)] == "NE":

                        # If CEA are available, a reference to the annotation
                        # IRIs is used
                        if cea:
                            subjectTM["po"].append({"p": p,
                                                    "o": [{"value": "$({})"
                                                           .format(col_names
                                                                   [int(o)]),
                                                           "type": "iri"}]})

                        # If CEA are not available, a dummy template value is
                        # used
                        # This can then be manually processed, be replaced
                        # with a blank node or a mapping function that calls a
                        # service for retrieving CEA
                        else:
                            value = entity_template_prefix + \
                                    "$({})".format(col_names[int(o)])
                            subjectTM["po"].append({"p": p,
                                                    "o": [{"value": value,
                                                           "type": "iri"}]})

                    # If the Object Column is a Literal Column
                    elif primary_annotations[int(o)] == "L":

                        # For literal columns we can add a reference to the
                        # column.
                        # This can be manually replaced with a template,
                        # according to the use case.
                        # If datatypes are also available we can add them as
                        # well.
                        xsd_type = map_datatype_to_xsd(
                            secondary_annotations[int(o)])
                        if xsd_type is None:
                            subjectTM["po"].append({"p": p,
                                                    "o": [{"value":  "$({})"
                                                           .format(col_names
                                                                   [int(o)]
                                                                   )}
                                                          ]})
                        else:
                            subjectTM["po"].append({"p": p,
                                                    "o": [{"value":  "$({})"
                                                           .format(col_names
                                                                   [int(o)]),
                                                           "datatype":
                                                               xsd_type}]})

        # If we do not have CPA annotations we use dummy constant properties
        # to define the predicate maps. These can then be manually processed or
        # retrieved by a mapping function
        elif not cpa:

            for i in range(len(primary_annotations)):

                if i in subject_column:
                    continue

                # If a Named Entity Object Column is of type IRI, we can use
                # its IRIs as reference to define the object maps
                primary_if = primary_annotations[i] == "NE"
                secondary_if = secondary_annotations[i] == "URL"
                if primary_if and secondary_if and cea == []:
                    subjectTM["po"].append({"p": property_template_prefix +
                                            "s-{}".format(ensure_valid_url(
                                                col_names[i])),
                                            "o": "$({})~iri"
                                            .format(col_names[i])})
                    continue

                # Named Entity Object Columns
                if primary_annotations[i] == "NE":
                    # If CEA are available, a reference to the annotation IRIs
                    # is used
                    if cea:
                        subjectTM["po"].append({"p": property_template_prefix +
                                                "s-{}".format(ensure_valid_url
                                                              (col_names[i])),
                                                "o": [{"value": "$({})"
                                                       .format(col_names[i]),
                                                       "type": "iri"}]})

                    # If CEA are not available, a dummy template value is used
                    # This can then be manually processed, be replaced with a
                    # blank node or a mapping function that calls a service for
                    # retrieving CEA
                    else:
                        value = entity_template_prefix + \
                                "$({})".format(ensure_valid_url(col_names[i]))
                        subjectTM["po"].append({"p": property_template_prefix +
                                                "s-{}".format(ensure_valid_url
                                                              (col_names[i])),
                                                "o": [{"value": value,
                                                       "type": "iri"}]})

                # Literal Object Columns
                elif primary_annotations[i] == "L":

                    # For literal columns we can add a reference to the column.
                    # This can be manually replaced with a template, according
                    # to the use case. If datatypes are also available we can
                    # add them as well.
                    xsd_type = map_datatype_to_xsd(secondary_annotations[i])
                    if xsd_type is None:
                        value = "$({})".format(col_names[i])
                        subjectTM["po"].append({"p": property_template_prefix +
                                                "s-{}".format(
                                                    ensure_valid_url(
                                                        col_names[i])),
                                                "o": [{"value":  value}]})
                    else:
                        subjectTM["po"].append({"p": property_template_prefix +
                                                "s-{}".format(
                                                    ensure_valid_url(
                                                        col_names[i])),
                                                "o": [{"value":  "$({})"
                                                       .format(col_names[i]),
                                                       "datatype": xsd_type}]})

    return subjectTM


# Define the Predicate-Object Maps for the Subject Column
def define_object_column_po_map(objectTM, column, cta, col_name):

    type_template_prefix = "http://example.com/entityType/"
    rdf_type_shortcut = "a"
    cta_label = None

    objectTM["po"] = []

    # Definition of rdf:type Predicate-Object Map
    if not cta:
        # If do not have CTA information, we use a dummy template rdf type.
        # This can then be manually processed, be replaced with a blank node
        # or a mapping function that calls a service for retrieving CTA
        objectTM["po"].append({"p": rdf_type_shortcut,
                               "o": type_template_prefix +
                               ensure_valid_url(col_name)})
    else:
        for cta_data in cta:
            if int(cta_data[0]) == column:
                cta_label = cta_data[1]
                break
        if cta_label:
            objectTM["po"].append({"p": rdf_type_shortcut,
                                   "o": cta_label})
        else:
            objectTM["po"].append({"p": rdf_type_shortcut,
                                   "o": type_template_prefix +
                                   ensure_valid_url(col_name)})

    return objectTM


def ensure_valid_url(string):

    # Replace spaces and remove any non-alphanumeric characters except
    # underscores
    string = re.sub(r'\s+', '_', string)
    string = re.sub(r'[^a-zA-Z0-9_]', '', string)

    return string


def map_datatype_to_xsd(secondary_annotation):

    default_datatype = None

    # Mapping of common secondary annotation to xsd datatypes
    xsd_mappings = {
        "BOOLEAN": "xsd:boolean",
        "INT": "xsd:int",
        "FLOAT": "xsd:float",
        "STRING": "xsd:string",
        "TIME": "xsd:string",
        "PHONE": "xsd:string",
        "URL": "xsd:anyURI",
        "EMAIL": "xsd:string",
        "IP": "xsd:string",
        "HEX": "xsd:string",
        "CREDIT_CARD": "xsd:string",
        "ADDRESS": "xsd:string",
        "COORDS": "xsd:string",
        "ISBN": "xsd:string",
    }

    if secondary_annotation in xsd_mappings:
        return xsd_mappings[secondary_annotation]
    else:
        return default_datatype
