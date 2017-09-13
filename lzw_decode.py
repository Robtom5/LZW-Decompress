#!/usr/bin/env python
#
# lzw_decode.py
#
# Author: Robert Thomas <robert.jst@icloud.com>
#
# Script coded using pep8 style guide


def decompress_LZW(input_file_path):

    # compressed = load_LZW(input_file_path)
    # Build the initial dictionary
    dict_size = 256
    dictionary = [chr(i) for i in range(dict_size)]
    generator = load_LZW(input_file_path)
    
    first = True

    # loop through all keys
    for chunk in generator:
        if first:
            result = w = chr(chunk.pop(0))
            first = False
        for k in chunk:
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
        i = 0
        n = 12
        while True:
            byte = file.read(1)
            if not byte:
                yield ([int(string[i:i+n], 2) for i in range(0, len(string), n)])
                break
            # pad with leading zeros
            string += ("{0:0>8b}".format(ord(byte)))
            i += 1
            if i >= 12:
                yield ([int(string[i:i+n], 2) for i in range(0, len(string), n)])
                string = ""
                i = 0

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
