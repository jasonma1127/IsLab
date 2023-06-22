from tqdm import tqdm
import os
import pandas as pd
import pickle

def readCSV(filepath: str):

    df = pd.read_csv(filepath)
    return df

def loadPickle(file_path: str) -> pickle:
    with open(file_path, "rb") as f:
        pk = pickle.load(f)
    return pk

def malwareDataset(filepath: str, datacsv):

    malware_list = []

    for file in tqdm(os.listdir(filepath)):
        filename = file.split(".")[0]
        opcode = loadPickle(os.path.join(filepath, file))
        if len(opcode) == 0:
            continue
        try:
            arch_fam = list(datacsv.query("sha256 == @filename")[["arch", "family"]].values[0])
            malware_list.append([1, filename] + arch_fam + [opcode])
        except:
            # malware_list.append([1, filename, "unknown", "unknown"] + [opcode])
            pass

    malware_pd = pd.DataFrame(malware_list)
    malware_pd.columns = ["label", "Filename", "arch", "family", "opcode"]
    # print(malware_pd)
    # print(malware_pd["arch"].value_counts())
    # print(malware_pd["family"].value_counts())
    return malware_pd

def benignDataset(filepath: str, datacsv):

    benign_list = []

    for file in tqdm(os.listdir(filepath)):
        filename = file.split(".")[0]
        opcode = loadPickle(os.path.join(filepath, file))
        if len(opcode) == 0:
            continue
        try:
            arch_fam = list(datacsv.query("filename == @filename")[["CPU Architecture", "label"]].values[0])
            benign_list.append([0, filename] + arch_fam + [opcode])
        except:
            # benign_list.append([0, filename, "unknown", "unknown"] + [opcode])
            pass

    benign_pd = pd.DataFrame(benign_list)
    benign_pd.columns = ["label", "Filename", "arch", "family", "opcode"]
    # print(benign_pd)
    # print(benign_pd["arch"].value_counts())
    # print(benign_pd["family"].value_counts())
    return benign_pd

def renameArch(datacsv):

    renameMap = {
        "mipseb": "MIPS",
        "mipsel": "MIPS",
        "mips64eb": "MIPS_64",
        "Intel 80386": "x86",
        "x86el": "x86",
        "x86_64el": "x86_64",
        "x86-64": "x86_64",
        "armel": "ARM",
        "armeb": "ARM",
        "ppceb": "PowerPC",
        "PowerPC or cisco 4500": "PowerPC"
    }

    rename_dataset = datacsv.replace({"arch":renameMap})
    return rename_dataset

if __name__ == "__main__":

    malCSV = readCSV("../DataSet/Toyset/OpcodeSequence_retdec/mal.csv")
    malware_pd = malwareDataset("../DataSet/Toyset/OpcodeSequence_retdec/malware_UFwR/", malCSV)

    benCSV = readCSV("../DataSet/Toyset/OpcodeSequence_retdec/dataset.csv")
    benign_pd = benignDataset("../DataSet/Toyset/OpcodeSequence_retdec/benign_UFwR/", benCSV)

    total = pd.concat([malware_pd, benign_pd])

    # print(total)
    # print(total["arch"].value_counts())
    # print(total["family"].value_counts())

    dataset = renameArch(total)
    print(dataset)
    print(dataset["arch"].value_counts())
    print(dataset["family"].value_counts())
    # saving the dataframe
    dataset.to_csv('CDMC2023.csv', index=False)