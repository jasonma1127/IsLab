# Extract Opcode

- extractFeature.py
- extractOpcode_retdec.py
- extractOpcode_radare2.py

# How to Use?

## Set Up Retdec

Create a symbolic link for retdec-decompiler in bin.

`ln -s <path/to/retdec-decompiler> /usr/bin/retdec-decompiler`

## Operation

`python3 extractFeature.py -h`

![extractFeature_help](./image/extractFeature_help.jpg)

### Extract Opcode sequence using Retdec

`python3 extractFeature.py -t retdec -i <path/to/source> -o <path/to/destination>`

### Extract Opcode sequence using Radare2

`python3 extractFeature.py -t radare2 -i <path/to/source> -o <path/to/destination>`