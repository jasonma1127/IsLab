import pandas as pd
import os
import json
from tqdm import tqdm

def createLabel(dataPath: str, packerPath: str, storePath) -> pd.DataFrame:

    print("[+] Creating Label...")

    if os.path.exists(storePath):

        print("packer_label.json already exists >_<")

    else:

        with open(dataPath, "r", encoding = "utf-8") as f:

            data = json.load(f)

        with open(packerPath, "r", encoding = "utf-8") as f:

            packed = json.load(f)

        label = {}

        for d in tqdm(data, desc = "[+] Extracting label..."):
            if d in packed.keys():
                label.update({d: {"packed":1}})
            else:
                label.update({d: {"packed":0}})
            
        # store json
        with open(storePath, "w") as outfile:
            json.dump(label, outfile)

    # load packer label
    label = pd.read_json(storePath, orient = "index")

    return label.sort_index()

if __name__ == "__main__":
    
    label = createLabel("/data/Data.json", "/data/packed_version.json", "./packer_label.json")
    print(label)
    