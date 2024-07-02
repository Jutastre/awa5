#!/usr/bin/env python3
from __future__ import annotations
import sys
import re #oops i did it again



def main(argv: list[str]):
    if not argv:
        print("Usage: python3 ir_to_awa.py input [output]")

    filename = argv[0]
    try:
        with open(filename) as file:
            raw_ir = file.readlines()
    except FileNotFoundError:
        print(f'"{filename}" not found! exiting...')
        quit()

    string_pieces = []
    for line in raw_ir:
        split_line = [int(n)  for n in line.split()]
        string_pieces.append(f"{split_line[0]:05b}")
        match split_line[0]:
            case 5:
                string_pieces.append(f"{int(split_line[1]):08b}")
            case 6|9|16|17:
                string_pieces.append(f"{int(split_line[1]):05b}")
    binary_string = ''.join(string_pieces)
    awa_string = f"awa{re.sub('1','wa', re.sub('0', ' awa', binary_string))}"

    if len(argv) > 1:
        filename = argv[1]
    else:
        filename += ".🌠"
    try:
        with open(filename, 'w') as file:
            file.write(awa_string)
            file.write("\n")
    except:
        print("Error writing file!")

if __name__ == "__main__":
    main(sys.argv[1:])
