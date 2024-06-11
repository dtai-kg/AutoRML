# Define the Predicate-Object Maps for the Subject Column
def define_subject_column_po_map(subjectTM, subject_column, primary_annotations, secondary_annotations, cea, cpa, cta, col_names):

    property_template_prefix = "http://example.com/property/"
    type_template_prefix = "http://example.com/entityType/"
    entity_template_prefix = "http://example.com/entity/"
    rdf_type_shortcut = "a"

    subjectTM["po"] = []
    
    # Definition of rdf:type Predicate-Object Map
    if subject_column == -1 or not cta:
        # If the Subject Column does not exist or if we don not have
        # CTA information, we use a dummy template rdf type. 
        # This can then be manually processed, be replaced with a blank node 
        # or a mapping function that calls a service for retrieving CTA
        subjectTM["po"].append({"p": rdf_type_shortcut, 
                                "o": type_template_prefix + "subjectType"})
    else:
        for cta_data in cta:
            if int(cta_data[0]) == subject_column:
                cta_label = cta_data[1]
                break
        if cta_label:
            subjectTM["po"].append({"p": rdf_type_shortcut, 
                                    "o": cta_label})
        else:
            subjectTM["po"].append({"p": rdf_type_shortcut, 
                                    "o": type_template_prefix + "subjectType"})
    
    # Definition of the rest of Predicate-Object Maps for table without a subject column
    # All columns can potentially be Object Columns. We decide according to available information
    # CPA is not possible without a subject column so we use dummy constant properties to define the predicate maps.
    # These can then be manually processed or retrieved by a mapping function
    if subject_column == -1: 

        # If a Named Entity Object Column is of type IRI, we can use its IRIs as reference
        # to define the object maps
        for i in range(len(primary_annotations)):

            if primary_annotations[i] == "NE" and secondary_annotations[i] == "URL" and cea==[]:
                subjectTM["po"].append({"p": property_template_prefix + "s-{}".format(col_names[i]), 
                                        "o": "$({})~iri".format(col_names[i])})

            # Named Entity Object Columns
            if primary_annotations[i] == "NE":
                #If CEA are available, a reference to the annotation IRIs is used
                if cea:
                    subjectTM["po"].append({"p": property_template_prefix + "s-{}".format(col_names[i]), 
                                            "o": "$({})~iri".format(col_names[i])})
                
                #If CEA are not available, a dummy template value is used 
                #This can then be manually processed, be replaced with a blank node 
                # or a mapping function that calls a service for retrieving CEA
                else:
                    subjectTM["po"].append({"p": property_template_prefix + "s-{}".format(col_names[i]), 
                                            "o": entity_template_prefix + "$({})~iri".format(col_names[i])})
                    
            # Literal Object Columns
            elif primary_annotations[i] == "L":

                # For literal columns we can add a reference to the column.
                # This can be manually replaced with a template, according to the use case.
                # If datatypes are also available we can add them as well.
                xsd_type = map_datatype_to_xsd(secondary_annotations[i])
            

    return subjectTM


def map_datatype_to_xsd(secondary_annotation):

    #Mapping of common secondary annotation to xsd datatypes
    xsd_mappings = {
        "BOOLEAN": "xsd:boolean",
        "INT": "xsd:int",
        "FLOAT": "xsd:float",
        "STRING": "xsd:string",
        "DATE": "xsd:date",
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

    return