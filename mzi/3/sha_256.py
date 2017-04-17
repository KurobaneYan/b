#! /usr/bin/python3

import struct

BITS_IN_BYTE = 8
LENGTH_FIELD_BITLEN = 64
BYTES_PER_CHUNK = 64
BITS_PER_CHUNK = BYTES_PER_CHUNK * BITS_IN_BYTE
BITS_PER_INT = 32
BINARY_RADIX = 2
INT_MASK = 0xffffffff

class SHA_256(object):
    def __init__(self, message):
        """
        Arguments:
            message {bytes} -- sequence of bytes
        """
        self._h0 = 0x6a09e667
        self._h1 = 0xbb67ae85
        self._h2 = 0x3c6ef372
        self._h3 = 0xa54ff53a
        self._h4 = 0x510e527f
        self._h5 = 0x9b05688c
        self._h6 = 0x1f83d9ab
        self._h7 = 0x5be0cd19

        length = SHA_256._to_bin(len(message) * BITS_IN_BYTE, LENGTH_FIELD_BITLEN)

        while len(message) > BYTES_PER_CHUNK:
            self._calculate(SHA_256._to_bin_string(message[:BYTES_PER_CHUNK]))
            message = message[BYTES_PER_CHUNK:]

        message = SHA_256._to_bin_string(message) + '1'
        message += '0' * ((BITS_PER_CHUNK - LENGTH_FIELD_BITLEN
                           - len(message) % BITS_PER_CHUNK)
                          % BITS_PER_CHUNK) + length
        for i in range(len(message) // BITS_PER_CHUNK):
            from_pos = i * BITS_PER_CHUNK
            self._calculate(message[from_pos:from_pos + BITS_PER_CHUNK])

    def _to_bin(number, string_bitlen):
        return bin(number)[2:].rjust(string_bitlen, '0')

    def _to_bin_string(string):
        return ''.join(SHA_256._to_bin(byte, BITS_IN_BYTE)
                       for byte in string)

    def ror(x, n):
        return (x >> n) | (x << (BITS_PER_INT - n))

    def _calculate(self, chunk):
        k = [0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5,
             0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
             0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3,
             0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
             0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc,
             0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
             0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7,
             0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
             0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13,
             0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
             0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3,
             0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
             0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5,
             0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
             0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208,
             0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2]

        w = []

        for i in range(len(chunk) // BITS_PER_INT):
            from_pos = i * BITS_PER_INT
            w.append(int(chunk[from_pos:from_pos + BITS_PER_INT], BINARY_RADIX))

        for i in range(len(w), len(k)):
            s0 = SHA_256.ror(w[i - 15], 7) ^ SHA_256.ror(w[i - 15], 18) ^ (w[i - 15] >> 3)
            s1 = SHA_256.ror(w[i - 2], 17) ^ SHA_256.ror(w[i - 2], 19) ^ (w[i - 2] >> 10)
            w.append((w[i - 16] + s0 + w[i - 7] + s1) & INT_MASK)

        a = self._h0
        b = self._h1
        c = self._h2
        d = self._h3
        e = self._h4
        f = self._h5
        g = self._h6
        h = self._h7

        for w_item, k_item in zip(w, k):
            s0 = SHA_256.ror(a, 2) ^ SHA_256.ror(a, 13) ^ SHA_256.ror(a, 22)
            maj = (a & b) ^ (a & c) ^ (b & c)
            t2 = s0 + maj
            s1 = SHA_256.ror(e, 6) ^ SHA_256.ror(e, 11) ^ SHA_256.ror(e, 25)
            ch = (e & f) ^ ((~ e) & g)
            t1 = h + s1 + ch + k_item + w_item

            h = g
            g = f
            f = e
            e = (d + t1) & INT_MASK
            d = c
            c = b
            b = a
            a = (t1 + t2) & INT_MASK

        self._h0 = (self._h0 + a) & INT_MASK
        self._h1 = (self._h1 + b) & INT_MASK
        self._h2 = (self._h2 + c) & INT_MASK
        self._h3 = (self._h3 + d) & INT_MASK
        self._h4 = (self._h4 + e) & INT_MASK
        self._h5 = (self._h5 + f) & INT_MASK
        self._h6 = (self._h6 + g) & INT_MASK
        self._h7 = (self._h7 + h) & INT_MASK

    def hexdigest(self):
        return self.digest().hex()

    def digest(self):
        return struct.pack(">8L", self._h0, self._h1, self._h2, self._h3,
                                  self._h4, self._h5, self._h6, self._h7)


if __name__ == '__main__':
    import hashlib
    import argparse

    def _parse_args():
        parser = argparse.ArgumentParser(description='SHA 256 hash algorithm.')
        parser.add_argument('input', type=str, help='Input file')

        return parser.parse_args()

    def main():
        args = _parse_args()
        with open(args.input, 'rb') as file:
            data = file.read()

        my_hash = SHA_256(data).hexdigest()
        lib_hash = hashlib.sha256(data).hexdigest()
        print(my_hash)
        print(lib_hash)
        if my_hash == lib_hash:
            print('My hash and hash from lib are equal')
        else:
            print('NOT equals')
    
    main()
