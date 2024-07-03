#!/usr/bin/env python3
from __future__ import annotations
import sys
import re  # oops i did it again


# expects input to look like this:
# 5 0
# 5 1
# 5 0
# 5 1
# 5 0
# 9 5
# 1


def main(argv: list[str]):
    if not argv:
        print("Usage: python3 ir_to_awa.py input [output]")
        quit()

    output_binary = False
    for arg in argv[:-1]:
        match arg:
            case "-b" | "-bin" | "--binary":
                output_binary = True
    filename = argv[-1]
    try:
        with open(filename) as file:
            raw_ir = file.readlines()
    except FileNotFoundError:
        print(f'"{filename}" not found! exiting...')
        quit()

    string_pieces = []
    for line in raw_ir:
        split_line = [int(n) for n in line.split()]
        string_pieces.append(f"{split_line[0]:05b}")
        match split_line[0]:
            case 5:
                # piece = f"{int(split_line[1]):08b}"
                if split_line[1] >= 0:
                    string_pieces.append(f"{int(split_line[1]):08b}")
                else:
                    string_pieces.append(f"{int(pow(2,8) + split_line[1]):08b}")
            case 6 | 9 | 16 | 17:
                string_pieces.append(f"{int(split_line[1]):05b}")
    binary_string = "".join(string_pieces)

    if output_binary:
        awa_string = binary_string
    else:
        awa_string = f"awa{re.sub('1','wa', re.sub('0', ' awa', binary_string))}"

    # if len(argv) > 1:
    #     filename = argv[-1]
    # else:
    filename += ".🌠"
    try:
        with open(filename, "w") as file:
            file.write(awa_string)
            file.write("\n")
    except:
        print("Error writing file!")


if __name__ == "__main__":
    main(sys.argv[1:])
