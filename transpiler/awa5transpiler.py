#!/usr/bin/env python3
from __future__ import annotations
import sys
import re  # OH NO NOT THE REGEX
import itertools  # always import itertools, you'll need them sooner or later

from Cblocks import *

USAGE_STRING = "Usage: awa5transpiler.py [options] source_file"

HELP_STRING = """
source_file defaults to \"program.🌠\"

output_file defaults to appending \".🌠\" to source_file unless source_file ends
with \".c\", in which case the \".c\" will be replaced by \".🌠\".

if source_file is "stdin" output will be read from stdin instead
if output_file is "stdout" output will be written to stdout instead

Options:

    -a, --parse-args                makes the output program read command line
                                    arguments as input (once arguments are 
                                    exhausted it will revert back to user 
                                    input)

    -f source_file                  specify input file to read awatalk from

    -h, --help                      displays this text

    -ir, --output-ir                outputs IR instead of c code

    --no-inline                     makes functions in output not static inline

    -o output_file                  specify output filename

    -O0                             disable optimizer pass

    -O1                             enable safe optimizations; these can't 
                                    break the behaviour of the program

    -O2                             enable all optimizations; can break
                                    programs in rare cases (never seen in the 
                                    wild)

    -p, --pipe                      sets source_file and output_file to stdin 
                                    and stdout respectively

    --surround-on-merge-simple      makes merge instruction surround instead of
                                    add when both top bubbles are simple (this
                                    matches other implementations, but not the
                                    specification)"""

AwaSCII_LOOKUP = "AWawJELYHOSIUMjelyhosiumPCNTpcntBDFGRbdfgr0123456789 .,!'()~_/;\n"
REVERSE_AwaSCII_LOOKUP = [
    56,
    56,
    56,
    56,
    56,
    56,
    56,
    56,
    56,
    56,
    63,
    56,
    56,
    56,
    56,
    56,
    56,
    56,
    56,
    56,
    56,
    56,
    56,
    56,
    56,
    56,
    56,
    56,
    56,
    56,
    56,
    56,
    52,
    55,
    56,
    56,
    56,
    56,
    56,
    56,
    57,
    58,
    56,
    56,
    54,
    56,
    53,
    61,
    42,
    43,
    44,
    45,
    46,
    47,
    48,
    49,
    50,
    51,
    56,
    62,
    56,
    56,
    56,
    56,
    56,
    0,
    32,
    25,
    33,
    5,
    34,
    35,
    8,
    11,
    4,
    56,
    6,
    13,
    26,
    9,
    24,
    56,
    36,
    10,
    27,
    12,
    56,
    1,
    56,
    7,
    56,
    56,
    56,
    56,
    56,
    60,
    56,
    2,
    37,
    29,
    38,
    15,
    39,
    40,
    18,
    21,
    14,
    56,
    16,
    23,
    30,
    19,
    28,
    56,
    41,
    20,
    31,
    22,
    56,
    3,
    56,
    17,
    56,
    56,
    56,
    56,
    59,
]


class MalformedCodeException(Exception):
    pass


class Ingester:
    def __init__() -> None:
        pass

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
        return [Ingester._char_to_AwaSCII(char) for char in string]

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
            op = Ingester._binary_string_to_int(binary[:5])  ##UNTESTED
            binary = binary[5:]
            match op:
                case 0x5:
                    data = Ingester._binary_string_to_int(binary[:8])
                    binary = binary[8:]
                case 0x6 | 0x9 | 0x10 | 0x11:
                    data = Ingester._binary_string_to_int(binary[:5])
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
                f"\"  \" found in input at location {raw_program_text.find('  ')} (after non-awatalk has been discarded)"
            )
        if " wa" in raw_program_text:
            raise MalformedCodeException(
                f"\" wa\" found in input at location {raw_program_text.find(' wa')} (after non-awatalk has been discarded)"
            )

        binary_data = Ingester._awa_string_to_binary_string(program_data_raw)
        program_data_ir = Ingester._binary_string_to_ir(binary_data)
        return program_data_ir


def ir_cleanup(ir):
    return [line for line in ir if len(line) != 0]


class OptimizerPatternMissException(BaseException):
    pass


