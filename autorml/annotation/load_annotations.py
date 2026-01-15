import json


def load_annotations(filename: str):

    with open(filename, "r") as f:
        annotations = json.load(f)

    return (annotations["subject_column"],
            annotations["primary_annotations"],
            annotations["secondary_annotations"],
            annotations["cea"],
            annotations["cpa"],
            annotations["cta"],
            annotations["cqa"])
