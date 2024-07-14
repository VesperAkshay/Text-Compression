import argparse
import zlib

def compress_file(input_file, output_file):
    with open(input_file, 'rb') as f:
        data = f.read()
    compressed_data = zlib.compress(data, level=9)
    
    with open(output_file, 'wb') as f:
        f.write(compressed_data)

def decompress_file(input_file, output_file):
    with open(input_file, 'rb') as f:
        compressed_data = f.read()
    decompressed_data = zlib.decompress(compressed_data)
    
    with open(output_file, 'wb') as f:
        f.write(decompressed_data)

def main():
    parser = argparse.ArgumentParser(description='Deflate Compression and Decompression')
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
