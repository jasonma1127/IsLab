import os, sys
import pickle
from tqdm import tqdm
import numpy as np
import argparse
from sklearn.model_selection import train_test_split

def loadPickle(file_path: str) -> pickle:
    with open(file_path, "rb") as f:
        pk = pickle.load(f)
    return pk

def split_target_test_set(ratio: float, benign_packed: str, malware_packed: str):

    benign_set = []
    malware_set = []
    total_set = []
    test_set = []
    train_set = []

    for filename in tqdm(os.listdir(benign_packed)):
        benign_set.append(filename)

    for filename in tqdm(os.listdir(malware_packed)):
        malware_set.append(filename)
    
    total_set = benign_set + malware_set

    benign_label = np.zeros(len(benign_set))
    malware_label = np.ones(len(malware_set))
 
    yLabel = np.append(benign_label, malware_label)

    train_set, test_set, train_label, test_label = train_test_split(total_set, yLabel, test_size = float(ratio), random_state = 42)

    print("total_set shape :", len(total_set))
    print("yLabel shape :", len(yLabel))
    print()
    print("train_set shape :", len(train_set))
    print("train_label shape :", len(train_label))
    print()
    print("test_set shape :", len(test_set))
    print("test_label shape :", len(test_label))
    print()

    return train_set, test_set, train_label, test_label

def features(sentence, index):
    """ sentence: [w1, w2, ...], index: the index of the word """
    return {
        # 'word': sentence[index],
        'length': len(sentence[index]),
        # 'is_first': index == 0,
        # 'is_last': index == len(sentence) - 1,
        # 'is_capitalized': sentence[index][0].upper() == sentence[index][0],
        # 'is_all_caps': sentence[index].upper() == sentence[index],
        # 'is_all_lower': sentence[index].lower() == sentence[index],
        # 'prefix-1': sentence[index][0],
        # 'prefix-2': sentence[index][:2],
        # 'prefix-3': sentence[index][:3],
        # 'suffix-1': sentence[index][-1],
        # 'suffix-2': sentence[index][-2:],
        # 'suffix-3': sentence[index][-3:],
        # 'prev_word': '' if index == 0 else sentence[index - 1],
        # 'next_word': '' if index == len(sentence) - 1 else sentence[index + 1],
        # 'has_hyphen': '.' in sentence[index],
        # 'is_numeric': sentence[index].isdigit(),
        # 'capitals_inside': sentence[index][1:].lower() != sentence[index][1:]
    }

def label_opcode(sample: pickle, oriset: set) -> list:

    opcode_label = []

    for opcode in sample:
        if opcode in oriset:
            # real opcode is 0
            opcode_label.append(0)
        else:
            # garbage opcode is 1
            opcode_label.append(1)
    
    return opcode_label

def transform_to_dataset(sample_list: list, label_list: list, benign_packed: str, malware_packed: str, benign_orig: str, malware_orig: str):
    X, y = [], []

    for i in tqdm(range(len(label_list)), desc = "Transforming Data"):
        # benign
        if label_list[i] == 0:
            sample_packed_op = loadPickle(os.path.join(benign_packed, sample_list[i]))
            sample_orig_op = loadPickle(os.path.join(benign_orig, sample_list[i]))

            ori_opcode_set = set(sample_orig_op)

            for op_index in range(len(sample_packed_op)):
                X.append(features(sample_packed_op, op_index))
                
            y += label_opcode(sample_packed_op, ori_opcode_set)
        
        # malware
        elif label_list[i] == 1:
            sample_packed_op = loadPickle(os.path.join(malware_packed, sample_list[i]))
            sample_orig_op = loadPickle(os.path.join(malware_orig, sample_list[i]))

            ori_opcode_set = set(sample_orig_op)

            for op_index in range(len(sample_packed_op)):
                X.append(features(sample_packed_op, op_index))

            y += label_opcode(sample_packed_op, ori_opcode_set)
 
    return X, y

def get_parser():
    parser = argparse.ArgumentParser(description = "Garbage Opcode Removal")
    parser.add_argument("-r", "--reference_ratio", type = str, help = "Enter reference ratio")
    parser.add_argument("-n", "--neighbor", type = str, help = "Enter neighbor amount")
    return parser

if __name__ == "__main__":

    parser = get_parser()
    args = parser.parse_args()

    benign_packed = "../NICT/DataSet/Toyset/OpcodeSequence_retdec/benign_UFwR/"
    malware_packed = "../NICT/DataSet/Toyset/OpcodeSequence_retdec/malware_UFwR/"
    benign_orig = "../NICT/DataSet/Toyset/OpcodeSequence_retdec/toy_benign_unpacked/"
    malware_orig = "../NICT/DataSet/Toyset/OpcodeSequence_retdec/toy_malware_unpacked/"

    train_set, test_set, train_label, test_label = split_target_test_set(args.reference_ratio, benign_packed, malware_packed)

    X, y = transform_to_dataset(train_set[2010:2025], train_label[2010:2025], benign_packed, malware_packed, benign_orig, malware_orig)

    print("y")
    print(len(y))
    print("garbage opcode:", sum(y))
    print("real opcode:", len(y) - sum(y))
    print("real opcode rate:", (len(y) - sum(y))/len(y))
    print()

    # y_range_low = 116528
    # y_range_high = 299376
    # print("y[:]")
    # print(len(y[y_range_low:y_range_high]))
    # print("real opcode:", sum(y[y_range_low:y_range_high]))
    # print("garbage opcode:", len(y[y_range_low:y_range_high]) - sum(y[y_range_low:y_range_high]))
    # print()

    from sklearn.tree import DecisionTreeClassifier
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.feature_extraction import DictVectorizer
    from sklearn.pipeline import Pipeline
    
    clf = Pipeline([
        ('vectorizer', DictVectorizer(sparse=False)),
        # ('classifier', DecisionTreeClassifier(criterion='entropy'))
        ('classifier', RandomForestClassifier(max_depth = 1000, random_state = 0))
    ])

    print("Training...")

    clf.fit(X, y)

    print("Training completed")

    X.clear()
    y.clear()
    del X
    del y
 
    X_test, y_test = transform_to_dataset(test_set[700:705], test_label[700:705], benign_packed, malware_packed, benign_orig, malware_orig)
    
    print("y_test")
    print(len(y_test))
    print("garbage opcode:", sum(y_test))
    print("real opcode:", len(y_test) - sum(y_test))
    print("real opcode rate:", (len(y_test) - sum(y_test))/len(y_test))
    print()

    # y_test_range_low = 506528
    # y_test_range_high = 719376
    # print("y_test[:]")
    # print(len(y_test[y_test_range_low:y_test_range_high]))
    # print("real opcode:", sum(y_test[y_test_range_low:y_test_range_high]))
    # print("garbage opcode:", len(y_test[y_test_range_low:y_test_range_high]) - sum(y_test[y_test_range_low:y_test_range_high]))
    # print()

    print("Accuracy:", clf.score(X_test, y_test))

    predict = clf.predict(X_test)

    from sklearn.metrics import confusion_matrix
    tn, fp, fn, tp = confusion_matrix(y_test, predict).ravel()
    print("實際 GP, 預測 GP:", tp)
    print("實際 RP, 預測 RP:", tn)
    print("實際 GP, 預測 RP:", fn)
    print("實際 RP, 預測 GP:", fp)