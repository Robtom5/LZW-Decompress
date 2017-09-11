#!/usr/bin/env python
#
# lzw_decode.py
#
# Author: Robert Thomas <robert.jst@icloud.com>
#
# Script coded using pep8 style guide
import numpy as np



with open("./LzwInputData/compressedfile1.z", mode="rb") as file:
    # test = file.read()
    # print (test)
    # print np.fromfile("./LzwInputData/compressedfile1.z", dtype=np.uint8)
#     # print bytearray(file.read())
    string = ""
    compressed=[]
    while True:
        byte = file.read(1)
        if not byte:
            break
        string += ("{0:0>8b}".format(ord(byte)))
        # string += str(ord(byte))
        compressed.append(byte)
n=12
compressed= ([int(string[i:i+n],2) for i in range(0, len(string), n)])


def decompress(compressed):
    """Decompress a list of output ks to a string."""
    
    # Build the dictionary.
    dict_size = 256
    dictionary = {i: chr(i) for i in range(dict_size)}
    test = [chr(i) for i in range(dict_size)]
    print(test)
    # in Python 3: dictionary = {i: chr(i) for i in range(dict_size)}
 
    # use StringIO, otherwise this becomes O(N^2)
    # due to string concatenation in a loop
    
    w = result = chr(compressed.pop(0))
    result = w
    for k in compressed:
        if k in dictionary:
            entry = dictionary[k]
        elif k == dict_size:
            entry = w + w[0]
        else:
            raise ValueError('Bad compressed k: %s' % k)
        result += entry
 
        # Add w+entry[0] to the dictionary.
        dictionary[dict_size] = w + entry[0]
        dict_size += 1
 

        w = entry
    # print dictionary
    return result
with open("results.txt", mode="w") as file:
    file.write(decompress(compressed))