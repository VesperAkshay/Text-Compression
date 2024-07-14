import argparse
import os
import pickle
from collections import Counter

class rANS:
    def __init__(self, precision=16):
        self.precision = precision
        self.base = 1 << precision
        self.mask = self.base - 1

    def build_cdf(self, freqs):
        total = sum(freqs.values())
        cdf = {}
        cumulative = 0
        for symbol, freq in freqs.items():
            cdf[symbol] = (cumulative, freq)
            cumulative += freq
        return cdf, total

    def compress(self, data):
        freqs = Counter(data)
        cdf, total = self.build_cdf(freqs)
        state = self.base

        compressed_data = []
        for symbol in reversed(data):
            low, freq = cdf[symbol]
            state = ((state // freq) << self.precision) + (state % freq) + low
            while state > self.mask:
                compressed_data.append(state & 0xFF)
                state >>= 8

        compressed_data.append(state)
        compressed_data.reverse()
        return compressed_data, freqs

    def decompress(self, compressed_data, freqs, original_size):
        cdf, total = self.build_cdf(freqs)
        state = compressed_data[0]
        pos = 1

        decompressed_data = []
        for _ in range(original_size):
            for symbol, (low, freq) in cdf.items():
                if low <= state % self.base < low + freq:
                    decompressed_data.append(symbol)
                    state = (state // self.base) * freq + (state % self.base) - low
                    break
            while state < self.base and pos < len(compressed_data):
                state = (state << 8) + compressed_data[pos]
                pos += 1

        decompressed_data.reverse()
        return decompressed_data

def compress_file(input_file, output_file):
    with open(input_file, 'rb') as f:
        data = f.read()
    compressor = rANS()
    compressed_data, freqs = compressor.compress(data)

    with open(output_file, 'wb') as f:
        pickle.dump((compressed_data, freqs, len(data)), f)

def decompress_file(input_file, output_file):
    with open(input_file, 'rb') as f:
        compressed_data, freqs, original_size = pickle.load(f)
    decompressor = rANS()
    decompressed_data = decompressor.decompress(compressed_data, freqs, original_size)

    with open(output_file, 'wb') as f:
        f.write(bytearray(decompressed_data))

parser = argparse.ArgumentParser(description='rANS Compression and Decompression')
parser.add_argument('action', choices={'compress', 'decompress'}, help='Define action to be performed.')
parser.add_argument('-i', action='store', dest='input', required=True, help='Input file.')
parser.add_argument('-o', action='store', dest='output', required=True, help='Output file.')
args = parser.parse_args()

ABSOLUTE_PATH = os.getcwd()

if args.action == 'compress':
    compress_file(ABSOLUTE_PATH + "/" + args.input, ABSOLUTE_PATH + "/" + args.output)
    print(f"File '{args.input}' compressed to '{args.output}'.")
elif args.action == 'decompress':
    decompress_file(ABSOLUTE_PATH + "/" + args.input, ABSOLUTE_PATH + "/" + args.output)
    print(f"File '{args.input}' decompressed to '{args.output}'.")
else:
    parser.print_help()
