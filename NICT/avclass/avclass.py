import json
import os
import re
import sys
from tqdm import tqdm

def readJson(path: str) -> dict:
    
    with open(path, newline = '') as jsonfile:
        data = json.load(jsonfile)

    return data

def store_new_result(data: dict) -> bool:
    
    json_object = json.dumps(data)

    try:
        with open("./fixed.json", "w") as outfile:
            outfile.write(json_object)
            return True
    except:
        return False

def analysis_avclass_output(filename:str , path: str) -> dict:

    with open(path, 'r') as f:
        data = f.read()
        
    filename = filename.split(".")[0]

    detail = re.split("\t", data)[-1]

    detail = re.split("\|\d+,|\n|\|\d+", detail)

    detail = [i for i in detail if i != '']

    av_detail = dict()

    for d in detail:
        detailList = d.rsplit(":", 1)

        try:
            av_detail.update({detailList[0]: detailList[1]})
        except:
            print(filename, detail)

    av = dict()
    av.update({filename: av_detail})
    # print(av)
    return av

if __name__ == "__main__":

    # argv
    n = len(sys.argv) - 1
    if n != 1:
        print("[x] Please enter data file.")
        sys.exit()

    dataPath = sys.argv[1]

    total_avclass = dict()

    for d in tqdm(sorted(os.listdir(dataPath)), desc = "All"):
        if len(d) == 2:
            for f in tqdm(os.listdir(dataPath + d), desc = d):
                data = readJson(dataPath + d + "/" + f)
                store_new_result(data)
                # perform avclass
                os.system("~/avclass/avclass2/avclass2_labeler.py -vt ./fixed.json -p > /dev/null 2>&1 > avclassOutput.txt")
                total_avclass.update(analysis_avclass_output(f, "./avclassOutput.txt"))  
    
    # store total avclass
    with open("./new_total_avclass.json", "w") as outfile:
        json.dump(total_avclass, outfile)

    