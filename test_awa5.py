#!/usr/bin/env python3
from __future__ import annotations
import itertools

from awa5 import AwaVM

ANSI_WHITE = "\033[0m"
ANSI_RED = "\033[31m"
ANSI_GREEN = "\033[32m"

PASS_STRING = f"{ANSI_GREEN}PASS{ANSI_WHITE}"
FAIL_STRING = f"{ANSI_RED}FAIL{ANSI_WHITE}"


output_buffer: str
input_buffer: str


def test_output_function(string: str):
    global output_buffer
    output_buffer += string


def test_input_function():
    global input_buffer
    return input_buffer


def load_tests(filename: str) -> list:
    with open(filename) as file:
        testcases = [
            (
                test_label.strip("\n"),
                code.strip("\n"),
                input.strip("\n"),
                expected_output.strip("\n"),
            )
            for test_label, code, input, expected_output in itertools.batched(
                file.read().split("!")[:-1], 4
            )
        ]
    return testcases


def run_tests(testcases: list) -> None:
    global input_buffer, output_buffer

    for test_idx, (test_label, code, input, expected_output) in enumerate(testcases):
        output_buffer = ""
        input_buffer = input

        vm = AwaVM(
            output_function=test_output_function, input_function=test_input_function
        )
        vm.run_program(code)

        passed = output_buffer.strip("\n") == expected_output
        print(f"Test #{test_idx + 1}: {PASS_STRING if passed else FAIL_STRING}")
        if not passed:
            print(f"Expected: {expected_output}")
            print(f"Got: {output_buffer}")


if __name__ == "__main__":

    tests = load_tests("test_cases.txt")

    run_tests(tests)
