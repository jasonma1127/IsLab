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

def savePickle(file_path: str, opcodeSequence) -> None:
    with open(file_path, "wb") as f:
        pickle.dump(opcodeSequence, f)

def split_target_reference_set(ratio: float, benign_packed: str, malware_packed: str):

    benign_set = []
    malware_set = []
    total_set = []
    reference_set = []
    target_set = []

    for filename in tqdm(os.listdir(benign_packed)):
        benign_set.append(filename)

    for filename in tqdm(os.listdir(malware_packed)):
        malware_set.append(filename)
    
    total_set = benign_set + malware_set

    benign_label = np.zeros(len(benign_set))
    malware_label = np.ones(len(malware_set))
 
    yLabel = np.append(benign_label, malware_label)

    target_set, reference_set, target_label, reference_label = train_test_split(total_set, yLabel, test_size = float(ratio), random_state = 42)

    print("total_set shape :", len(total_set))
    print("yLabel shape :", len(yLabel))
    print()
    print("target_set shape :", len(target_set))
    print("target_label shape :", len(target_label))
    print()
    print("reference_set shape :", len(reference_set))
    print("reference_label shape :", len(reference_label))
    print()

    return target_set, reference_set, target_label, reference_label

def find_garbage_opcode(sample: pickle, oriset: set) -> list:
    
    garbage_opcode = []

    for opcode in sample:
        if opcode not in oriset:
            garbage_opcode.append(opcode)
    
    return garbage_opcode

def create_garbage_opcode_dict(reference_set, reference_label, benign_packed, malware_packed, benign_orig, malware_orig) -> set:

    garbage_opcode_dict = []

    for i in tqdm(range(len(reference_label)), desc = "Create Garbage Opcode Dict"):
        # benign
        if reference_label[i] == 0:
            sample_packed_op = loadPickle(os.path.join(benign_packed, reference_set[i]))
            sample_orig_op = loadPickle(os.path.join(benign_orig, reference_set[i]))

            ori_opcode_set = set(sample_orig_op)

            garbage_opcode_dict += find_garbage_opcode(sample_packed_op, ori_opcode_set)
        
        # malware
        elif reference_label[i] == 1:
            sample_packed_op = loadPickle(os.path.join(malware_packed, reference_set[i]))
            sample_orig_op = loadPickle(os.path.join(malware_orig, reference_set[i]))

            ori_opcode_set = set(sample_orig_op)

            garbage_opcode_dict += find_garbage_opcode(sample_packed_op, ori_opcode_set)

    return set(garbage_opcode_dict)

def find_garbage_opcode_index(sample: pickle, garbage_opcode_set: set) -> list:
    
    garbage_opcode_index = []

    for index in range(len(sample)):
        if sample[index] in garbage_opcode_set:
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
    benign_dictionary = "../NICT/DataSet/Toyset/OpcodeSequence_retdec/benign_dictionary/"
    malware_dictionary = "../NICT/DataSet/Toyset/OpcodeSequence_retdec/malware_dictionary/"

    target_set, reference_set, target_label, reference_label = split_target_reference_set(args.reference_ratio, benign_packed, malware_packed)

    garbage_opcode_dict = create_garbage_opcode_dict(reference_set, reference_label, benign_packed, malware_packed, benign_orig, malware_orig)

    print("garbage_opcode_dict size :", len(garbage_opcode_dict))
    print()

    for i in tqdm(range(len(target_label)), desc = "Garbage Opcode Removal"):
        # benign
        if target_label[i] == 0:
            sample_packed_op = loadPickle(os.path.join(benign_packed, target_set[i]))

            garbage_opcode_index = find_garbage_opcode_index(sample_packed_op, garbage_opcode_dict)

            sample_garbage_removed = remove_garbage_n_neighbor(int(args.neighbor), sample_packed_op, garbage_opcode_index)
        
            savePickle(os.path.join(benign_dictionary, target_set[i]), sample_garbage_removed)
        
        # malware
        if target_label[i] == 1:
            sample_packed_op = loadPickle(os.path.join(malware_packed, target_set[i]))

            garbage_opcode_index = find_garbage_opcode_index(sample_packed_op, garbage_opcode_dict)

            sample_garbage_removed = remove_garbage_n_neighbor(int(args.neighbor), sample_packed_op, garbage_opcode_index)
        
            savePickle(os.path.join(malware_dictionary, target_set[i]), sample_garbage_removed)