def optimizer(ir: list[tuple[int, int]], options) -> list[tuple[int, int]]:

    if (level := options.get("optimize", 1)) <= 0 :
        return ir
    if verbose :=options.get("verbose", False):
        print(f"running optimizer pass...")

    if verbose :
        print(f"before optimizations: {len(ir)}")

    # find blow -> print pairs and replace with "print_string char"
    for idx, (line1, line2) in enumerate(itertools.pairwise(ir)):
        if line1[0] == 5 and line2[0] == 1:
            ir[idx] = ("print_string", AwaSCII_LOOKUP[line1[1]].replace("\n", "\\n"))
            ir[idx + 1] = tuple()
    ir = ir_cleanup(ir)
    if verbose :
        print(f"after step 1: {len(ir)}")
    # find blow -> surround -> print sequences; replace with "print_string"

    for idx in range(len(ir) - 1, -1, -1):

        if len(ir[idx]) != 0 and ir[idx][0] == 1:
            try:
                if idx <= 1:
                    raise OptimizerPatternMissException
                if ir[idx - 1][0] == 0x09:
                    surrounded = ir[idx - 1][1]
                    values_to_print = []
                    for offset in range(surrounded):
                        if idx - 2 - offset < 0:
                            raise OptimizerPatternMissException
                        if ir[idx - 2 - offset][0] != 5:
                            raise OptimizerPatternMissException
                        values_to_print.append(ir[idx - 2 - offset][1])
                    # if you get this far without errors its g2g
                    string_to_print = "".join(
                        [AwaSCII_LOOKUP[n] for n in values_to_print]
                    ).replace("\n", "\\n")
                    ir[idx] = ("print_string", string_to_print)
                    ir[idx - 1] = tuple()
                    for offset in range(surrounded):
                        ir[idx - 2 - offset] = tuple()

            except OptimizerPatternMissException as ex:
                pass
    ir = ir_cleanup(ir)
    if verbose :
        print(f"after step 2: {len(ir)}")

    # merge consecutive prints

    old_len = 0

    while len(ir) != old_len:
        for idx in range(len(ir) - 1):
            if ir[idx][0] == "print_string" and ir[idx + 1][0] == "print_string":
                ir[idx] = tuple()
                ir[idx + 1] = ("print_string", ir[idx][1] + ir[idx + 1][1])
        ir = ir_cleanup(ir)
        old_len = len(ir)
    if verbose :
        print(f"after step 3: {len(ir)}")

    # find div -> pop -> pop and replace with "fast_modulo"
    if level >= 2:
        for idx in range(len(ir) - 2):
            if not ir[idx]:
                continue
            if (ir[idx][0], ir[idx + 1][0], ir[idx + 2][0]) == (0x0E, 0x07, 0x07):
                ir[idx] = ("fast_modulo", None)
                ir[idx + 1], ir[idx + 2] = tuple(), tuple()

        ir = ir_cleanup(ir)
        if verbose :
            print(f"after step 4: {len(ir)}")
    return ir


def codegen(awa_ir, options=None) -> str:
    if not options:
        options = {}

    # apply patches to codeset

    if not options.get("add_on_merge_simple", True):
        c_functions[0x0A] = c_functions["alternative 0x0A"]
        dependencies[0x0A] = dependencies["alternative 0x0A"]

    if options.get("arg_parse", False):
        c_functions[0x03] = c_functions["0x03 argparse"]
        c_functions[0x04] = c_functions["0x04 argparse"]
        c_code[0x03] = c_code["0x03 argparse"]
        c_code[0x04] = c_code["0x04 argparse"]

    head_pieces = []
    code_pieces = []

    instruction_set = set()

    # construct code body

    if options.get("arg_parse", False):
        code_pieces.append(
            "\n\nint main(int argc, char ** argv) {\n    size_t args_consumed = 1;\n"
        )
    else:
        code_pieces.append("\n\nint main() {\n")

    entering_block = False
    exiting_block = False
    for instruction, parameter in awa_ir:
        code_pieces.append("    ")
        instruction_set.add(instruction)
        match instruction:
            case 0x10:  # label
                code_pieces.append(f"lbl_{parameter}:\n")
            case 0x11:  # jmp
                code_pieces.append(f"goto lbl_{parameter};\n")
            case 0x12 | 0x13 | 0x14:  # eq/gt/lt
                code_pieces.append(c_code[instruction])
                entering_block = True
            case 0x1F:  # exit
                code_pieces.append("return 0;\n")
            case _:
                code_pieces.append(
                    c_code[instruction].replace("%FUNCTION_PARAMETER%", str(parameter))
                )

        if (
            exiting_block
        ):  # this feels dirty but idk how else; should make it insert an "end" instruction into ir once i have an pass optimizer
            code_pieces.append("    }\n")
            exiting_block = False
        if entering_block:
            entering_block = False
            exiting_block = True

    if exiting_block:
        code_pieces.append("    }\n")
    code_pieces.append("    return 0;\n}\n")

    # construct header

    # add dependencies:

    for instruction in instruction_set.copy():
        if instruction in dependencies:
            for dependency in dependencies[instruction]:
                instruction_set.add(dependency)

    head_pieces.append(boilerplate)

    # these need to be added in correct order before other functions
    # / and / or removed to be able to sort the numerical instructions
    if "awascii_lookup" in instruction_set:
        head_pieces.append(awascii_lookup)
        instruction_set.remove("awascii_lookup")
    if "reverse_awascii_lookup" in instruction_set:
        head_pieces.append(reverse_awascii_lookup)
        instruction_set.remove("reverse_awascii_lookup")
    if "delete" in instruction_set:
        head_pieces.append(c_functions["delete"])
        instruction_set.remove("delete")
    if 5 in instruction_set:
        head_pieces.append(c_functions[0x05])
        instruction_set.remove(0x05)
    if "fast_modulo" in instruction_set:
        head_pieces.append(c_functions["fast_modulo"])
        instruction_set.remove("fast_modulo")
    if "print_string" in instruction_set:
        instruction_set.remove("print_string")

    for instruction in sorted(instruction_set):  # rest can be added in numerical order
        if instruction in c_functions:
            head_pieces.append(c_functions[instruction])

    header = "".join(head_pieces)
    body = "".join(code_pieces)

    if not options.get("inline", True):
        header.replace("static inline ", "")

    return header + body


