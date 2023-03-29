import os, sys
import argparse
from tqdm import tqdm
import glob
import pickle
import time
import pandas as pd
import numpy as np
import joblib
from typing import Union

def createOpcodeDict(benignPath: str, malwarePath: str) -> dict:

    opcodeDict = dict()

    # for dirpath, dirnames, files in os.walk(datasetPath):
    #     for f in tqdm(files, desc = dirpath.split("/")[-1]):
    #         if f.endswith('.pickle'):
    #             with open(os.path.join(dirpath, f), "rb") as p:
    #                 opcodeSequence = pickle.load(p)
    #                 for opcode in opcodeSequence:
    #                     opcodeDict.add(opcode)

    global benignAmount
    benignAmount = 0
    for file in tqdm(os.listdir(benignPath), desc = benignPath.split("/")[-1]):
        benignAmount += 1
        with open(os.path.join(benignPath, file), "rb") as p:
            opcodeSequence = pickle.load(p)
            for opcode in opcodeSequence:
                opcodeDict[opcode] = 0
                
    global malwareAmount
    malwareAmount = 0
    for file in tqdm(os.listdir(malwarePath), desc = malwarePath.split("/")[-1]):
        malwareAmount += 1
        with open(os.path.join(malwarePath, file), "rb") as p:
            opcodeSequence = pickle.load(p)
            for opcode in opcodeSequence:
                opcodeDict[opcode] = 0

    return opcodeDict

def extractOpcodeFrequency(opcodeDict: dict, samplePath: str) -> None:
    
    for file in tqdm(os.listdir(samplePath), desc = samplePath.split("/")[-1]):
        # reset opcodeDict
        opcodeDict = dict.fromkeys(opcodeDict, 0)
        
        start = time.time()
        filename = file.split(".")[0]
        with open(os.path.join(samplePath, file), "rb") as p:
            opcodeSequence = pickle.load(p)
            for opcode in opcodeSequence:
                opcodeDict[opcode] += 1

        end = time.time()
        frequencyTime = end - start
        totalFeature.append([filename, frequencyTime, list(opcodeDict.values())])

def train_and_predict(benignAmount: int, malwareAmount: int, train_ratio: float) -> Union[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    
    # Create label
    # Given benign and malware amount to create y_label 
    benign_label = np.zeros(benignAmount)
    malware_label = np.ones(malwareAmount)
 
    yLabel = np.append(benign_label, malware_label)

    xData = np.vstack(totalFeatureDf["feature"])
    
    # Prepare train test data
    from sklearn.model_selection import train_test_split
    X_train, X_test, y_train, y_test = train_test_split(xData, yLabel, train_size = float(train_ratio), random_state = 42)

    print("xData shape :", xData.shape)
    print("yLabel shape :", yLabel.shape)
    print()
    print("X_train shape :", X_train.shape)
    print("y_train shape :", y_train.shape)
    print()
    print("X_test shape :", X_test.shape)
    print("y_test shape :", y_test.shape)

    return X_train, X_test, y_train, y_test

def RandomForestModel(_max_depth: int, X_train: pd.DataFrame, y_train: pd.DataFrame, modelName: str) -> None:
    
    from sklearn.ensemble import RandomForestClassifier

    # train
    clf = RandomForestClassifier(max_depth = _max_depth, random_state = 0)

    start = time.time()
    clf.fit(X_train, y_train)
    stop = time.time()

    # save model
    joblib.dump(clf, modelName)

    print()
    print(f"Training time: {stop - start} s")

def Predict(X_test: pd.DataFrame, y_test: pd.DataFrame, model: object) -> None:
    
    start = time.time()
    predict = model.predict(X_test)
    stop = time.time()

    # evalution
    acc = 0
    for i in range(len(y_test)):
        if y_test[i] == predict[i]:
            acc = acc + 1

    print()
    print(f"Predicting time: {stop - start} s")
    print()
    print("Accuracy :", acc/len(y_test))
    print()

def get_parser():
    parser = argparse.ArgumentParser(description = "OpcodeFrequency")
    parser.add_argument("-b", "--benign", type = str, help = "Enter source path for benign")
    parser.add_argument("-m", "--malware", type = str, help = "Enter source path for malware")
    parser.add_argument("-r", "--train_ratio", type = str, help = "Enter train ratio")
    return parser

if __name__ == "__main__":
    
    parser = get_parser()
    args = parser.parse_args()

    # collect all the opcode in the dataset including packed and unpacked
    print("[+] Create Unique Opcode Dict")
    opcodeDict = createOpcodeDict(args.benign, args.malware)
    
    with open('opcodeDict.pickle', 'wb') as f:
        pickle.dump(opcodeDict, f)

    global totalFeature
    totalFeature = []

    # extract opcode frequency for each samples and append in global totalFeature list
    print("[+] Extracting Opcode Frequency")
    extractOpcodeFrequency(opcodeDict, args.benign)
    extractOpcodeFrequency(opcodeDict, args.malware)

    totalFeatureDf = pd.DataFrame(totalFeature)
    totalFeatureDf.columns = ["filename", "frequencyTime", "feature"]

    print()
    print(" ====== totalFeatureDf Info ====== ")
    print()
    print("totalFeatureDf shape :", totalFeatureDf.shape)
    print("feature shape :", len(totalFeatureDf["feature"].iloc[0]))
    print(totalFeatureDf)

    totalFeatureDf.to_csv("totalFeatureDf.csv", index = False)

    # Train & Predict
    X_train, X_test, y_train, y_test = train_and_predict(benignAmount, malwareAmount, args.train_ratio)

    for depth in [2, 3, 5, 10, 15, 30, 50, 100, 1000]:
        print()
        print("【Depth】", depth)
        RandomForestModel(depth, X_train, y_train, "./model/opcodeFrequency_RF_" + str(depth))

        model = joblib.load("./model/opcodeFrequency_RF_" + str(depth))

        Predict(X_test, y_test, model)


    # python3 opcodeFrequency.py -b ../NICT/DataSet/Toyset/OpcodeSequence/toy_benign_packed -m ../NICT/DataSet/Toyset/OpcodeSequence/toy_malware_packed
