import json
import os
from tqdm import tqdm
import argparse

DEST_DIR = './label_data'
LABELING_RESULT_DIR = './라벨링결과-20221001.010519.json'


if __name__ == "__main__":
    with open(LABELING_RESULT_DIR, "r") as label_json:
        label_dict = json.load(label_json)
        count = label_dict["count"]
        label_list = label_dict["labels"]
        
    label_json.close()

    student_dict = {}
    for i in tqdm(range(count), desc = "Parsing label json"):
        studentId = label_list[i]["studentId"]
        questionId = label_list[i]["questionId"]
        subquestionType = label_list[i]["subquestionType"]
        annotation = label_list[i]["annotation"]

        if studentId not in student_dict:
            student_dict[studentId] = {}
        if questionId not in student_dict[studentId]:
            student_dict[studentId][questionId] = {}
        student_dict[studentId][questionId][subquestionType] = annotation

    try:
        os.mkdir(DEST_DIR)
    except FileExistsError:
        pass

    for studentId in tqdm(student_dict, desc = "Convert to json"):
        # check if directory "jsons/" + studentId exists
        try:
            os.mkdir(f"{DEST_DIR}/{studentId}")
        except FileExistsError:
            pass
                
        for questionId in student_dict[studentId]:

            json_data = {
                "student_id": studentId,
                "question_id": questionId,
                "labels": {
                    "STAGE_BASE": {
                        "annotation": student_dict[studentId][questionId]["BASE"]
                    },
                    "STAGE_COMPREHENSION": {
                        "annotation": student_dict[studentId][questionId]["COMPREHENSION"]
                    },
                    "STAGE_EMOTION": {
                        "annotation": student_dict[studentId][questionId]["EMOTION"]
                    }
                }
            }
            dir_path = f"{DEST_DIR}/{studentId}/{questionId}.json"
            #check if directory exists
            
            with open(dir_path, 'w') as f:
                json.dump(json_data, f, indent=4, ensure_ascii=False)