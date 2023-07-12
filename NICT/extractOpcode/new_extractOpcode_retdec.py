import os, sys
import pickle
import argparse

def createTempFile(temp: str):
    if not os.path.exists(temp):
        try:
            os.system("mkdir " + temp)
            # print("[o] CreateTempFile Successfully")
        except:
            # print("[x] CreateTempFile Failed")
            sys.exit()

def analyzeDSM(file: str) -> list:
    f = open(file)
    lines = f.readlines()
    opcodeSequence = []
    for line in lines:
        opcode = line.split("\t")
        if(len(opcode) == 2):
            opcode = opcode[1].split(" ")[0]
            opcodeSequence.append(opcode)

    f.close()
    return opcodeSequence

def extractOpcode_retdec(srcPath: str, dstPath: str, fileName: str):
    
    # Check if pickle file already exists
    if os.path.isfile(os.path.join(dstPath, fileName) + ".pickle"):
        return

    # Create dsmTemp
    createTempFile("sh_dsmTemp")

    # copy target file to dsmTemp
    tgtFilePath = os.path.join(srcPath, fileName)
    os.system("cp " + tgtFilePath + " sh_dsmTemp/")
    
    os.system("retdec-decompiler sh_dsmTemp/" + fileName + " > /dev/null 2>&1")

    if os.path.isfile("sh_dsmTemp/" + fileName + ".dsm"):
        opcodeSequence = analyzeDSM("sh_dsmTemp/" + fileName + ".dsm")

        with open(os.path.join(dstPath, fileName) + ".pickle", "wb") as f:
            pickle.dump(opcodeSequence, f)

    try:
        os.system("rm sh_dsmTemp/" + fileName + "*")
    except:
        pass

def get_parser():
    parser = argparse.ArgumentParser(description = "Extract OpcodeSequence using Retdec")
    parser.add_argument("-i", "--input", type = str, help = "Enter source path")
    parser.add_argument("-o", "--output", type = str, help = "Enter destination path")
    parser.add_argument("-f", "--file", type = str, help = "Enter filename")
    return parser

if __name__ == "__main__":
    
    parser = get_parser()
    args = parser.parse_args()
    extractOpcode_retdec(args.input, args.output, args.file)

