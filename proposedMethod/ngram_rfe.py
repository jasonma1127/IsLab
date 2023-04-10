from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
from sklearn.feature_selection import RFECV
from sklearn.feature_selection import RFE
import os
import argparse
from tqdm import tqdm
import pickle
import time
import joblib
import numpy as np
import pandas as pd

def loadPickle(file_path: str) -> pickle:
    with open(file_path, "rb") as f:
        pk = pickle.load(f)
    return pk

def createCorpusDataset(benignPath: str, malwarePath: str) -> list and list:
    opcode_corpus = []
    label = []
    for file in tqdm(os.listdir(benignPath), desc="Benign"):
        opcode_corpus.append(" ".join(loadPickle(os.path.join(benignPath, file))))
        label.append(0)

    for file in tqdm(os.listdir(malwarePath), desc="Malware"):
        opcode_corpus.append(" ".join(loadPickle(os.path.join(malwarePath, file))))
        label.append(1)
    return opcode_corpus, label

def TFIDFvec(X: list, ng_min: int, ng_max: int) -> np.array:
    vectorizer = TfidfVectorizer(ngram_range = (ng_min, ng_max))
    return vectorizer.fit_transform(X)

def Countvec(X: list, ng_min: int, ng_max: int) -> np.array:
    vectorizer = CountVectorizer(ngram_range = (ng_min, ng_max))
    return vectorizer.fit_transform(X)

def RandomForestModel_RFE(_max_depth: int, X_train: pd.DataFrame, y_train: pd.DataFrame, modelName: str) -> None:
    
    # train
    print("Training...")
    clf = RandomForestClassifier(max_depth = _max_depth, random_state = 42)
    start = time.time()
    # clf.fit(X_train, y_train)
    # RFE
    rfe = RFE(clf, step=0.2)
    # RFCVE
    # rfe = RFECV(clf, step=0.2, cv=2, scoring="accuracy", n_jobs=-1, min_features_to_select=1)
    rfe.fit(X_train, y_train)
    print("n_features_", rfe.n_features_)
    stop = time.time()
    # save model
    joblib.dump(rfe, modelName)
    print(f"Training time: {stop - start} s")

def get_parser():
    parser = argparse.ArgumentParser(description = "N-gram RFE")
    parser.add_argument("-b", "--benign", type = str, help = "Enter source path for benign")
    parser.add_argument("-m", "--malware", type = str, help = "Enter source path for malware")
    parser.add_argument("-r", "--train_ratio", type = float, help = "Enter train ratio")
    parser.add_argument("-ng", "--n_gram", type = int, nargs='+', help = "Enter n_gram")
    return parser

if __name__ == "__main__":
    
    parser = get_parser()
    args = parser.parse_args()

    X, y = createCorpusDataset(args.benign, args.malware)

    # vectorize
    print("Vectorizing...")
    start = time.time()
    # X = TFIDFvec(X, args.n_gram[0], args.n_gram[1])
    X = Countvec(X, args.n_gram[0], args.n_gram[1])
    end = time.time()
    difference = end-start
    print("X shape:", X.shape)
    print("Vectorize time: ", difference)
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, train_size = args.train_ratio, random_state = 42)

    print("total_set shape :", X.shape)
    print("yLabel shape :", len(y))
    print()
    print("train_set shape :", X_train.shape)
    print("train_label shape :", len(y_train))
    print()
    print("test_set shape :", X_test.shape)
    print("test_label shape :", len(y_test))
    print()

    for depth in [2, 3, 5, 10, 15, 30, 50, 100, 1000]:
        print()
        print("【Depth】", depth)
        RandomForestModel_RFE(depth, X_train, y_train, "./model_ngram_rfe/ngram_rfe_RF_" + str(depth))
        model = joblib.load("./model_ngram_rfe/ngram_rfe_RF_" + str(depth))
        print("Accuracy:", model.score(X_test, y_test))
        print()

        # predict = model.predict(X_test)
        # tn, fp, fn, tp = confusion_matrix(y_test, predict).ravel()
        # print("實際 Malware, 預測 Malware:", tp)
        # print("實際 Benign, 預測 Benign:", tn)
        # print("實際 Malware, 預測 Benign:", fn)
        # print("實際 Benign, 預測 Malware:", fp)
    