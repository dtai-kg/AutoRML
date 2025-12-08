import json


def save_annotations(subject_column, primary_annotations,
                     secondary_annotations, cea, cpa, cta, cqa, path):

    annotation_object = {
            "subject_column": subject_column,
            "primary_annotations": primary_annotations,
            "secondary_annotations": secondary_annotations,
            "cea": cea,
            "cpa": cpa,
            "cta": cta,
            "cqa": cqa
        }

    with open(path, 'w') as file:
        json.dump(annotation_object, file, indent=4)