def main(argv: list[str]):
    # initialize vars:

    filename = None
    output_filename = None

    options = {}

    # option defaults:

    options["arg_parse"] = False
    options["inline"] = True
    options["add_on_merge_simple"] = True
    options["output_ir"] = False
    options["optimize"] = 1
    options["verbose"] = False

    # parse args: (this is not pretty, should write my own lib for this)
    if (
        argv
        and argv[-1][0] != "-"
        and not (len(argv) >= 2 and (argv[-2] == "-o" or argv[-2] == "-f"))
    ):
        # use last arg as input unless it follows -o
        filename = argv[-1]
        argv = argv[:-1]

    for arg_idx, arg in enumerate(argv):
        match arg:
            case "-a" | "--parse-args":
                options["arg_parse"] = True
            case "-h" | "--help":
                print(USAGE_STRING)
                print(HELP_STRING)
                quit()
            case "--no-inline":
                options["inline"] = False
            case "--surround-on-merge-simple":
                options["add_on_merge_simple"] = False
            case "-ir" | "--output-ir":
                options["output_ir"] = True
            case "-f":
                filename = argv[arg_idx + 1]
            case "-o":
                output_filename = argv[arg_idx + 1]
            case "-O0":
                options["optimize"] = 0
            case "-O1":
                options["optimize"] = 1
            case "-O2":
                options["optimize"] = 2
            case "-p" | "--pipe":
                filename = "stdin"
                output_filename = "stdout"
            case "-v" | "--verbose":
                options["verbose"] = True
            case _:
                if arg_idx == 0 or not (
                    argv[arg_idx - 1] == "-f" or argv[arg_idx - 1] == "-o"
                ):
                    print(USAGE_STRING)
                    quit()

    if not filename:
        filename = "program.🌠"

    if not output_filename:
        output_filename = filename + ".c"
        if filename[-2:] == ".🌠":
            output_filename = filename[:-2] + ".c"

    # read input file:
    if options["verbose"] and filename != "stdin":
        print(f"opening file {filename}...")

    if filename == "stdin":
        raw_program_text = input().strip()
    else:
        try:
            with open(filename) as file:
                raw_program_text = file.read().strip()
        except FileNotFoundError:
            print(f'"{filename}" not found! exiting...')
            quit()

    # decode:

    if options["verbose"]:
        print(f"decoding...")
    ir = Ingester._awa_string_to_ir(raw_program_text)

    # generate code:

    ir = optimizer(ir, options)

    if options.get("output_ir", False):
        output = "\n".join([" ".join([str(piece) for piece in line]) for line in ir])
    else:
        if options["verbose"]:
            print(f"generating code...")
        output = codegen(ir, options)

    if options["verbose"]:
        print(f"writing output to {output_filename}...")
    # write output to file:
    if output_filename == "stdout":
        print(output, end="")  # , end='\0')
    else:
        with open(output_filename, "w") as file:
            file.write(output)

    if options["verbose"]:
        print(f"Done!")


if __name__ == "__main__":
    main(sys.argv[1:])
