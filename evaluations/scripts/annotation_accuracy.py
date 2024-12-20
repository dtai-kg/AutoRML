import os 
import pandas as pd
from utils import read_json

def get_gt_annotations_by_filename(gt_file_path, file_name):

    df = pd.read_csv(gt_file_path, header=None)
    matching_rows = df[df[0] == file_name]

    if "cta" in gt_file_path:
        gt_list = matching_rows[[1, 2]].values.tolist()
    else:
        gt_list = matching_rows[[1, 2, 3]].values.tolist()

    return gt_list

def assess_task_accuracy(task, annotations_file_path, gt_path, file_name):

    task_gt = get_gt_annotations_by_filename(gt_path, file_name)
    annotations = read_json(annotations_file_path)

    task_results = annotations[task]

    #Assert same datatype (int as in ground truth)
    for annotation in task_results:
        annotation[0] = int(annotation[0])
        if task == "cpa" or task == "cea":
            annotation[1] = int(annotation[1])

    for annotation in task_gt:
        if annotation not in task_results:
            return False, None

    #Check if there exist excessive cea labels  
    if task == "cea":
        cea_gt_colums = []
        cea_results_columns = []
        for cea_gt_annotation in task_gt:
            if cea_gt_annotation[1] not in cea_gt_colums: cea_gt_colums.append(cea_gt_annotation[1])
        for cea_results_annotation in task_results:
            if cea_results_annotation[1] not in cea_results_columns: cea_results_columns.append(cea_results_annotation[1])
        if cea_gt_colums != cea_results_columns: return False, None
        
    return True, task_gt

def assess_annotations_accuracy(file_name, data_collection, sta_system):

    annotations_path = "evaluations/annotations"
    ground_truth_path = "evaluations/ground_truth"

    cea_gt_filename = "cea_gt.csv"
    cpa_gt_filename = "cpa_gt.csv"
    cta_gt_filename = "cta_gt.csv"

    annotations_file_path = os.path.join(annotations_path, data_collection, sta_system, file_name + ".json")
    cea_gt_path = os.path.join(ground_truth_path, data_collection, cea_gt_filename)
    cpa_gt_path = os.path.join(ground_truth_path, data_collection, cpa_gt_filename)
    cta_gt_path = os.path.join(ground_truth_path, data_collection, cta_gt_filename)

    cta_check, cta_gt = assess_task_accuracy("cta", annotations_file_path, cta_gt_path, file_name)
    if cta_check == False: return False, None, None, None

    cpa_check, cpa_gt = assess_task_accuracy("cpa", annotations_file_path, cpa_gt_path, file_name)
    if cpa_check == False: return False, None, None, None

    cea_check, cea_gt = assess_task_accuracy("cea", annotations_file_path, cea_gt_path, file_name)
    if cea_check == False: return False, None, None, None
    

    return True, cea_gt, cpa_gt, cta_gt

