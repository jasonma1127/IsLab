from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer

from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.neural_network import MLPClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import Lasso
from sklearn.linear_model import Perceptron
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.pipeline import Pipeline
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import RepeatedStratifiedKFold
from numpy import mean
from numpy import std

from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
from sklearn.feature_selection import RFECV
from sklearn.feature_selection import RFE
import os
import argparse
from tqdm import tqdm
import pickle
import time
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

def Training_Model(model, X_train: pd.DataFrame, y_train: pd.DataFrame):
    
    # train
    print("Training...")
    start = time.time()
    model.fit(X_train, y_train)
    # print("n_features_", model.n_features_)
    stop = time.time()
    print(f"Training time: {stop - start} s")
    return model

def get_parser():
    parser = argparse.ArgumentParser(description = "N-gram RFE")
    parser.add_argument("-b", "--benign", type = str, help = "Enter source path for benign")
    parser.add_argument("-m", "--malware", type = str, help = "Enter source path for malware")
    # parser.add_argument("-mth", "--method", type = str, help = "Enter method")
    return parser


# get a list of models to evaluate
def get_models():
    models = dict()

    # rf
    rfe = RFE(estimator=RandomForestClassifier(max_depth = 1000, random_state = 42), step=0.01)
    model = RandomForestClassifier(max_depth = 1000, random_state = 42)
    models['RFE_rf'] = Pipeline(steps=[('s',rfe),('m',model)])
    models['rf'] = model
    
    # knn
    rfe = RFE(estimator=RandomForestClassifier(max_depth = 100, random_state = 42), step=0.01)
    model = KNeighborsClassifier(n_neighbors=3)
    models['RFE_knn'] = Pipeline(steps=[('s',rfe),('m',model)])
    models['knn'] = model
    
    # mlp
    rfe = RFE(estimator=RandomForestClassifier(max_depth = 100, random_state = 42), step=0.01)
    model = MLPClassifier(random_state=42, max_iter=5)
    models['RFE_mlp'] = Pipeline(steps=[('s',rfe),('m',model)])
    models['mlp'] = model

    # decision tree
    rfe = RFE(estimator=RandomForestClassifier(max_depth = 5, random_state = 42), step=0.01)
    model = DecisionTreeClassifier()
    models['RFE_dt'] = Pipeline(steps=[('s',rfe),('m',model)])
    models['dt'] = model

    # gbm
    rfe = RFE(estimator=GradientBoostingClassifier(n_estimators=5, learning_rate=1.0, max_depth=10, random_state=42), step=0.01)
    model = GradientBoostingClassifier(n_estimators=5, learning_rate=1.0, max_depth=10, random_state=42)
    models['RFE_gbm'] = Pipeline(steps=[('s',rfe),('m',model)])
    models['gbm'] = model

    return models
 
# evaluate a give model
def evaluate_model(model, X_train, X_test, y_train, y_test):

    model = Training_Model(model, X_train, y_train)
    
    ACC = model.score(X_test, y_test)
    predict = model.predict(X_test)
    
    tn, fp, fn, tp = confusion_matrix(y_test, predict).ravel()

    FPR = fp/(tn+fp)
    Precision = tp/(tp+fp)
    Recall = tp/(tp+fn)
    F1 = 2*(Precision*Recall)/(Precision+Recall)

    return ACC, Recall, Precision, FPR, F1

if __name__ == "__main__":
    
    parser = get_parser()
    args = parser.parse_args()

    X, y = createCorpusDataset(args.benign, args.malware)

    # vectorize
    print("Vectorizing...")
    start = time.time()
    # X = TFIDFvec(X, 1, 2)
    X = Countvec(X, 1, 2)
    end = time.time()
    difference = end-start
    print("X shape:", X.shape)
    print("Vectorize time: ", difference)
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, train_size = 0.8, random_state = 42)

    print("total_set shape :", X.shape)
    print("yLabel shape :", len(y))
    print()
    print("train_set shape :", X_train.shape)
    print("train_label shape :", len(y_train))
    print()
    print("test_set shape :", X_test.shape)
    print("test_label shape :", len(y_test))
    print()

    # get the models to evaluate
    models = get_models()

    for name, model in models.items():
        print("===", name, "===")
        ACC, Recall, Precision, FPR, F1 = evaluate_model(model, X_train, X_test, y_train, y_test)
        print()
        print("Accuracy", ACC)
        print("Recall:", Recall)
        print("Precision:", Precision)
        print("誤報率(FPR):", FPR)
        print("F1:", F1)
        print()
