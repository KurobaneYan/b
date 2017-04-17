#! /usr/bin/python3

import argparse
from sha_256 import SHA_256


def xor_bytes(key, data_chunk):
    return bytes(data_byte ^ key_byte
                 for data_byte, key_byte in zip(data_chunk, key))


def read_input_by_chunks(source_file, chunk_size):
    input_bytes = source_file.read(chunk_size)
    while input_bytes:
        yield input_bytes
        input_bytes = source_file.read(chunk_size)


def read_sequence_by_chunks(sequence, chunk_size):
    chunks_count = len(sequence) // chunk_size
    for i in range(chunks_count):
        from_pos = i * chunk_size
        yield sequence[from_pos:from_pos + chunk_size]

    try:
        yield sequence[chunks_count * chunk_size:]
    except:
        pass


def parse_args():
    parser = argparse.ArgumentParser(description='Message auth code.')
    parser.add_argument('input_file', type=str)
    parser.add_argument('key', type=str)
    parser.add_argument('--output_file', type=str)

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    key = args.key.encode('utf-8')
    HASH_LEN = 32

    with open(args.input_file, 'rb') as input_file:
        data = input_file.read()

    if args.output_file:
        with open(args.output_file, 'wb') as output_file:
            output_file.write(data)
            for data_chunk in read_sequence_by_chunks(SHA_256(data).digest(), len(key)):
                output_file.write(xor_bytes(key, data_chunk))
    else:
        split_pos = len(data) - HASH_LEN
        message, encrypted_hash = data[:split_pos], data[split_pos:]

        message_hash = SHA_256(message).digest()
        decrypted_hash = b''.join((xor_bytes(key, chunk) for chunk
                                   in read_sequence_by_chunks(encrypted_hash, len(key))))

        print('Authenticated' if message_hash == decrypted_hash else 'Invalid message')
