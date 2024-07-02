#!/usr/bin/env python3
from __future__ import annotations
import sys
import itertools
import copy
import re  # OH NO NOT THE REGEX

DEBUG = False
DEBUG_INGESTION = False

# PATCHES
SURROUND_ON_SIMPLE_MERGE = True
BLOW_ZERO_ON_EMPTY = False


AwaSCII_LOOKUP = "AWawJELYHOSIUMjelyhosiumPCNTpcntBDFGRbdfgr0123456789 .,!'()~_/;\n"


def AwaSCII_to_string(number) -> str:
    return AwaSCII_LOOKUP[number]


def char_to_AwaSCII(char: str) -> int:
    return AwaSCII_LOOKUP.find(char)


def string_to_AwaSCII(string: str) -> list[int]:
    return [char_to_AwaSCII(char) for char in string]



class Bubble:
    def __init__(self, data: int | list | Bubble) -> None:
        self.data: int | list | Bubble
        if isinstance(data, Bubble):
            self.data = data.data
        else:
            self.data = data

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
            return Bubble(
                [Bubble(self.data % other.data), Bubble(self.data // other.data)]
            )
        elif self.is_double() != other.is_double():
            if other.is_double():
                self, other = other, self
            simple = other.data
            self.data = [d1 // simple for d1 in self.data]
        else:
            self.data = [
                d1 // d2
                for d1, d2 in itertools.zip_longest(
                    self.data, other.data, fillvalue=1
                )  # this isn't correct
            ]
        return self

    def __sizeof__(self) -> int:
        if self.is_double():
            return 0
        else:
            return len(self.data)

    def is_double(self):
        return isinstance(self.data, list)

    def __str__(self) -> str:
        if self.is_double():
            return "".join([str(sub) for sub in self.data])
        else:
            return AwaSCII_to_string(self.data)

    def __repr__(self) -> str:

        if self.is_double():
            contents = ",".join([repr(sub) for sub in self.data])
        else:
            contents = str(self.data)
        return f"B[{contents}]"

    def string_as_number(self: Bubble) -> str:
        if self.is_double():
            return " ".join(
                [sub.string_as_number() for sub in self.data]
            )  # why is sub any type?
        else:
            return str(self.data)  # this might be wrong but doc is hard to interpret

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
            if SURROUND_ON_SIMPLE_MERGE and not self.is_double():
                return Bubble([self, other])
            else:
                self.data = self.data + other.data
        else:
            if self.is_double():
                self.data.append(other.data)
            else:
                other.data.insert(0, self.data)
                self = other
        return self


class AwaVM:

    def print_wrapper(string: str) -> None:
        print(string, end="")

    def __init__(
        self,
        input_function: function = input,
        output_function: function = print_wrapper,
    ) -> None:
        self.abyss: list[Bubble] = []
        self.input_function = input_function
        self.output_function = output_function

    @staticmethod
    def _binary_string_to_int(string: str) -> int:
        total = 0
        negative = False
        if len(string) == 8:
            if int(string[0]):
                negative = True
            string = string[1:]
        for char in string:
            total *= 2
            if char == "1":
                total += 1
        if negative:
            return 0 - total
        else:
            return total
        
    @staticmethod
    def _awa_string_to_binary_string(awa_string: str) -> list[int]:
        return re.sub('wa', '1', re.sub(' awa', '0', awa_string))
    
    @staticmethod
    def _binary_string_to_ir(binary: list[int]) -> list:
        ir = []
        while binary:
            op = AwaVM._binary_string_to_int(binary[:5])  ##UNTESTED
            binary = binary[5:]
            match op:
                case 0x5:
                    data = AwaVM._binary_string_to_int(binary[:8])
                    binary = binary[8:]
                case 0x6 | 0x9 | 0x10 | 0x11:
                    data = AwaVM._binary_string_to_int(binary[:5])
                    binary = binary[5:]
                case _:
                    data = None
            ir.append((op, data))
        return ir


    def read_program(self, raw_program_text: str):
        # I DIDNT wANNA USe REGEX I SWEAR
        raw_program_text = re.sub("[^AWaw ]", "", raw_program_text)
        raw_program_text = re.sub("  ", " ", raw_program_text)
        checksum = raw_program_text[:3].lower()
        program_data_raw = raw_program_text[3:].lower().rstrip()
        assert checksum == "awa"
        assert len(program_data_raw) % 2 == 0
        #binary_data = AwaVM.decode_string_to_binary_awa(program_data_raw)
        #program_data_ir = AwaVM.decode_binary_awa_to_awa_ir(binary_data)
        binary_data = AwaVM._awa_string_to_binary_string(program_data_raw)
        program_data_ir = AwaVM._binary_string_to_ir(binary_data)
        return program_data_ir

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
                    self.output_function(str(bubble))
                case 0x02:
                    bubble = self.abyss.pop()
                    self.output_function(bubble.string_as_number())
                case 0x03:
                    input_string = self.input_function()
                    decoded = string_to_AwaSCII(input_string)
                    self.abyss.append(Bubble([Bubble(value) for value in decoded]))
                case 0x04:
                    input_string = self.input_function()
                    while not input_string.isnumeric():
                        input_string = input_string[:-1]  # THIS IS DUMB and wrong
                    self.abyss.append(Bubble(int(input_string)))
                case 0x05:  # blow
                    self.abyss.append(Bubble(data))
                case 0x06:  # submerge
                    bubble = self.abyss.pop()
                    if data == 0:
                        self.abyss.insert(0, bubble)
                    else:
                        self.abyss.insert(data * -1, bubble)
                case 0x07:  # pop
                    self.pop_top()
                case 0x08:  # duplicate
                    self.abyss.append(Bubble(copy.deepcopy(self.abyss[-1].data)))
                case 0x09:  # surround
                    bubble = Bubble([])
                    for _ in range(data):
                        bubble.data.append(self.abyss.pop())
                    self.abyss.insert(0, bubble)
                case 0x0A:  # merge
                    bub1, bub2 = self.abyss.pop(), self.abyss.pop()
                    self.abyss.append(bub1.mrg(bub2))
                case 0x0B:  # add
                    if len(self.abyss) < 2 and BLOW_ZERO_ON_EMPTY:
                        self.abyss.append(Bubble(0))
                        program_counter += 1
                        continue
                    bub1, bub2 = self.abyss.pop(), self.abyss.pop()
                    self.abyss.append(bub1 + bub2)
                case 0x0C:  # sub
                    if len(self.abyss) < 2 and BLOW_ZERO_ON_EMPTY:
                        self.abyss.append(Bubble(0))
                        program_counter += 1
                        continue
                    bub1, bub2 = self.abyss.pop(), self.abyss.pop()
                    self.abyss.append(bub1 - bub2)
                case 0x0D:  # mul
                    if len(self.abyss) < 2 and BLOW_ZERO_ON_EMPTY:
                        self.abyss.append(Bubble(0))
                        program_counter += 1
                        continue
                    bub1, bub2 = self.abyss.pop(), self.abyss.pop()
                    self.abyss.append(bub1 * bub2)
                case 0x0E:  # div
                    if len(self.abyss) < 2 and BLOW_ZERO_ON_EMPTY:
                        self.abyss.append(Bubble(0))
                        program_counter += 1
                        continue
                    bub1, bub2 = self.abyss.pop(), self.abyss.pop()
                    self.abyss.append(bub1 // bub2)
                case 0x0F:  # count
                    if len(self.abyss) < 1 and BLOW_ZERO_ON_EMPTY:
                        self.abyss.append(Bubble(0))
                        program_counter += 1
                        continue
                    bubble = self.abyss[0]
                    if bubble.is_double():
                        self.abyss.append(Bubble(len(self.abyss[0].data)))
                    else:
                        self.abyss.append(Bubble(0))
                case 0x10:  # label
                    pass
                case 0x11:  # jmp
                    for location_idx, (instruction2, data2) in enumerate(awa_ir):
                        # instruction2, data2 = ir_tuple
                        if instruction2 == 0x10 and data2 == data:
                            program_counter = location_idx
                            continue
                case 0x12:  # eql
                    if len(self.abyss) < 2:
                        program_counter += 2
                        continue
                    if not self.abyss[-1].data == self.abyss[-2].data:
                        program_counter += 2
                        continue
                case 0x13:  # gt
                    if len(self.abyss) < 2:
                        program_counter += 2
                        continue
                    if not self.abyss[-1].data > self.abyss[-2].data:
                        program_counter += 2
                        continue
                case 0x14:  # lt
                    if len(self.abyss) < 2:
                        program_counter += 2
                        continue
                    if not self.abyss[-1].data < self.abyss[-2].data:
                        program_counter += 2
                        continue
                case 0x1F:  # exit
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
        filename = "program.🌠"
    try:
        with open(filename) as file:
            raw_program_text = file.read().strip()
    except FileNotFoundError:
        print(f'"{filename}" not found! exiting...')
        quit()

    ## TODO: input from file
    # try:
    #     with open("input") as file:
    #         raw_input = file.read()
    # except FileNotFoundError:
    #     raw_input = ""

    vm = AwaVM()

    vm.run_program(raw_program=raw_program_text)


if __name__ == "__main__":
    main(sys.argv[1:])
