import os, sys
import pickle

def createTempFile(temp: str):
    if not os.path.exists(temp):
        try:
            os.system("sudo mkdir " + temp)
            print("[o] CreateTempFile Successfully")
        except:
            print("[x] CreateTempFile Failed")
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

def extractOpcode(srcPath: str, dstPath: str, fileName: str):

    # Create dsmTemp
    createTempFile("dsmTemp")

    # copy target file to dsmTemp
    tgtFilePath = os.path.join(srcPath, fileName)
    os.system("sudo cp " + tgtFilePath + " dsmTemp/temp")
    
    # decompiler target file
    os.system("sudo retdec-decompiler dsmTemp/temp > /dev/null 2>&1")

    opcodeSequence = analyzeDSM("dsmTemp/temp.dsm")

    with open(os.path.join(dstPath, fileName) + ".pickle", "wb") as f:
        pickle.dump(opcodeSequence, f)
    
