import os, sys
import pickle
from tqdm import tqdm
import numpy as np
import argparse

def loadPickle(file_path: str) -> pickle:
    with open(file_path, "rb") as f:
        pk = pickle.load(f)
    return pk

def savePickle(file_path: str, opcodeSequence) -> None:
    with open(file_path, "wb") as f:
        pickle.dump(opcodeSequence, f)

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

def get_parser():
    parser = argparse.ArgumentParser(description = "Garbage Opcode Removal")
    parser.add_argument("-n", "--neighbor", type = str, help = "Enter neighbor amount")
    return parser

if __name__ == "__main__":

    parser = get_parser()
    args = parser.parse_args()

    benign_packed = "../NICT/DataSet/Toyset/OpcodeSequence_retdec/benign_UFwR/"
    malware_packed = "../NICT/DataSet/Toyset/OpcodeSequence_retdec/malware_UFwR/"
    benign_orig = "../NICT/DataSet/Toyset/OpcodeSequence_retdec/toy_benign_unpacked/"
    malware_orig = "../NICT/DataSet/Toyset/OpcodeSequence_retdec/toy_malware_unpacked/"
    benign_garbage_removed = "../NICT/DataSet/Toyset/OpcodeSequence_retdec/benign_garbage_removed/"
    malware_garbage_removed = "../NICT/DataSet/Toyset/OpcodeSequence_retdec/malware_garbage_removed/"

    for sample in tqdm(os.listdir(benign_packed), desc = "Benign"):
        
        sample_packed_op = loadPickle(os.path.join(benign_packed, sample))
        sample_orig_op = loadPickle(os.path.join(benign_orig, sample))

        ori_opcode_set = set(sample_orig_op)

        garbage_opcode_index = find_garbage_opcode_index(sample_packed_op, ori_opcode_set)

        sample_garbage_removed = remove_garbage_n_neighbor(int(args.neighbor), sample_packed_op, garbage_opcode_index)
        
        savePickle(os.path.join(benign_garbage_removed, sample), sample_garbage_removed)


    for sample in tqdm(os.listdir(malware_packed), desc = "Malware"):
        
        sample_packed_op = loadPickle(os.path.join(malware_packed, sample))
        sample_orig_op = loadPickle(os.path.join(malware_orig, sample))

        ori_opcode_set = set(sample_orig_op)

        garbage_opcode_index = find_garbage_opcode_index(sample_packed_op, ori_opcode_set)

        sample_garbage_removed = remove_garbage_n_neighbor(int(args.neighbor), sample_packed_op, garbage_opcode_index)
        
        savePickle(os.path.join(malware_garbage_removed, sample), sample_garbage_removed)