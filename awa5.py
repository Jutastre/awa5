#!/usr/bin/env python3
from __future__ import annotations
import sys
import itertools
import copy

def AwaSCII_to_string(number):
    lookup = "AWawJELYHOSIUMjelyhosiumPCNTpcntBDFGRbdfgr0123456789 .,!'()~_/;\n"
    return lookup[number]


class Bubble:
    def __init__(self, data:int|list|Bubble) -> None:
        if isinstance(data,Bubble):
            self.data=data.data
        else:
            self.data = data

    def __add__(self,other:Bubble):
        if not self.is_double() and not other.is_double():
            return Bubble(self.data + other.data)
        elif self.is_double() != other.is_double():
            if other.is_double():
                self,other = other,self
            simple = other.data
            self.data = [d1 + simple for d1 in self.data]
        else:
            self.data = [d1 + d2 for d1,d2 in itertools.zip_longest(self.data,other.data, fillvalue = 0)]
        return self
    
    def __sub__(self,other:Bubble):
        if not self.is_double() and not other.is_double():
            return Bubble(self.data - other.data)
        elif self.is_double() != other.is_double():
            if other.is_double():
                self,other = other,self
            simple = other.data
            self.data = [d1 - simple for d1 in self.data]
        else:
            self.data = [d1 - d2 for d1,d2 in itertools.zip_longest(self.data,other.data, fillvalue = 0)]
        return self    
    
    def __mul__(self,other:Bubble):
        if not self.is_double() and not other.is_double():
            return Bubble(self.data * other.data)
        elif self.is_double() != other.is_double():
            if other.is_double():
                self,other = other,self
            simple = other.data
            self.data = [d1 * simple for d1 in self.data]
        else:
            self.data = [d1 * d2 for d1,d2 in itertools.zip_longest(self.data,other.data, fillvalue = 0)]
        return self

    def is_double(self):
        return isinstance(self.data, list)

    # def print(self):
    #     string = ""

    def __str__(self) -> str:
        if self.is_double():
            return str("".join(self.data))
        else:
            return AwaSCII_to_string(self.data)

    def __repr__(self) -> str:
        if self.is_double():
            return repr(" ".join(self.data))
        else:
            return AwaSCII_to_string(self.data)
        
        
    def add(self,other:Bubble):
        if not self.is_double() and not other.is_double():
            return Bubble(self.data + other.data)
        elif self.is_double() != other.is_double():
            if other.is_double():
                self,other = other,self
            simple = other.data
            self.data = [d1 + simple for d1 in self.data]
        else:
            self.data = [d1 + d2 for d1,d2 in itertools.zip_longest(self.data,other.data, fillvalue = 0)]
        return self

    def mrg(self,other:Bubble):
        if self.is_double() == other.is_double(): #why am i doing this
            self.data =  self.data + other.data
        else:
            if self.is_double():
                self.data.append(other.data)
            else:
                other.data.insert(0, self.data)
                self = other
        return self


class AwaVM:

    def __init__(self) -> None:
        self.abyss:list[Bubble] = []

    @staticmethod
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

    @staticmethod
    def decode_binary_awa_to_awa_ir(binary: list[int]) -> list:
        ir = []
        while binary:
            op = int("0b" + "".join([str(n) for n in binary[:5]]))  ##UNTESTED
            binary = binary[5:]
            match op:
                case 0x5:
                    data = int(
                        "0b" + "".join([str(n) for n in binary[:8]])
                    )  ##obviously also untested
                    binary = binary[8:]
                case 0x6 | 0x9 | 0x10 | 0x11:
                    data = int(
                        "0b" + "".join([str(n) for n in binary[:5]])
                    )  ##obviously also untested
                    binary = binary[5:]
                case _:
                    data = None
            ir.append((op, data))

    def read_program(self, raw_program_text: str):
        checksum = raw_program_text[:3]
        program_data_raw = raw_program_text[3:]
        assert checksum == "awa"
        assert len(program_data_raw) % 2 == 0
        binary_data = AwaVM.decode_awa_to_binary_awa(raw_program_text)
        program_data = AwaVM.decode_binary_awa_to_awa_ir(binary_data)
        return program_data

    # def print_bubble(bubble):
    #     pass
    
    def pop_top(self):
        bubble = self.abyss.pop()
        if bubble.is_double():
            self.abyss += bubble.data

    def execute_ir(self, awa_ir):
        for instruction, data in awa_ir:
            match instruction:
                case 0x00:
                    continue
                case 0x01:
                    bubble = self.abyss.pop()
                    print(str(bubble))
                case 0x02:
                    bubble = self.abyss.pop()
                    print(repr(bubble))
                case 0x03:
                    ...
                case 0x04:
                    ...
                case 0x05:
                    self.abyss.append(Bubble(data))
                case 0x06:
                    bubble = self.abyss.pop()
                    if data == 0:
                        self.abyss.insert(0, bubble)
                    else:
                        self.abyss.insert(data * -1, bubble)
                case 0x07:
                    self.pop_top()
                case 0x08:
                    self.abyss.insert(Bubble(copy.deepcopy(self.abyss[-1].data)))
                case 0x09:
                    bubble = Bubble([])
                    for _ in range(data):
                        bubble.data.append(self.abyss.pop())
                    self.abyss.append(bubble)
                case 0x0A:
                    bub1,bub2 = self.abyss.pop(),self.abyss.pop()
                    self.abyss.append(bub1.mrg(bub2))
                case 0x0B:
                    bub1,bub2 = self.abyss.pop(),self.abyss.pop()
                    self.abyss.append(bub1 + bub2)
                case 0x0C:
                    bub1,bub2 = self.abyss.pop(),self.abyss.pop()
                    self.abyss.append(bub1 - bub2)
                case 0x0C:
                    bub1,bub2 = self.abyss.pop(),self.abyss.pop()
                    self.abyss.append(bub1 * bub2)

    def run_program(self, raw_program):
        ir = AwaVM.read_program(raw_program)
        self.execute_ir(ir)



def main(argv: list[str]):
    if argv:
        filename = argv[-1]
    else:
        filename = "program.🚆"
    try:
        with open(filename) as file:
            raw_program_text = file.read()
    except FileNotFoundError:
        print(f'"{filename}" not found! exiting...')
        quit()

    try:
        with open("input") as file:
            raw_input = file.read()
    except FileNotFoundError:
        raw_input = ""

    vm = AwaVM

    vm.run_program(raw_program_text)


if __name__ == "__main__":
    main(sys.argv[1:])
