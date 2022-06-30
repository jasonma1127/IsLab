import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from tqdm import tqdm
from sklearn import manifold, datasets
import os, sys
import csv
import random
import time
from networkx.drawing.nx_agraph import write_dot
from networkx.drawing.nx_agraph import read_dot
from os.path import exists
import gc

#### 常用 Func ####

def read_label():
    # read label file
    family_dict = {'BenignWare':0, 'Mirai':1, 'Tsunami':2, 'Hajime':3, 'Dofloo':4, 'Bashlite':5, 'Xorddos':6, 'Android':7, 'Pnscan':8, 'Unknown':9}
    arch_dict = {'armel':0, 'mipseb':1, 'x86el':2, 'mipsel':3, 'x86_64el':4, 'unknown':5, 'ppceb':6, 'sparceb':7, 'mips64eb':8, 'armeb':9, 'ppcel':10, 'm68keb':11}
    label = {}
    with open('../dataset.csv', newline='') as csvfile:
        rows = csv.reader(csvfile)
        next(rows)
        for row in rows:
            temp = [family_dict[row[1]], arch_dict[row[3]]]
            label[row[0]] = temp
    #print('---- finish read label ----\n')
    return label

def realse_list(a):
    del a[:]
    del a

def createOpcodeGraph(sequence):

    G = nx.MultiDiGraph()

    # add nodes
    G.add_nodes_from(sequence)

    # add edges
    for i in range(len(sequence) - 1):
        G.add_edge(sequence[i], sequence[i + 1])
    
    return G


def removeEdges(G):
    edges = G.edges()
    for edge in list(edges):
        if edge[0] != edge[1]:
            G.remove_edge(*edge)
    
    return G


def calculateNodeDegree(G):
    return dict(G.degree(G.nodes()))


def DataAmount(malAmount, benAmount, malSeq, benSeq):
    
    # 把檔案順序打亂
    random.shuffle(malSeq)
    random.shuffle(benSeq)
    
    # 要各自拿多少個
    malSeq = malSeq[:malAmount]
    benSeq = benSeq[:benAmount]
    
    np.save("./malSeq.npy", malSeq)
    np.save("./benSeq.npy", benSeq)
    
    return malSeq, benSeq


def findUniqueOpcode(pathDict, malSeq, benSeq):
    
    # 初始 uniqueOpcode
    uniqueOpcode = np.empty(0)
    
    # malware
    for filename in tqdm(malSeq, desc = "Malware"):
        file = np.load(pathDict["malware_OpcodeSequence"] + filename)
        
        # unique
        file = np.unique(file)
        
        # concatenate
        uniqueOpcode = np.concatenate((uniqueOpcode, file), axis=None)
        
        # unique
        uniqueOpcode = np.unique(uniqueOpcode)
        
    # benign
    for filename in tqdm(benSeq, desc = "Benign"):
        file = np.load(pathDict["benign_OpcodeSequence"] + filename)
        
        # unique
        file = np.unique(file)
        
        # concatenate
        uniqueOpcode = np.concatenate((uniqueOpcode, file), axis=None)
        
        # unique
        uniqueOpcode = np.unique(uniqueOpcode)
        
    # to Dict
    uniqueOpcode_DICT = {}
    zeros = np.zeros(len(uniqueOpcode), int)
    
    for A, B in zip(uniqueOpcode, zeros):
        uniqueOpcode_DICT[A] = B
    
    return uniqueOpcode_DICT


def prepareToTrain(uniqueOpcode, nodeDegree):
    
    for key in nodeDegree.keys():
        uniqueOpcode[key] = nodeDegree[key]
        
    return list(uniqueOpcode.values())


# ====== Main ======

#### Setting ####

pathDict = {
    "malware_OpcodeSequence" : "/media/islab/media_1/JasonMa/OpcodeSequence/OpcodeSequence/",
    "benign_OpcodeSequence" : "/media/islab/media_1/JasonMa/BenignWareOpcodeSequence/Benignware_OpcodeSequence/",
    "OpcodeGraphPath" : "/media/islab/media_1/JasonMa/OpcodeGraph/",
    "OPG_rmAllEdgesPath" : "/media/islab/media_1/JasonMa/OPG_rmAllEdges/"
}

benignAmount = 50000
malwareAmount = 50000

#### Dataset ####

print()
print(" ====== Dataset ====== ")
print()

# 所有 sample 對應到的家族與架構
label_dict = read_label()

