#!/usr/bin/env python
#
# lzw_decode.py
#
# Author: Robert Thomas <robert.jst@icloud.com>
#
# Script coded using pep8 style guide


def decompress_LZW(input_file_path):
    # Function based and adapted from code available at:
    #    https://rosettacode.org/wiki/LZW_compression

    # Build the initial dictionary
    dict_size = 256
    dictionary = [chr(i) for i in range(dict_size)]
    generator = load_LZW(input_file_path)

    first = True

    # loop through all keys
    for chunk in generator:
        # Reset the output string
        result = ""
        if first:
            # If at the start of the generator, initialise results
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
        yield result


def load_LZW(input_file_path):
    with open(input_file_path, mode="rb") as file:
        # Initialise empty string for outputs
        string = ""
        i = 0
        n = 12
        while True:
            byte = file.read(1)
            if not byte:
                yield ([int(string[i:i+n], 2)
                        for i in range(0, len(string), n)])
                break
            # pad with leading zeros
            string += ("{0:0>8b}".format(ord(byte)))
            i += 1
            if i >= 12:
                yield ([int(string[i:i+n], 2)
                        for i in range(0, len(string), n)])
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
        for decompressed in decompress_LZW(args.input_file_path):
            out_file.write(decompressed)
