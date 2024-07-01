#!/usr/bin/env python3
from __future__ import annotations
import sys
import itertools
import copy

DEBUG = True

AwaSCII_LOOKUP = "AWawJELYHOSIUMjelyhosiumPCNTpcntBDFGRbdfgr0123456789 .,!'()~_/;\n"


def AwaSCII_to_string(number) -> str:
    return AwaSCII_LOOKUP[number]


def char_to_AwaSCII(char: str) -> int:
    return AwaSCII_LOOKUP.find(char)


def string_to_AwaSCII(string: str) -> list[int]:
    return [char_to_AwaSCII(char) for char in string]


def binary_string_to_int(string: str) -> int:
    total = 0
    for char in string:
        total *= 2
        if char == "1":
            total += 1
    return total


class Bubble:
    def __init__(self, data: int | list | Bubble) -> None:
        if isinstance(data, Bubble):
            self.data: int | list | Bubble = data.data
        else:
            self.data: int | list | Bubble = data

    def __add__(self, other: Bubble):
        if not self.is_double() and not other.is_double():
            return Bubble(self.data + other.data)
        elif self.is_double() != other.is_double():
            if other.is_double():
                self, other = other, self
            simple = other.data
            self.data = [d1 + simple for d1 in self.data]
        else:
            self.data = [
                d1 + d2
                for d1, d2 in itertools.zip_longest(self.data, other.data, fillvalue=0)
            ]
        return self

    def __sub__(self, other: Bubble):
        if not self.is_double() and not other.is_double():
            return Bubble(self.data - other.data)
        elif self.is_double() != other.is_double():
            if other.is_double():
                self, other = other, self
            simple = other.data
            self.data = [d1 - simple for d1 in self.data]
        else:
            self.data = [
                d1 - d2
                for d1, d2 in itertools.zip_longest(self.data, other.data, fillvalue=0)
            ]
        return self

    def __mul__(self, other: Bubble):
        if not self.is_double() and not other.is_double():
            return Bubble(self.data * other.data)
        elif self.is_double() != other.is_double():
            if other.is_double():
                self, other = other, self
            simple = other.data
            self.data = [d1 * simple for d1 in self.data]
        else:
            self.data = [
                d1 * d2
                for d1, d2 in itertools.zip_longest(self.data, other.data, fillvalue=1)
            ]
        return self

    def __floordiv__(self, other: Bubble):
        if not self.is_double() and not other.is_double():
            return Bubble(self.data // other.data)
        elif self.is_double() != other.is_double():
            if other.is_double():
                self, other = other, self
            simple = other.data
            self.data = [d1 // simple for d1 in self.data]
        else:
            self.data = [
                d1 // d2
                for d1, d2 in itertools.zip_longest(self.data, other.data, fillvalue=1)
            ]
        return self

    def __sizeof__(self) -> int:
        if self.is_double():
            return 0
        else:
            return len(self.data)

    def is_double(self):
        return isinstance(self.data, list)

    # def print(self):
    #     string = ""

    def __str__(self) -> str:
        if self.is_double():
            return "".join([str(sub) for sub in self.data])
        else:
            return AwaSCII_to_string(self.data)

    def string_as_number(self) -> str:
        if self.is_double():
            return " ".join([sub.string_as_number() for sub in self.data])
        else:
            return str(self.data) #this might be wrong but doc is hard to interpret

    def add(self, other: Bubble):
        if not self.is_double() and not other.is_double():
            return Bubble(self.data + other.data)
        elif self.is_double() != other.is_double():
            if other.is_double():
                self, other = other, self
            simple = other.data
            self.data = [d1 + simple for d1 in self.data]
        else:
            self.data = [
                d1 + d2
                for d1, d2 in itertools.zip_longest(self.data, other.data, fillvalue=0)
            ]
        return self

    def mrg(self, other: Bubble):
        if self.is_double() == other.is_double():  # why am i doing this
            self.data = self.data + other.data
        else:
            if self.is_double():
                self.data.append(other.data)
            else:
                other.data.insert(0, self.data)
                self = other
        return self


class AwaVM:

    def __init__(self) -> None:
        self.abyss: list[Bubble] = []

    @staticmethod
    def decode_string_to_binary_awa(awa_string: str) -> list[int]:
        binary_awa = []
        skip = False
        assert len(awa_string) % 2 == 0
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

    @staticmethod
    def decode_binary_awa_to_awa_ir(binary: list[int]) -> list:
        ir = []
        while binary:
            op = binary_string_to_int("".join([str(n) for n in binary[:5]]))  ##UNTESTED
            binary = binary[5:]
            match op:
                case 0x5:
                    data = binary_string_to_int("".join([str(n) for n in binary[:8]]))
                    binary = binary[8:]
                case 0x6 | 0x9 | 0x10 | 0x11:
                    data = binary_string_to_int("".join([str(n) for n in binary[:5]]))
                    binary = binary[5:]
                case _:
                    data = None
            ir.append((op, data))
        return ir

    def read_program(self, raw_program_text: str):
        checksum = raw_program_text[:3].lower()
        program_data_raw = raw_program_text[3:].lower().rstrip()
        assert checksum == "awa"
        assert len(program_data_raw) % 2 == 0
        binary_data = AwaVM.decode_string_to_binary_awa(program_data_raw)
        program_data_ir = AwaVM.decode_binary_awa_to_awa_ir(binary_data)
        return program_data_ir

    # def print_bubble(bubble):
    #     pass

    def pop_top(self):
        bubble = self.abyss.pop()
        if bubble.is_double():
            self.abyss += bubble.data

    def execute_ir(self, awa_ir):
        assert awa_ir
        program_counter = 0
        while program_counter < len(awa_ir):
            instruction, data = awa_ir[program_counter]
            if DEBUG:
                print(
                    f"Executing instruction #{program_counter} [{instruction}] with data [{data}]..."
                )
            match instruction:
                case 0x00:
                    pass
                case 0x01:
                    bubble = self.abyss.pop()
                    print(str(bubble), "")
                case 0x02:
                    bubble = self.abyss.pop()
                    print(bubble.string_as_number(), "")
                case 0x03:
                    input_string = input()  # TO BE FIXED
                    decoded = string_to_AwaSCII(input_string)
                    for value in decoded:
                        self.abyss.append(Bubble(value))
                case 0x04:
                    input_string = input()  # TO BE FIXED
                    while not input_string.isnumeric():
                        input_string = input_string[:-1]  # THIS IS DUMB
                    self.abyss.append(Bubble(int(input_string)))
                case 0x05: #blow
                    self.abyss.append(Bubble(data))
                case 0x06: #submerge
                    bubble = self.abyss.pop()
                    if data == 0:
                        self.abyss.insert(0, bubble)
                    else:
                        self.abyss.insert(data * -1, bubble)
                case 0x07: #pop
                    self.pop_top()
                case 0x08: #duplicate
                    self.abyss.append(Bubble(copy.deepcopy(self.abyss[-1].data)))
                case 0x09: #surround
                    bubble = Bubble([])
                    for _ in range(data):
                        bubble.data.append(self.abyss.pop())
                    self.abyss.append(bubble)
                case 0x0A: #merge
                    bub1, bub2 = self.abyss.pop(), self.abyss.pop()
                    self.abyss.append(bub1.mrg(bub2))
                case 0x0B: #add
                    bub1, bub2 = self.abyss.pop(), self.abyss.pop()
                    self.abyss.append(bub1 + bub2)
                case 0x0C: #sub
                    bub1, bub2 = self.abyss.pop(), self.abyss.pop()
                    self.abyss.append(bub1 - bub2)
                case 0x0D: #mul
                    bub1, bub2 = self.abyss.pop(), self.abyss.pop()
                    self.abyss.append(bub1 * bub2)
                case 0x0E: #div
                    bub1, bub2 = self.abyss.pop(), self.abyss.pop()
                    self.abyss.append(bub1 // bub2)
                case 0x0F: #count
                    self.abyss.append(len(self.abyss[0]))
                case 0x10: #label
                    pass
                case 0x11: #jmp
                    for location_idx, ir_tuple in enumerate(awa_ir):
                        instruction2, data2 = ir_tuple
                        if instruction2 == 0x10 and data2 == data:
                            program_counter = location_idx
                            continue
                case 0x12: #eql
                    if len(self.abyss) < 2:
                        program_counter += 2
                        continue
                    if not self.abyss[0].data == self.abyss[1].data:
                        program_counter += 2
                        continue
                case 0x13: #gt
                    if len(self.abyss) < 2:
                        program_counter += 2
                        continue
                    if not self.abyss[0].data < self.abyss[1].data:
                        program_counter += 2
                        continue
                case 0x14: #lt
                    if len(self.abyss) < 2:
                        program_counter += 2
                        continue
                    if not self.abyss[0].data > self.abyss[1].data:
                        program_counter += 2
                        continue
                case 0x1F: #exit
                    return
                case _:
                    raise Exception
            program_counter += 1

    def run_program(self, raw_program):
        ir = self.read_program(raw_program)
        self.execute_ir(ir)


def main(argv: list[str]):
    if argv:
        filename = argv[-1]
    else:
        filename = "program.🚆"
    try:
        with open(filename) as file:
            raw_program_text = file.read().strip("\n")
    except FileNotFoundError:
        print(f'"{filename}" not found! exiting...')
        quit()

    try:
        with open("input") as file:
            raw_input = file.read()
    except FileNotFoundError:
        raw_input = ""

    vm = AwaVM()

    vm.run_program(raw_program=raw_program_text)


if __name__ == "__main__":
    main(sys.argv[1:])
