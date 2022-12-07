import os, sys
import pickle
import r2pipe
import json

def analyzeDSM(dsm: str):

    dsmList = dsm.split("\n")
    opcodeSequence = []
    for d in dsmList:
        opcode = d.split()
        if(len(opcode) > 2):
            opcode = opcode[2]
            opcodeSequence.append(opcode)

    return opcodeSequence

def extractOpcode_radare2(srcPath: str, dstPath: str, fileName: str):
    
    # Check if pickle file already exists
    if os.path.isfile(os.path.join(dstPath, fileName) + ".pickle"):
        return

    # analyze sample
    targetPath = os.path.join(srcPath, fileName)
    r = r2pipe.open("/bin/ls", flags=['-2'])
    r.cmd("aaaa")
    dsm = r.cmd("pda")

    # extract opcode
    opcodeSequence = analyzeDSM(dsm)

    with open(os.path.join(dstPath, fileName) + ".pickle", "wb") as f:
        pickle.dump(opcodeSequence, f)