Mirai_armel_OpcodeSequence = []
Benign_armel_OpcodeSequence = []

for file in tqdm(os.listdir(pathDict["malware_OpcodeSequence"])):
    
    filename = file.split(".")[0]
    family = label_dict[filename][0]
    arch = label_dict[filename][1]
    
    if arch == 0:
        Mirai_armel_OpcodeSequence.append(file)
        

for file in tqdm(os.listdir(pathDict["benign_OpcodeSequence"])):
    
    filename = file.split(".")[0]
    family = label_dict[filename][0]
    arch = label_dict[filename][1]
    
    if family == 0 and arch == 0:
        Benign_armel_OpcodeSequence.append(file)
        
print("Size of Mirai_armel_OpcodeSequence:", len(Mirai_armel_OpcodeSequence))

print("Size of Benign_armel_OpcodeSequence:", len(Benign_armel_OpcodeSequence))

#### Find Unique Opcode ####

print()
print(" ====== Find Unique Opcode ====== ")
print()

# 選擇 data 筆數
malSeq, benSeq = DataAmount(benignAmount, malwareAmount, Mirai_armel_OpcodeSequence, Benign_armel_OpcodeSequence)

# 用過的
# malSeq = np.load("./malSeq.npy")
# benSeq = np.load("./benSeq.npy")

UNIopcode = findUniqueOpcode(pathDict, malSeq, benSeq)

#### Extract Features for each Sample ####

totalsFeature = []

print()
print(" ====== Extract Features for each Sample ====== ")
print()

for filename in tqdm(malSeq, desc = "Malware Extraction"):
    
    Feature = []
    
    file = np.load(pathDict["malware_OpcodeSequence"] + filename)
    Feature.append(filename)
    
    # CreateOpcodeGraph
    start = time.time()
    opcodeGraph = createOpcodeGraph(file)
    stop = time.time()
    COG_time = stop - start
    Feature.append(COG_time)
    
    # RemoveEdges
    start = time.time()
    subgraph = removeEdges(opcodeGraph)
    stop = time.time()
    REs_time = stop - start
    Feature.append(REs_time)
    
    # CalculateNodeDegree
    start = time.time()
    nodeDegree = calculateNodeDegree(subgraph)
    stop = time.time()
    CND_time = stop - start
    Feature.append(CND_time)
    
    totalTime = COG_time + REs_time + CND_time
    Feature.append(totalTime)
    
    # PrepareToTrain
    histogram = prepareToTrain(UNIopcode, nodeDegree)
    Feature.append(np.array(histogram))
    
    # DeleteAll
    del file
    opcodeGraph.clear()
    subgraph.clear()
    del nodeDegree
    del histogram
    
    totalsFeature.append(Feature)
    
for filename in tqdm(benSeq, desc = "Benign Extraction"):
    
    Feature = []
    
    file = np.load(pathDict["benign_OpcodeSequence"] + filename)
    Feature.append(filename)
    
    # CreateOpcodeGraph
    start = time.time()
    opcodeGraph = createOpcodeGraph(file)
    stop = time.time()
    COG_time = stop - start
    Feature.append(COG_time)
    
    # RemoveEdges
    start = time.time()
    subgraph = removeEdges(opcodeGraph)
    stop = time.time()
    REs_time = stop - start
    Feature.append(REs_time)
    
    # CalculateNodeDegree
    start = time.time()
    nodeDegree = calculateNodeDegree(subgraph)
    stop = time.time()
    CND_time = stop - start
    Feature.append(CND_time)
    
    totalTime = COG_time + REs_time + CND_time
    Feature.append(totalTime)
    
    # PrepareToTrain
    histogram = prepareToTrain(UNIopcode, nodeDegree)
    Feature.append(np.array(histogram))
    
    # DeleteAll
    del file
    opcodeGraph.clear()
    subgraph.clear()
    del nodeDegree
    del histogram
    
    totalsFeature.append(Feature)
    
    

totalsFeatureDf = pd.DataFrame(totalsFeature)
totalsFeatureDf.columns = ["filename", "COG time", "REs time", "CND time", "total time", "feature"]

print()
print(" ====== totalsFeatureDf Info ====== ")
print()
print("totalsFeatureDf shape :", totalsFeatureDf.shape)
print("feature shape :", len(totalsFeatureDf["feature"].iloc[0]))
print(totalsFeatureDf)

totalsFeatureDf.to_csv("totalsFeatureDf_withREs.csv", index = False)


