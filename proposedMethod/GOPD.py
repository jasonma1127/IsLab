import os, sys
import pickle
from tqdm import tqdm
import numpy as np
import argparse
from sklearn.model_selection import train_test_split
import joblib

def loadPickle(file_path: str) -> pickle:
    with open(file_path, "rb") as f:
        pk = pickle.load(f)
    return pk

def savePickle(file_path: str, opcodeSequence) -> None:
    with open(file_path, "wb") as f:
        pickle.dump(opcodeSequence, f)

def find_indices(list_to_check, item_to_find) -> list:
    indices = []
    for idx, value in enumerate(list_to_check):
        if value == item_to_find:
            indices.append(idx)
    return indices

def find_garbage_opcode_index(sample: pickle, oriset: set) -> list:
    
    garbage_opcode_index = []

    for index in range(len(sample)):
        if sample[index] not in oriset:
            garbage_opcode_index.append(index)
    
    return garbage_opcode_index

def remove_garbage_n_neighbor(n: int, sample: pickle, garbage_opcode_index: list) -> list:
    
    garbage_remove_index = []
    
    for i in garbage_opcode_index:
        low = i - n
        high = i + n
        for remove_i in range(low, high+1):
            garbage_remove_index.append(remove_i)

    garbage_remove_index = set(garbage_remove_index)

    garbage_remove_index = list(filter(lambda x:x>=0 and x<len(sample), garbage_remove_index))

    sample_garbage_removed = np.delete(np.array(sample),(garbage_remove_index)).tolist()

    return sample_garbage_removed

def transform_to_feature(sample_packed_op: pickle):
    X = []
    for op_index in range(len(sample_packed_op)):
        X.append(features(sample_packed_op, op_index))
    return X

def features(sentence, index):
    """ sentence: [w1, w2, ...], index: the index of the word """
    return {
        'word': sentence[index],
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

def get_parser():
    parser = argparse.ArgumentParser(description = "【Garbage Opcode Detector】- Removal")
    parser.add_argument("-n", "--neighbor", type = str, help = "Enter neighbor amount")
    parser.add_argument("-m", "--model", type = str, help = "Enter model")
    return parser

if __name__ == "__main__":

    parser = get_parser()
    args = parser.parse_args()

    # All
    # benign_packed = "../NICT/DataSet/Toyset/OpcodeSequence_retdec/benign_UFwR/"
    # malware_packed = "../NICT/DataSet/Toyset/OpcodeSequence_retdec/malware_UFwR/"
    # benign_garbage_removed = "../NICT/DataSet/Toyset/OpcodeSequence_retdec/benign_garbage_removed/"
    # malware_garbage_removed = "../NICT/DataSet/Toyset/OpcodeSequence_retdec/malware_garbage_removed/"
    # benign_garbage_removed = "../NICT/DataSet/Toyset/OpcodeSequence_retdec/benign_GOPD/"
    # malware_garbage_removed = "../NICT/DataSet/Toyset/OpcodeSequence_retdec/malware_GOPD/"


    # # real_opcode rate > 50
    # benign_packed = "../NICT/DataSet/Toyset/OpcodeSequence_retdec/benign_pos/"
    # malware_packed = "../NICT/DataSet/Toyset/OpcodeSequence_retdec/malware_pos/"
    # benign_garbage_removed = "../NICT/DataSet/Toyset/OpcodeSequence_retdec/benign_GOPD/"
    # malware_garbage_removed = "../NICT/DataSet/Toyset/OpcodeSequence_retdec/malware_GOPD/"

    # 100 sample
    benign_packed = "../NICT/DataSet/Toyset/OpcodeSequence_retdec/benign_50/"
    malware_packed = "../NICT/DataSet/Toyset/OpcodeSequence_retdec/malware_50/"
    benign_garbage_removed = "../NICT/DataSet/Toyset/OpcodeSequence_retdec/benign_GOPD/"
    malware_garbage_removed = "../NICT/DataSet/Toyset/OpcodeSequence_retdec/malware_GOPD/"

    # load model
    # loaded_model = joblib.load("./model/nlp_pos_model.joblib")
    # loaded_model = joblib.load("./model/nlp_pos_all_model.joblib")
    loaded_model = joblib.load("./model/" + args.model + ".joblib")

    # load cheat dict
    # GOP_dict = loadPickle("./GOP_dict.pickle")

    for sample in tqdm(os.listdir(benign_packed), desc = "Benign"):
        
        sample_packed_op = loadPickle(os.path.join(benign_packed, sample))
        sample_feature = transform_to_feature(sample_packed_op)

        try:
            sample_predict = loaded_model.predict(sample_feature)
            garbage_opcode_index = find_indices(sample_predict, 1)
            sample_garbage_removed = remove_garbage_n_neighbor(int(args.neighbor), sample_packed_op, garbage_opcode_index)
            savePickle(os.path.join(benign_garbage_removed, sample), sample_garbage_removed)
        except:
            savePickle(os.path.join(benign_garbage_removed, sample), sample_packed_op)

        # # Cheat
        # sample_packed_op = loadPickle(os.path.join(benign_packed, sample))
        # gop_index = []
        # for index, op in enumerate(sample_packed_op):
        #     if op in GOP_dict:
        #         gop_index.append(index)
        # sample_garbage_removed = remove_garbage_n_neighbor(int(args.neighbor), sample_packed_op, gop_index)
        # savePickle(os.path.join(benign_garbage_removed, sample), sample_garbage_removed)

    for sample in tqdm(os.listdir(malware_packed), desc = "Malware"):
        
        sample_packed_op = loadPickle(os.path.join(malware_packed, sample))
        sample_feature = transform_to_feature(sample_packed_op)

        try:
            sample_predict = loaded_model.predict(sample_feature)
            garbage_opcode_index = find_indices(sample_predict, 1)
            sample_garbage_removed = remove_garbage_n_neighbor(int(args.neighbor), sample_packed_op, garbage_opcode_index)
            savePickle(os.path.join(malware_garbage_removed, sample), sample_garbage_removed)
        except:
            savePickle(os.path.join(malware_garbage_removed, sample), sample_packed_op)

        # # Cheat
        # sample_packed_op = loadPickle(os.path.join(malware_packed, sample))
        # gop_index = []
        # for index, op in enumerate(sample_packed_op):
        #     if op in GOP_dict:
        #         gop_index.append(index)
        # sample_garbage_removed = remove_garbage_n_neighbor(int(args.neighbor), sample_packed_op, gop_index)
        # savePickle(os.path.join(malware_garbage_removed, sample), sample_garbage_removed)