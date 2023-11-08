#!/usr/bin/env python3

import json
import re
import sys

# Example of a CPE string:
# cpe:2.3:a:microsoft:internet_explorer:8.0.6001:beta:*:*:*:*:*:*
#
# Documentation: https://nvlpubs.nist.gov/nistpubs/Legacy/IR/nistir7695.pdf
#
# Required attributes, see '5.2 WFN Attributes':
# part, vendor, product, version, update,
# edition, lanuguage, sw_edition, target_sw,
# target_hw, other


def add_quoting(string: str) -> str:
    """Processes quoted characters in the input string.
    Escape characters are handled to produce a final string.

    For more info -> see '6.2.1 Syntax for Formatted String Binding'.

    Note:
        This function was implemented based on pseudocode provided in the official specification.
        For more info -> see:
            6.2.3.1 'Summary of algorithm'
            6.2.3.2 'Pseudocode for algorithm'

    Args:
        string (str): value to process

    Returns:
        str: processed value
    """
    result = ""
    idx = 0
    embedded = False
    while idx < len(string):
        char = string[idx]
        if char.isalnum() or char == "_":
            result += char
            idx += 1
            embedded = True
            continue

        if char == "\\":
            result += string[idx : idx + 1 + 1]
            idx += 2
            embedded = True
            continue

        if char == "*":
            if idx == 0 or idx == len(string) - 1:
                result += char
                idx += 1
                embedded = True
                continue
            else:
                raise ValueError(f"Unquoted asterisk must appear at the beggining or end of a component.")

        if char == "?":
            if idx == 0 or idx == len(string) - 1 or (not embedded and string[idx - 1] == "?") or (embedded and string[idx + 1 : idx + 1 + 1] == "?"):
                result += char
                idx += 1
                embedded = False
            else:
                raise ValueError(f"Unquoted question mark must appear at the beginning or end of the string, or in a leading or trailing sequence")

        result += "\\" + char
        idx += 1
        embedded = True

    return result


def unbind_value(value: str) -> str:
    """Binds the value for filesystem.
    Convert values to appropriate representations.

    Args:
        value (str): value to be binded

    Returns:
        str: binded value
    """

    if value == "*":
        return "ANY"
    elif value == "-":
        return "NA"
    else:
        return add_quoting(value)


def unbind(match: re.Match) -> dict[str, str]:
    """Create a dictionary with field-value pairs for formatted string representation.

    This function extracts the parts of a CPE 2.3 formatted string, and tries to validate
    them against logic provided in documentation.

    Args:
        match (re.Match): regex match of a formatted string

    Returns:
        dict[str, str]: dictionary with extracted parts from CPE formatted string
    """
    part, vendor, product, version, update, edition, language, sw_edition, target_sw, target_hw, other = match.groups()

    result = {
        "part": part,
        "vendor": vendor,
        "product": product,
        "version": version,
        "update": update,
        "edition": edition,
        "language": language,
        "sw_edition": sw_edition,
        "target_sw": target_sw,
        "target_hw": target_hw,
        "other": other,
    }

    for k, v in result.items():
        if v is None:
            raise ValueError(f"Empty value is not valid for '{k}'")

        result[k] = unbind_value(v)
    return result


def process_cpe_str(cpe_string: str) -> dict:
    """Processes the CPE string and extracts its parts.

    Args:
        cpe_string (str): The CPE string to be processed

    Returns:
        dict: A dictionary containing the extracted parts of the CPE formatted string
    """
    cpe_2_3_formatted_pattern = r"cpe:2.3:([aho]):([^:]*):([^:]*):([^:]*):([^:]*):([^:]*):([^:]*):([^:]*):([^:]*):([^:]*):([^:]*)"

    match = re.match(cpe_2_3_formatted_pattern, cpe_string)

    if not match:
        raise ValueError("The CPE string has an invalid format. Make sure it starts with 'cpe:2.3:', contains 11 components, and is properly quoted.")

    return unbind(match)


def main():
    if len(sys.argv) < 2:
        raise ValueError("No argument supplied")

    cpe_string = sys.argv[1]
    result = process_cpe_str(cpe_string)

    # This ensures that print is actually produced with a single backslash instead of two
    # which are produced by dict's __str__ and __repr__
    # For more info refer to '6.2.3.3.1 - 6.2.3.3.4' Examples
    print(json.dumps(result, indent=2).replace("\\\\", "\\"))


if __name__ == "__main__":
    main()
