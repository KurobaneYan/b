def decrypt(string_data, string_key):
    return decode(_decrypt(encode(string_data),
                           encode(string_key)))


def encrypt(string_data, string_key):
    return decode(_encrypt(encode(string_data),
                           encode(string_key)))


def _decrypt(data, key):
    return _encrypt(data, key)


def _encrypt(data, key):
    encrypted_chunks = []

    for data_chunk in read_sequence_by_chunks(data, len(key)):
        encrypted_chunks.append(xor_bytes(key, data_chunk))

    return b''.join(encrypted_chunks)


def xor_bytes(key, data_chunk):
    return bytes(data_byte ^ key_byte
                 for data_byte, key_byte in zip(data_chunk, key))


def read_sequence_by_chunks(sequence, chunk_size):
    start, end = 0, chunk_size
    while start < len(sequence):
        yield sequence[start:end]
        start, end = end, end + chunk_size


def decode(bytes_seq):
    return bytes_seq.decode('utf-8', 'backslashreplace')


def encode(string):
    return string.encode('utf-8')
