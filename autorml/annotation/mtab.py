import requests
import pprint
import time
import sys
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def mtab(file):

    print("Querying the MTab API to retrieve semantic table annotations...")
    api_url = "https://mtab.kgraph.jp/api/v1/mtab"

    retry_count = 10
    backoff_factor = 2
    session = requests.Session()

    # Open the file in binary mode
    with open(file, 'rb') as table:
        # Create a dictionary for the file parameter to send
        files = {'file': table}

        # Make the POST request to the API
        response = None
        retrieve_success = False
        for attempt in range(retry_count):
            try:
                response = session.post(api_url, files=files, verify=False,
                                        timeout=(5, 10000))
                response.raise_for_status()
                retrieve_success = True
                break
            except requests.exceptions.RequestException as e:
                print(f"Attempt {attempt + 1} failed: {e}")
                wait_time = backoff_factor**attempt + (time.perf_counter() % 1)
                time.sleep(wait_time)
                retrieve_success = False

    # Check the status of the request
    if retrieve_success is True:
        # Parse the JSON response (assuming the API returns JSON)
        annotations = response.json()

        if annotations["tables"][0]["status"] == "Error":
            (subject_column, primary_annotations, secondary_annotations,
             new_cea, new_cpa, new_cta, cqa) = mtab(file)
        else:
            (subject_column, primary_annotations, secondary_annotations,
             new_cea, new_cpa, new_cta, cqa) =\
                 standard_annotation_formatter(annotations)
    else:
        sys.exit("Failed to annotate. Status code: "
                 f"{response.status_code}, Response: {response.text}")

    return (subject_column, primary_annotations, secondary_annotations,
            new_cea, new_cpa, new_cta, cqa)


def standard_annotation_formatter(annotations):

    # pprint.pprint(annotations)

    # Get subject column 
    subject_column =\
        int(annotations["tables"][0]["structure"]["core_attribute"])

    # Get CEA labels
    cea = annotations["tables"][0]["semantic"]["cea"]
    new_cea = []
    for cea_annotation in cea:
        if cea_annotation["target"][0] == 0:
            continue
        new_cea.append([str(cea_annotation["target"][0]),
                        str((cea_annotation["target"][1])),
                        cea_annotation["annotation"]["wikidata"]])

    # Get CPA labels
    cpa = annotations["tables"][0]["semantic"]["cpa"]
    new_cpa = []
    for cpa_annotation in cpa:
        new_cpa.append([str(cpa_annotation["target"][0]),
                        str(cpa_annotation["target"][1]),
                        cpa_annotation["annotation"][0]["wikidata"]])

    # Get CTA labels
    cta = annotations["tables"][0]["semantic"]["cta"]
    new_cta = []
    ne_columns = []
    for cta_annotation in cta:
        ne_columns.append(int(cta_annotation["target"]))
        new_cta.append([str(cta_annotation["target"]),
                        cta_annotation["annotation"][0]["wikidata"]])

    # Get primary and secondary annotations
    n_cols = int(annotations["tables"][0]["structure"]["columns"])
    primary_annotations = ["L"]*n_cols
    secondary_annotations = ["Unknown"]*n_cols
    for i in range(len(primary_annotations)):
        if i in ne_columns: 
            primary_annotations[i] = "NE"
            secondary_annotations[i] = "NE"

    new_cpa = fill_missing_properties(new_cpa, subject_column,
                                      primary_annotations)
    new_cta = fill_missing_types(new_cta, subject_column, primary_annotations)
    cqa = []

    return (subject_column, primary_annotations, secondary_annotations,
            new_cea, new_cpa, new_cta, cqa)


def fill_missing_properties(cpa, subject_column, primary_annotations):

    object_columns = []
    for i in range(len(primary_annotations)):
        if i != subject_column:
            object_columns.append(i)

    object_columns_with_properies = []
    for property_annotation in cpa:
        object_columns_with_properies.append(int(property_annotation[1]))

    object_columns_without_properties = \
        [item for item in object_columns
         if item not in object_columns_with_properies]
    for object_column in object_columns_without_properties:
        cpa.append([str(subject_column), str(object_column), None])

    return cpa


def fill_missing_types(cta, subject_column, primary_annotations):

    ne_cols = []
    for i in range(len(primary_annotations)):
        if primary_annotations[i] == "NE" or i == subject_column:
            ne_cols.append(i)

    ne_cols_with_type = []
    for type_annotation in cta:
        ne_cols_with_type.append(int(type_annotation[0]))

    ne_cols_without_type =\
        [item for item in ne_cols if item not in ne_cols_with_type]
    for ne_column in ne_cols_without_type:
        cta.append([str(ne_column), None])

    return cta
