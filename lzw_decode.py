#!/usr/bin/env python
#
# lzw_decode.py
#
# Author: Robert Thomas <robert.jst@icloud.com>
#
# Script coded using pep8 style guide


def decompress_LZW(input_file_path):

    compressed = load_LZW(input_file_path)
    # Build the initial dictionary
    dict_size = 256
    dictionary = [chr(i) for i in range(dict_size)]

    result = w = chr(compressed.pop(0))

    # loop through all keys
    for k in compressed:
        # Check for dictionary reset
        if (dict_size >= 4096):  # 2^12 entries
            dict_size = 256
            dictionary = [chr(i) for i in range(dict_size)]
        if k > dict_size:
            raise ValueError('Invalid key, k: %s' % k)
        elif k == dict_size:
            entry = w + w[0]
        else:
            entry = dictionary[k]

        result += entry
        dictionary.append(w + entry[0])
        dict_size += 1
        w = entry

    return result


def load_LZW(input_file_path):
    with open(input_file_path, mode="rb") as file:
        string = ""
        compressed = []
        while True:
            byte = file.read(1)
            if not byte:
                break
            # pad with leading zeros
            string += ("{0:0>8b}".format(ord(byte)))
    # Split into list of 12 bit sections
    n = 12
    compressed = ([int(string[i:i+n], 2) for i in range(0, len(string), n)])
    return compressed

if __name__ == "__main__":
    import argparse
    # Create argument parser for input and output file paths
    parser = argparse.ArgumentParser(description="Decompress LZW")
    parser.add_argument('-f', '--file', dest='input_file_path')
    parser.add_argument('-o', '--output', dest='output_file_path',
                        default='output.txt')
    args = parser.parse_args()
    with open(args.output_file_path, "w") as out_file:
        out_file.write(decompress_LZW(args.input_file_path))
