#!/usr/bin/python
# -*- coding: utf-8 -*-

import argparse, sys

parser = argparse.ArgumentParser()
parser.add_argument('-k', '--key', default = '50m3 5tr0ng K3y', help = 'key')
parser.add_argument('-i', '--input_file', help = 'input file')
parser.add_argument('-o', '--output_file', default = 'a.out', help = 'output file')
parser.add_argument('-e', '--encrypt', dest = 'action', help = 'encrypt file', action = 'store_true')
parser.add_argument('-d', '--decrypt', dest = 'action',  help = 'decrypt file', action = 'store_false')
parser.set_defaults(action = True)
args = parser.parse_args()

if (args.input_file is None):
    sys.exit("You must enter input file name")

key = args.key.encode('utf-8')

with open(args.input_file, 'rb') as input_file:
    data = bytearray(input_file.read())

if args.action:
    new_data = data[3:]
    new_data.extend(data[:3])
    for i in range(len(data)):
        new_data[i] ^= key[i%len(key)]
else:
    for i in range(len(data)):
        data[i] ^= key[i%len(key)]
    new_data = data[-3:]
    new_data.extend(data[:-3])

with open(args.output_file, 'wb') as output_file:
    output_file.write(new_data)

print('resault in file', args.output_file)
