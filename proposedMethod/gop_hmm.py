import os, sys
import pickle
from tqdm import tqdm
import numpy as np
import argparse
import pandas as pd
import time
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

def label_opcode(sample: pickle, oriset: set) -> list:

    opcode_tagged = []

    for opcode in sample:
        if opcode in oriset:
            # real opcode is 0
            opcode_tagged.append((opcode, 0))
        else:
            # garbage opcode is 1
            opcode_tagged.append((opcode, 1))
    
    return opcode_tagged
    
def transform_to_dataset(sample_list: list, label_list: list, benign_packed: str, malware_packed: str, benign_orig: str, malware_orig: str):
    tagged_opcode = []

    for i in tqdm(range(len(label_list)), desc = "Transforming Data"):
        # benign
        if label_list[i] == 0:
            sample_packed_op = loadPickle(os.path.join(benign_packed, sample_list[i]))
            sample_orig_op = loadPickle(os.path.join(benign_orig, sample_list[i]))

            ori_opcode_set = set(sample_orig_op)

            tagged_opcode += label_opcode(sample_packed_op, ori_opcode_set)
        
        # malware
        elif label_list[i] == 1:
            sample_packed_op = loadPickle(os.path.join(malware_packed, sample_list[i]))
            sample_orig_op = loadPickle(os.path.join(malware_orig, sample_list[i]))

            ori_opcode_set = set(sample_orig_op)

            tagged_opcode += label_opcode(sample_packed_op, ori_opcode_set)
 
    return tagged_opcode

def t2_given_t1(t2, t1, train_bag):
    tags = [pair[1] for pair in train_bag]
    count_t1 = len([t for t in tags if t==t1])
    count_t2_t1 = 0
    for index in tqdm(range(len(tags)-1)):
        if tags[index]==t1 and tags[index+1] == t2:
            count_t2_t1 += 1
    return (count_t2_t1, count_t1)

def word_given_tag(word, tag, train_bag):
    tag_list = [pair for pair in train_bag if pair[1]==tag]
    count_tag = len(tag_list)#total number of times the passed tag occurred in train_bag
    w_given_tag_list = [pair[0] for pair in tag_list if pair[0]==word]
    #now calculate the total number of times the passed word occurred as the passed tag.
    count_w_given_tag = len(w_given_tag_list)

    return (count_w_given_tag, count_tag)

def Viterbi(words, train_bag):
    state = []
    T = list(set([pair[1] for pair in train_bag]))
     
    for key, word in enumerate(words):
        #initialise list of probability column for a given observation
        p = [] 
        for tag in T:
            if key == 0:
                transition_p = tags_df.loc[0, tag]
            else:
                transition_p = tags_df.loc[state[-1], tag]
                 
            # compute emission and state probabilities
            emission_p = word_given_tag(words[key], tag, train_bag)[0]/word_given_tag(words[key], tag, train_bag)[1]
            state_probability = emission_p * transition_p
            p.append(state_probability)
 
        pmax = max(p)
        # getting state for which probability is maximum
        state_max = T[p.index(pmax)] 
        state.append(state_max)
    return list(zip(words, state))

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

    train_tagged_opcode = transform_to_dataset(train_set, train_label, benign_packed, malware_packed, benign_orig, malware_orig)
    test_tagged_opcode = transform_to_dataset(test_set, test_label, benign_packed, malware_packed, benign_orig, malware_orig)

    train_tagged_opcode = train_tagged_opcode
    test_tagged_opcode = test_tagged_opcode

    print("train_tagged_opcode len", len(train_tagged_opcode))
    print("test_tagged_opcode len", len(test_tagged_opcode))
    print(train_tagged_opcode[:10])

    tags = {tag for opcode,tag in train_tagged_opcode}
    print(len(tags))
    print(tags)

    tags_matrix = np.zeros((len(tags), len(tags)), dtype='float32')
    for i, t1 in enumerate(list(tags)):
        for j, t2 in enumerate(list(tags)): 
            tags_matrix[i, j] = t2_given_t1(t2, t1, train_tagged_opcode)[0]/t2_given_t1(t2, t1, train_tagged_opcode)[1]
    
    print(tags_matrix)

    global tags_df
    tags_df = pd.DataFrame(tags_matrix, columns = list(tags), index=list(tags))
    print(tags_df)

    # Test
    test_untagged_opcode = [tup[0] for tup in test_tagged_opcode]
    
    start = time.time()
    tagged_seq = Viterbi(test_untagged_opcode, train_tagged_opcode)
    end = time.time()
    difference = end-start
    
    print("Time taken in seconds: ", difference)
    
    # accuracy
    check = [i for i, j in zip(tagged_seq, test_tagged_opcode) if i == j]
    
    accuracy = len(check)/len(tagged_seq)
    print('Viterbi Algorithm Accuracy: ',accuracy*100)

    predict = [tup[1] for tup in tagged_seq]
    test = [tup[1] for tup in test_tagged_opcode]

    from sklearn.metrics import confusion_matrix
    tn, fp, fn, tp = confusion_matrix(test, predict).ravel()
    print("實際 GP, 預測 GP:", tp)
    print("實際 RP, 預測 RP:", tn)
    print("實際 GP, 預測 RP:", fn)
    print("實際 RP, 預測 GP:", fp)