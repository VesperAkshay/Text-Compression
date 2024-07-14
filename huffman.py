import heapq
import pickle
import argparse
from collections import Counter, defaultdict

class HuffmanNode:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq

def build_huffman_tree(text):
    frequency = Counter(text)
    heap = [HuffmanNode(char, freq) for char, freq in frequency.items()]
    heapq.heapify(heap)

    while len(heap) > 1:
        node1 = heapq.heappop(heap)
        node2 = heapq.heappop(heap)
        merged = HuffmanNode(None, node1.freq + node2.freq)
        merged.left = node1
        merged.right = node2
        heapq.heappush(heap, merged)

    return heap[0]

def build_codes(node, prefix="", codebook=None):
    if codebook is None:
        codebook = {}
    if node is not None:
        if node.char is not None:
            codebook[node.char] = prefix
        build_codes(node.left, prefix + "0", codebook)
        build_codes(node.right, prefix + "1", codebook)
    return codebook

def huffman_encode(text):
    root = build_huffman_tree(text)
    huffman_codes = build_codes(root)
    encoded_text = ''.join(huffman_codes[char] for char in text)
    return encoded_text, huffman_codes

def huffman_decode(encoded_text, huffman_codes):
    reverse_codebook = {v: k for k, v in huffman_codes.items()}
    current_code = ""
    decoded_text = []

    for bit in encoded_text:
        current_code += bit
        if current_code in reverse_codebook:
            decoded_text.append(reverse_codebook[current_code])
            current_code = ""

    return ''.join(decoded_text)

def compress_file(input_file, output_file):
    with open(input_file, 'r') as f:
        text = f.read()
    encoded_text, huffman_codes = huffman_encode(text)

    # Use a more compact representation for the encoded text
    encoded_text_bits = ''.join(encoded_text)
    extra_padding = 8 - len(encoded_text_bits) % 8
    encoded_text_bits = f'{extra_padding:08b}' + encoded_text_bits + '0' * extra_padding

    b = bytearray()
    for i in range(0, len(encoded_text_bits), 8):
        byte = encoded_text_bits[i:i + 8]
        b.append(int(byte, 2))

    with open(output_file, 'wb') as f:
        pickle.dump((b, huffman_codes), f)

def decompress_file(input_file, output_file):
    with open(input_file, 'rb') as f:
        b, huffman_codes = pickle.load(f)
    
    encoded_text_bits = ''.join(f'{byte:08b}' for byte in b)
    extra_padding = int(encoded_text_bits[:8], 2)
    encoded_text_bits = encoded_text_bits[8:-extra_padding]

    decoded_text = huffman_decode(encoded_text_bits, huffman_codes)
    
    with open(output_file, 'w') as f:
        f.write(decoded_text)

def main():
    parser = argparse.ArgumentParser(description='Huffman Compression and Decompression')
    parser.add_argument('command', choices=['compress', 'decompress'], help='compress or decompress a file')
    parser.add_argument('input_file', help='input file path')
    parser.add_argument('output_file', help='output file path')
    
    args = parser.parse_args()
    
    if args.command == 'compress':
        compress_file(args.input_file, args.output_file)
        print(f"File '{args.input_file}' compressed to '{args.output_file}'.")
    elif args.command == 'decompress':
        decompress_file(args.input_file, args.output_file)
        print(f"File '{args.input_file}' decompressed to '{args.output_file}'.")
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
