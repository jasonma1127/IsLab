from extractOpcode import extractOpcode
import os, sys
import argparse
from tqdm import tqdm

def get_parser():
    parser = argparse.ArgumentParser(description = "Extract Features")
    parser.add_argument("-i", "--input", type = str, help = "Enter source path")
    parser.add_argument("-o", "--output", type = str, help = "Enter destination path")
    return parser
    
if __name__ == "__main__":

    parser = get_parser()
    args = parser.parse_args()

    for file in tqdm(os.listdir(args.input), desc = "Extract Features"):
        extractOpcode(args.input, args.output, file)