#! /usr/bin/python3

import argparse
import os
from PIL import Image
from itertools import chain

MASK = 0b11
FILE_LEN_SIZE_IN_BYTES = 4
BYTE_SIZE = 8
BITS_PER_CHUNK = 2
HIDDEN_DATA_SIZE = 4  # bytes
CHUNKS_PER_BYTE = 4


def prepare_data_to_hide(file_name):
    def split_file_in_bytes():
        with open(file_name, 'rb') as file:
            for line in file:
                for byte in line:
                    yield byte

    def split_bytes_in_bit_chunks(bytes_seq):
        for byte in bytes_seq:
            for shift in range(0, BYTE_SIZE, BITS_PER_CHUNK):
                yield (byte & (MASK << shift)) >> shift

    def split_length_in_bit_chunks(length):
        return split_bytes_in_bit_chunks(length.to_bytes(4, byteorder='big'))

    return (split_length_in_bit_chunks(os.stat(file_name).st_size),
            split_bytes_in_bit_chunks(split_file_in_bytes()))


def build_byte(bit_chunks):
    result = 0
    for shift, chunk in zip(range(0, BYTE_SIZE, BITS_PER_CHUNK), bit_chunks):
        result |= chunk << shift

    return result


def hide_bit_chunk(target, bit_chunk):
    if bit_chunk is not None:
        target = (target & ~MASK) | bit_chunk

    return target


def extract_bit_chunk(target):
    return target & MASK


def hide(args):
    container = Image.open(args.file_container)
    x, y = container.size
    pixels = container.load()

    bit_chunks = chain(*prepare_data_to_hide(args.data))
    bit_chunk = None

    for j in range(y):
        for i in range(x):
            new_pixel_components = []
            for component in pixels[i, j]:
                bit_chunk = next(bit_chunks, None)
                new_pixel_components.append(hide_bit_chunk(component,
                                                           bit_chunk))

            pixels[i, j] = tuple(new_pixel_components)

            if bit_chunk is None:
                container.save(args.output_file)
                return


def show(args):
    container = Image.open(args.file_container)
    x, y = container.size
    pixels = container.load()

    bit_chunks = []
    data_bytes = []
    file_size = None
    for j in range(y):
        for i in range(x):
            for component in pixels[i, j]:
                bit_chunks.append(extract_bit_chunk(component))
                if len(bit_chunks) == CHUNKS_PER_BYTE:
                    data_bytes.append(build_byte(bit_chunks))
                    bit_chunks.clear()

                if file_size is None:
                    if len(data_bytes) == FILE_LEN_SIZE_IN_BYTES:
                        file_size = int.from_bytes(bytes(data_bytes),
                                                   byteorder='big',
                                                   signed=False)
                        data_bytes.clear()
                else:
                    if len(data_bytes) == file_size:
                        with open(args.output_file, 'wb') as file:
                            file.write(bytes(data_bytes))
                        return


def _parse_args():
    parser = argparse.ArgumentParser(description='LSB steganography algorithm.')
    parser.add_argument('--data', type=str, help='Data to hide')
    parser.add_argument('file_container', type=str, help='Input image')
    parser.add_argument('output_file', type=str, help='Output image')
    parser.add_argument('--hide', dest = 'hide', help = 'Hide data', action = 'store_true')
    parser.add_argument('--show', dest = 'hide',  help = 'Show data', action = 'store_false')
    parser.set_defaults(hide = True)

    return parser.parse_args()


def main():
    args = _parse_args()

    container = Image.open(args.file_container)
    x, y = container.size
    pixels = container.load()

    if args.hide:
        hide(args)

    else:
        show(args)


if __name__ == "__main__":
    main()
