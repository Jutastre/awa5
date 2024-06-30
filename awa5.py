#!/usr/bin/env python3
import itertools

try:
    with open("program.txt") as file:
        raw_program_text = file.read()
except FileNotFoundError:
    print('"program.txt" not found! exiting...')
    quit()

try:
    with open("input") as file:
        raw_input = file.read()
except FileNotFoundError:
    raw_input = ""


def decode_awa_to_binary_awa(awa_string: str) -> list[int]:
    binary_awa = []
    skip = False
    for awa_bit, _ in itertools.batched(awa_string, 2):
        if skip:
            skip = False
            continue
        if awa_bit == " ":
            binary_awa.append(0)
            skip = True
        else:
            binary_awa.append(1)
    return binary_awa

def decode_binary_awa_to_awa_ir(binary:list[int]) -> list:
    ir = []
    while binary:
        op = int('0b' + ''.join([str(n) for n in binary[:5]]))      ##UNTESTED
        binary = binary[5:]
        match op:
            case 0x5:
                data = int('0b' + ''.join([str(n) for n in binary[:8]])) ##obviously also untested
                binary = binary[8:]
            case 0x6|0x9|0x10|0x11:
                data = int('0b' + ''.join([str(n) for n in binary[:5]])) ##obviously also untested
                binary = binary[5:]
            case _:
                data = None
        ir.append((op,data))

def read_program(raw_program_text: str):
    checksum = raw_program_text[:3]
    program_data_raw = raw_program_text[3:]
    assert checksum == "awa"
    assert len(program_data_raw) % 2 == 0
    binary_data = decode_awa_to_binary_awa(raw_program_text)
    program_data = decode_binary_awa_to_awa_ir(binary_data)
    return program_data

class AwaVM:
    def __init__(self) -> None:
        self.abyss = []
    
    def print()




    def execute_ir(awa_ir):
        for instruction,data in awa_ir
            match instruction:
                case 0x0:
                    continue
                case 0x01:
