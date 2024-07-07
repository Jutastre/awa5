# AWA5.0

## What is AWA5.0?
AWA5.0 is a silly esolang related to vtuber Jelly Hoshiumi of Phase Connect.
More info at https://esolangs.org/wiki/AWA5.0

## What is in this repo?

### Interpreter

/interpreter/awa5.py is an interpreter written in python.
Execute it with a program named "program.🌠" in the same folder, or specify a different file with a command line parameter, to run an AWA5.0 program directly.

### Transpiler

/transpiler/awa5transpiler.py takes an AWA5.0 program as input and outputs a human-readable .c file with equivalent function.

#### Usage and options:

Usage: awa5transpiler.py [options] source_file

source_file defaults to "program.🌠"

output_file defaults to appending ".🌠" to source_file unless source_file ends
with ".c", in which case the ".c" will be replaced by ".🌠".

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

    -O                              enable optimizer pass

    --surround-on-merge-simple      makes merge instruction surround instead of
                                    add when both top bubbles are simple (this
                                    matches other implementations, but not the
                                    specification)

### Tools

tools/ir_to_awa.py translates from a simple intermediate representation into proper awatalk for the interpreter or transpiler to read.
The transpiler can output the same IR if the flag -ir is used.

IR example:

    5 0
    5 1
    5 0
    5 1
    5 0
    9 5
    1