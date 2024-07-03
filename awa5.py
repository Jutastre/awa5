#!/usr/bin/env python3
from __future__ import annotations
import sys
import itertools
import copy
import re  # OH NO NOT THE REGEX

# TODO: input from file
# TODO: negative number handling, both in and out


DEBUG = False
DEBUG_INGESTION = False

# PATCHES
SURROUND_ON_SIMPLE_MERGE = True
BLOW_ZERO_ON_EMPTY = False


AwaSCII_LOOKUP = "AWawJELYHOSIUMjelyhosiumPCNTpcntBDFGRbdfgr0123456789 .,!'()~_/;\n"


class MalformedCodeException(Exception):
    pass


class UnknownInstructionException(Exception):
    pass

class AwaRuntimeError(Exception):
    pass

class Bubble:
    def __init__(self, data: int | list | Bubble) -> None:
        self.data: int | list | Bubble
        if isinstance(data, Bubble):
            self.data = copy.deepcopy(data.data)
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
        if self.data == 1:  # identity shortcuts
            return other
        if other.data == 1:
            return self

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
                for d1, d2 in itertools.zip_longest(
                    reversed(self.data), reversed(other.data), fillvalue=1
                )
            ].reverse()  # think these reverses fixes order
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
                    reversed(self.data), reversed(other.data), fillvalue=1
                )
            ].reverse()  # could be correct but idk
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
            return "".join(reversed([str(sub) for sub in self.data]))
        else:
            return AwaVM._AwaSCII_to_string(self.data)

    def __repr__(self) -> str:

        if self.is_double():
            contents = ",".join([repr(sub) for sub in self.data])
        else:
            contents = str(self.data)
        return f"B[{contents}]"

    def as_number(self: Bubble) -> str:
        if self.is_double():
            return " ".join(
                reversed([sub.as_number() for sub in self.data])
            )  # why is sub any type?
        else:
            return re.sub("-", "~", str(self.data))

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
        self.input_function: function = input_function
        self.output_function: function = output_function

    @staticmethod
    def _dirty_string_cleanup(string: str):
        return re.sub(f"[^{AwaSCII_LOOKUP}]", "", string)

    @staticmethod
    def _AwaSCII_to_string(number) -> str:
        return AwaSCII_LOOKUP[number]

    @staticmethod
    def _char_to_AwaSCII(char: str) -> int:
        return AwaSCII_LOOKUP.find(char)

    @staticmethod
    def _string_to_AwaSCII(string: str) -> list[int]:
        return [AwaVM._char_to_AwaSCII(char) for char in string]

    @staticmethod
    def _binary_string_to_int(string: str) -> int:
        total = 0
        negative = False
        if len(string) == 8:
            if int(string[0]):
                negative = True
        for char in string:
            total *= 2
            if char == "1":
                total += 1
        if negative:
            return total - pow(2, 8)
        else:
            return total

    @staticmethod
    def _awa_string_to_binary_string(awa_string: str) -> list[int]:
        return re.sub("wa", "1", re.sub(" awa", "0", awa_string))

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

    @staticmethod
    def _awa_string_to_ir(raw_program_text: str):
        # I DIDNT wANNA USe REGEX I SWEAR
        raw_program_text = re.sub("[^AWaw ]", "", raw_program_text)
        checksum = raw_program_text[:3].lower()
        program_data_raw = raw_program_text[3:].lower().rstrip()
        assert checksum == "awa"
        if len(program_data_raw) % 2 != 0:
            raise MalformedCodeException(f"Code length mismatch")

        ## warnings for specific "common" errors i've seen in code
        if "  " in raw_program_text:
            raise MalformedCodeException(
                f"'  ' found in input at location {raw_program_text.find('  ')} (after non-awatalk has been discarded)"
            )
        if " wa" in raw_program_text:
            raise MalformedCodeException(
                f"' wa' found in input at location {raw_program_text.find(' wa')} (after non-awatalk has been discarded)"
            )

        binary_data = AwaVM._awa_string_to_binary_string(program_data_raw)
        program_data_ir = AwaVM._binary_string_to_ir(binary_data)
        return program_data_ir

    def _pop_top(self):
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
                    self.output_function(bubble.as_number())
                case 0x03:
                    input_string = self.input_function()
                    decoded = AwaVM._string_to_AwaSCII(input_string)
                    self.abyss.append(Bubble([Bubble(value) for value in decoded]))
                case 0x04:
                    input_string = AwaVM._dirty_string_cleanup(self.input_function())
                    extracted_number_string = re.findall("~?[0-9]+", input_string)[
                        0
                    ]  # can surely do this with a more appropriate regex function
                    extracted_number_string = re.sub("~", "-", extracted_number_string)
                    # while not input_string.isnumeric():
                    #     input_string = input_string[:-1]  # THIS IS DUMB and wrong
                    self.abyss.append(Bubble(int(extracted_number_string)))
                case 0x05:  # blow
                    self.abyss.append(Bubble(data))
                case 0x06:  # submerge
                    bubble = self.abyss.pop()
                    if data == 0:
                        self.abyss.insert(0, bubble)
                    else:
                        self.abyss.insert(data * -1, bubble)
                case 0x07:  # pop
                    self._pop_top()
                case 0x08:  # duplicate
                    self.abyss.append(Bubble(copy.deepcopy(self.abyss[-1].data)))
                case 0x09:  # surround
                    bubble = Bubble([])
                    for _ in range(data):
                        bubble.data.insert(0, self.abyss.pop())
                    self.abyss.insert(0, bubble)
                case 0x0A:  # merge
                    bub1, bub2 = self.abyss.pop(), self.abyss.pop()
                    self.abyss.append(bub1.mrg(bub2))
                case 0x0B:  # add
                    if len(self.abyss) < 2:
                        if BLOW_ZERO_ON_EMPTY:
                            self.abyss.append(Bubble(0))
                            program_counter += 1
                            continue
                        else:
                            raise AwaRuntimeError(f"Tried to execute {f'{instruction:#2X}'.replace('0X', '0x')} but less than 2 bubbles were in the abyss")
                    bub1, bub2 = self.abyss.pop(), self.abyss.pop()
                    self.abyss.append(bub1 + bub2)
                case 0x0C:  # sub
                    if len(self.abyss) < 2:
                        if BLOW_ZERO_ON_EMPTY:
                            self.abyss.append(Bubble(0))
                            program_counter += 1
                            continue
                        else:
                            raise AwaRuntimeError(f"Tried to execute {f'{instruction:#2X}'.replace('0X', '0x')} but less than 2 bubbles were in the abyss")
                    bub1, bub2 = self.abyss.pop(), self.abyss.pop()
                    self.abyss.append(bub1 - bub2)
                case 0x0D:  # mul
                    if len(self.abyss) < 2:
                        if BLOW_ZERO_ON_EMPTY:
                            self.abyss.append(Bubble(0))
                            program_counter += 1
                            continue
                        else:
                            raise AwaRuntimeError(f"Tried to execute {f'{instruction:#2X}'.replace('0X', '0x')} but less than 2 bubbles were in the abyss")
                    bub1, bub2 = self.abyss.pop(), self.abyss.pop()
                    self.abyss.append(bub1 * bub2)
                case 0x0E:  # div
                    if len(self.abyss) < 2:
                        if BLOW_ZERO_ON_EMPTY:
                            self.abyss.append(Bubble(0))
                            program_counter += 1
                            continue
                        else:
                            raise AwaRuntimeError(f"Tried to execute {f'{instruction:#2X}'.replace('0X', '0x')} but less than 2 bubbles were in the abyss")
                    bub1, bub2 = self.abyss.pop(), self.abyss.pop()
                    self.abyss.append(bub1 // bub2)
                case 0x0F:  # count
                    if len(self.abyss) < 1:
                        if BLOW_ZERO_ON_EMPTY:
                            self.abyss.append(Bubble(0))
                            program_counter += 1
                            continue
                        else:
                            raise AwaRuntimeError(f"Tried to execute {f'{instruction:#2X}'.replace('0X', '0x')} but abyss was empty")
                    bubble = self.abyss[0]
                    if bubble.is_double():
                        self.abyss.append(Bubble(len(self.abyss[0].data)))
                    else:
                        self.abyss.append(Bubble(0))
                case 0x10:  # label
                    pass
                case 0x11:  # jmp
                    for location_idx, (instruction2, data2) in enumerate(awa_ir):
                        if instruction2 == 0x10 and data2 == data:
                            program_counter = location_idx
                            break
                    else:
                        raise AwaRuntimeError(f"Tried to jump to label {data} but it wasn't found")
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
                    raise UnknownInstructionException(
                        f"Instruction {f'{instruction:#2X}'.replace('0X', '0x')} not recognized"
                    )
            program_counter += 1

    def run_program(self, raw_program):
        ir = AwaVM._awa_string_to_ir(raw_program)
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
