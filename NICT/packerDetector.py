import json
import pandas as pd
from sklearn.model_selection import train_test_split
from tqdm import tqdm
import os
from sklearn.ensemble import RandomForestClassifier
import sys

def readData(filepath: str) -> pd.DataFrame:

    print("[+] Reading Data...")

    with open(filepath, "r", encoding = "utf-8") as f:

        data = json.load(f)

    data = pd.DataFrame.from_dict(data, orient = "index")

    return data

def createFeature(data: pd.DataFrame) -> pd.DataFrame:
    
    print("[+] Creating Feature...")

    feature = pd.DataFrame()

    # cauclate mean
    feature["mean"] = data.mean(axis = 1)

    # cauclate max
    feature["max"] = data.max(axis = 1)

    # cauclate min
    feature["min"] = data.min(axis = 1)

    return feature

def createLabel(dataPath: str, packerPath: str, storePath) -> pd.DataFrame:

    print("[+] Creating Label...")

    if os.path.exists(storePath):

        print("packer_label.json already exists >_<")

    else:

        with open(dataPath, "r", encoding = "utf-8") as f:

            data = json.load(f)

        with open(packerPath, "r", encoding = "utf-8") as f:

            packed = json.load(f)

        label = {}

        for d in tqdm(data, desc = "[+] Extracting label..."):
            if d in packed.keys():
                label.update({d: 1})
            else:
                label.update({d: 0})
            
        # store json
        with open(storePath, "w") as outfile:
            json.dump(label, outfile)

    # load packer label
    label = pd.read_json(storePath, orient = "index")

    return label.sort_index()

def evalution(predict: list, answer: list) -> float:
    
    hit = 0

    for p in range(len(predict)):
        if predict[p] == answer[p]:
            hit += 1

    return hit/len(predict)
            

if __name__ == "__main__":

    # argv
    n = len(sys.argv) - 1
    if n != 1:
        print("[x] Please enter entropy json file.")
        sys.exit()

    data = readData(sys.argv[1])

    feature = createFeature(data)

    label = createLabel("/data/Data.json", "/data/packed_version.json", "./packer_label.json")

    # merge feature and label
    feature["label"] = label

    print(feature)

    # training
    X = feature[["mean", "max", "min"]]
    y = feature["label"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)

    print("\nTraining shape:", len(X_train))
    print("Testing shape:", len(X_test))

    clf = RandomForestClassifier(max_depth=100, random_state=0)
    clf.fit(X_train, y_train)

    # testing
    predict = clf.predict(X_test)

    # evalution
    accuracy = evalution(predict, y_test)
    print("\nAccuracy:", accuracy)

