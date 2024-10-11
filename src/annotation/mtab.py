import requests 
import pprint
import time
import sys
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def mtab(file):

    print("Querying the MTab API to retrieve semantic table annotaions...")
    api_url = "https://mtab.kgraph.jp/api/v1/mtab"

    # Open the file in binary mode
    with open(file, 'rb') as table:
        # Create a dictionary for the file parameter to send
        files = {'file': table}
        
        # Make the POST request to the API
        retry_count = 10
        backoff_factor = 2
        retrieve_success = False
        for attempt in range(retry_count):
            try:
                response = requests.post(api_url, files=files, verify=False)
                response.raise_for_status()
                retrieve_success = True
                break
            except requests.exceptions.RequestException as e:
                time.sleep(backoff_factor**attempt)
                retrieve_success = False
        
    # Check the status of the request
    if retrieve_success == True:
        # Parse the JSON response (assuming the API returns JSON)
        annotations = response.json()
        if annotations["tables"][0]["status"] == "Error":
            #print("Error")
            (subject_column, primary_annotations, secondary_annotations, new_cea, new_cpa, new_cta, cqa) = mtab(file)
        (subject_column, primary_annotations, secondary_annotations, new_cea, new_cpa, new_cta, cqa) = standard_annotation_formatter(annotations)
    else:
        sys.exit(f"Failed to annotate. Status code: {response.status_code}, Response: {response.text}")

    return (subject_column, primary_annotations, secondary_annotations, new_cea, new_cpa, new_cta, cqa)

def standard_annotation_formatter(annotations):

    #pprint.pprint(annotations)

    # Get subject column 
    subject_column = int(annotations["tables"][0]["structure"]["core_attribute"])
    
    # Get CEA labels
    cea = annotations["tables"][0]["semantic"]["cea"]
    new_cea = []
    for cea_annotation in cea:
        new_cea.append([str(cea_annotation["target"][1]), str((cea_annotation["target"][0])-1), cea_annotation["annotation"]["wikidata"]])

    # Get CPA labels
    cpa = annotations["tables"][0]["semantic"]["cpa"]
    new_cpa = []
    for cpa_annotation in cpa:
        new_cpa.append([str(cpa_annotation["target"][0]), str(cpa_annotation["target"][1]), cpa_annotation["annotation"][0]["wikidata"]])
    
    # Get CTA labels
    cta = annotations["tables"][0]["semantic"]["cta"]
    new_cta = []
    ne_columns = []
    for cta_annotation in cta:
        ne_columns.append(int(cta_annotation["target"]))
        new_cta.append([str(cta_annotation["target"]), cta_annotation["annotation"][0]["wikidata"]])
    
    # Get primary and secondary annotations
    n_cols = int(annotations["tables"][0]["structure"]["columns"])
    primary_annotations = ["L"]*n_cols
    secondary_annotations = ["Unknown"]*n_cols
    for i in range(len(primary_annotations)):
        if i in ne_columns: 
            primary_annotations[i] = "NE"
            secondary_annotations[i] = "NE"

    cqa = []
    print(subject_column, primary_annotations, secondary_annotations, new_cea, new_cpa, new_cta, cqa)
    return (subject_column, primary_annotations, secondary_annotations, new_cea, new_cpa, new_cta, cqa)

# file = "/Users/ioannisdasoulas/Desktop/AutoRML/Data/Y3OHOKFF.csv"
# mtab(file)