import requests 
import pprint
import time
import sys

def mtab(file):

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
            standard_annotation_formatter(annotations)
        else:
            sys.exit(f"Failed to annotate. Status code: {response.status_code}, Response: {response.text}")

    return

def standard_annotation_formatter(annotations):

    pprint.pprint(annotations)

    subject_column = int(annotations["tables"][0]["structure"]["core_attribute"])
    
    cea = annotations["tables"][0]["semantic"]["cea"]
    new_cea = []
    for cea_annotation in cea:
        new_cea.append([str(cea_annotation["target"][1]), str((cea_annotation["target"][0])-1), cea_annotation["annotation"]["wikidata"]])

    cpa = annotations["tables"][0]["semantic"]["cpa"]
    new_cpa = []
    for cpa_annotation in cpa:
        new_cpa.append([str(cpa_annotation["target"][0]), str(cpa_annotation["target"][1]), cpa_annotation["annotation"][0]["wikidata"]])
    
    cta = annotations["tables"][0]["semantic"]["cta"]
    new_cta = []
    for cta_annotation in cta:
        new_cta.append([str(cta_annotation["target"]), cta_annotation["annotation"][0]["wikidata"]])

    return

file = "/Users/ioannisdasoulas/Desktop/AutoRML/Data/Y3OHOKFF.csv"
mtab(file)