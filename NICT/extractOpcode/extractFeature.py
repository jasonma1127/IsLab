from extractOpcode_retdec import extractOpcode_retdec
from extractOpcode_radare2 import extractOpcode_radare2
import os, sys
import argparse
from tqdm import tqdm

def get_parser():
    parser = argparse.ArgumentParser(description = "Extract Features")
    parser.add_argument("-t", "--tool", type = str, help = "Select tool you want to use")
    parser.add_argument("-i", "--input", type = str, help = "Enter source path")
    parser.add_argument("-o", "--output", type = str, help = "Enter destination path")
    return parser
    
if __name__ == "__main__":

    parser = get_parser()
    args = parser.parse_args()

    if args.tool == "retdec":
        for file in tqdm(os.listdir(args.input), desc = "Extract Features using retdec"):
            extractOpcode_retdec(args.input, args.output, file)
    
    if args.tool == "radare2":
        for file in tqdm(os.listdir(args.input), desc = "Extract Features using radare2"):
            extractOpcode_radare2(args.input, args.output, file)