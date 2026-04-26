#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__  = 'Hardik'
__version__ = '5.0'
__email__   = 'contact@hardik.com'
__github__  = 'https://github.com/Hardikvats713/cryptobreak'

import os
import re
import sys
import time
import hashlib
import platform
import json
import argparse
from colorama import init
from termcolor import colored
from pathlib import Path

from src.base_chain import DecodeBase
from src.messages import push_error, print_line_separator

# ── Advanced: Hash identification patterns ──────────────────────────────────
HASH_PATTERNS = {
    'MD5':        (r'^[a-fA-F0-9]{32}$', 128),
    'SHA-1':      (r'^[a-fA-F0-9]{40}$', 160),
    'SHA-224':    (r'^[a-fA-F0-9]{56}$', 224),
    'SHA-256':    (r'^[a-fA-F0-9]{64}$', 256),
    'SHA-384':    (r'^[a-fA-F0-9]{96}$', 384),
    'SHA-512':    (r'^[a-fA-F0-9]{128}$', 512),
    'SHA3-256':   (r'^[a-fA-F0-9]{64}$', 256),
    'SHA3-512':   (r'^[a-fA-F0-9]{128}$', 512),
    'NTLM':      (r'^[a-fA-F0-9]{32}$', 128),
    'CRC32':     (r'^[a-fA-F0-9]{8}$', 32),
    'Bcrypt':    (r'^\$2[aby]?\$.{56}$', None),
}


class CryptoBreak:
    def __init__(self, output=None, magic_mode_call=False, quit_after_fail=True,
                 json_output=False, verbose=False):
        self.output = output
        # initial bools
        self.api_call = False
        self.magic_mode_call = magic_mode_call
        self.image_mode_call = False
        self.quit_after_fail = quit_after_fail
        # advanced options
        self.json_output = json_output
        self.verbose = verbose
        self.decode_log = []  # stores all decode results for JSON export

    # ── Advanced: ROT13 decode ──────────────────────────────────────────────
    @staticmethod
    def rot13_decode(text):
        """Decode ROT13 encoded text."""
        result = []
        for char in text:
            if 'a' <= char <= 'z':
                result.append(chr((ord(char) - ord('a') + 13) % 26 + ord('a')))
            elif 'A' <= char <= 'Z':
                result.append(chr((ord(char) - ord('A') + 13) % 26 + ord('A')))
            else:
                result.append(char)
        return ''.join(result)

    # ── Advanced: ROT47 decode ──────────────────────────────────────────────
    @staticmethod
    def rot47_decode(text):
        """Decode ROT47 encoded text."""
        result = []
        for char in text:
            ascii_val = ord(char)
            if 33 <= ascii_val <= 126:
                result.append(chr(33 + ((ascii_val - 33 + 47) % 94)))
            else:
                result.append(char)
        return ''.join(result)

    # ── Advanced: Caesar cipher brute-force ──────────────────────────────────
    @staticmethod
    def caesar_bruteforce(text):
        """Brute-force all 25 Caesar cipher shifts and return results."""
        results = []
        for shift in range(1, 26):
            decoded = []
            for char in text:
                if 'a' <= char <= 'z':
                    decoded.append(chr((ord(char) - ord('a') + shift) % 26 + ord('a')))
                elif 'A' <= char <= 'Z':
                    decoded.append(chr((ord(char) - ord('A') + shift) % 26 + ord('A')))
                else:
                    decoded.append(char)
            results.append((shift, ''.join(decoded)))
        return results

    # ── Advanced: Hash identification ────────────────────────────────────────
    @staticmethod
    def identify_hash(text):
        """Identify possible hash types based on length and pattern."""
        text = text.strip()
        matches = []
        for hash_name, (pattern, bits) in HASH_PATTERNS.items():
            if re.match(pattern, text):
                matches.append({
                    'type': hash_name,
                    'bits': bits,
                    'confidence': 'High' if bits else 'Medium'
                })
        return matches

    # ── Advanced: Encoding confidence score ──────────────────────────────────
    @staticmethod
    def confidence_score(decoded_string):
        """Calculate confidence score based on printable ASCII ratio."""
        if not decoded_string:
            return 0.0
        printable = sum(1 for c in decoded_string if 32 <= ord(c) <= 126)
        return round((printable / len(decoded_string)) * 100, 2)

    # main decode function
    def decode_base(self, encoded_base):
        if len(encoded_base) > 3:
            # execute decode chain
            encoding_type, results = DecodeBase(
                encoded_base,
                api_call = self.api_call,
                image_mode = self.image_mode_call
            ).decode()

            if not results and not self.api_call:
                if not self.image_mode_call:
                    push_error('Not a valid encoding.')

                if self.quit_after_fail:
                    quit()

            # print/return the results
            for x in range(len(results)):          
                if not self.api_call:
                    confidence = self.confidence_score(results[x])

                    print(
                        colored('\n[-] The Encoding Scheme Is ', 'blue') +
                        colored(encoding_type[x], 'green')
                    )

                    if self.verbose:
                        print(
                            colored('    ├── Confidence: ', 'cyan') +
                            colored('{}%'.format(confidence), 'yellow')
                        )
                        print(
                            colored('    └── Length: ', 'cyan') +
                            colored('{} chars'.format(len(results[x])), 'yellow')
                        )

                    # log for JSON export
                    self.decode_log.append({
                        'input': encoded_base,
                        'decoded': results[x],
                        'scheme': encoding_type[x],
                        'confidence': confidence
                    })

                    # generating the wordlist/output file with the decoded base
                    if self.output != None:
                        open(self.output, 'a').write(results[x]+'\n')
                else:
                    return results[x].strip(), encoding_type[x]

            if self.image_mode_call and results:
                print_line_separator()
        else:
            push_error("Found no valid base encoded strings.")


    def decode_from_file(self, file):
        """
        `decode_from_file()` fetches the set of base encodings from the input file
        and passes it to 'decode_base()' function to decode it all
        """

        print(colored('[-] Decoding Base Data From ', 'cyan') + colored(file, 'yellow'))

        # check whether file exists
        if not Path(file).is_file():
            push_error('File does not exist.')
            quit()

        total = 0
        success = 0
        start_time = time.time()

        with open(file) as input_file:
            # reading each line from the file
            for line in input_file:
                # checking if the line/base is not empty
                if len(line) > 1:
                    total += 1
                    line = line.strip()
                    print(colored('\n[-] Encoded Base: ', 'yellow')+str(line))
                    
                    if self.magic_mode_call:
                        self.magic_mode(line)
                    else:
                        self.decode_base(line)

                    if self.decode_log:
                        success += 1

                    print_line_separator()

        # ── Advanced: Batch statistics ───────────────────────────────────────
        elapsed = time.time() - start_time
        print(colored('\n╔══════════════════════════════════════╗', 'cyan'))
        print(colored('║       BATCH DECODE STATISTICS        ║', 'cyan'))
        print(colored('╠══════════════════════════════════════╣', 'cyan'))
        print(colored('║  Total Entries:  ', 'cyan') + colored('{:<19}'.format(total), 'yellow') + colored('║', 'cyan'))
        print(colored('║  Decoded:        ', 'cyan') + colored('{:<19}'.format(success), 'green') + colored('║', 'cyan'))
        print(colored('║  Failed:         ', 'cyan') + colored('{:<19}'.format(total - success), 'red') + colored('║', 'cyan'))
        print(colored('║  Time Elapsed:   ', 'cyan') + colored('{:<19}'.format(str(elapsed)[:6] + 's'), 'yellow') + colored('║', 'cyan'))
        print(colored('╚══════════════════════════════════════╝\n', 'cyan'))


    def decode(self, encoded_base):
        """
        API FUNCTION
        ------------
        the `decode()` function returns a tuple
        with the structure:
            ('DECODED_STRING', 'ENCODING SCHEME')
            For example:
                >> from cryptobreak import CryptoBreak
                >> CryptoBreak().decode('c3BhZ2hldHRp')
                ('spaghetti', 'Base64')
            ie:
                result[0] is the decoded string
                result[1] is the encoding scheme
        """
        self.api_call = True

        # api calls returns a tuple with the decoded base and the encoding scheme
        return self.decode_base(encoded_base)


    def magic_mode(self, encoded_base):
        """
        `magic_mode()` tries to decode multi-encoded bases of any pattern
        """
        iteration = 0
        result = None
        encoding_pattern = []
        start_time = time.time()

        while True:
            if self.decode(encoded_base) is not None:
                iteration += 1
                result = self.decode(encoded_base)
                decoded_string = result[0]
                encoding_scheme = result[1]
                encoding_pattern.append(encoding_scheme)

                print(colored('\n[-] Iteration: ', 'green')+colored(iteration, 'blue'))
                print(colored('\n[-] Heuristic Found Encoding To Be: ', 'yellow')+colored(encoding_scheme, 'green'))
                print(colored('\n[-] Decoding as {}: '.format(encoding_scheme), 'blue')+colored(decoded_string, 'green'))
                print(colored('\n{{<<', 'red')+colored('='*70, 'yellow')+colored('>>}}', 'red'))
                
                # setting the encoded bases and the current result for the next iteration
                encoded_base = decoded_string
            else:
                break

        if result is not None:
            end_time = time.time()

            print(colored('\n[-] Total Iterations: ', 'green')+colored(iteration, 'blue'))

            # show the encoding pattern in order and comma-seperated
            pattern = ' -> '.join(map(str, encoding_pattern))
            print(colored('\n[-] Encoding Pattern: ', 'green')+colored(pattern, 'blue'))

            # ── Advanced: Visual encoding chain ──────────────────────────────
            print(colored('\n[-] Encoding Chain: ', 'green'))
            for idx, enc in enumerate(encoding_pattern):
                prefix = '    └── ' if idx == len(encoding_pattern) - 1 else '    ├── '
                print(colored(prefix, 'yellow') + colored('Layer {}: '.format(idx+1), 'cyan') + colored(enc, 'magenta'))

            print(
                colored('\n[-] Magic Decode Finished With Result: ', 'green') +
                colored(decoded_string, 'yellow', attrs=['bold'])
            )

            # generating the wordlist/output file with the decoded base
            if self.output != None:
                open(self.output, 'a').write(decoded_string+'\n')

            completion_time = str(end_time-start_time)[:6]

            print(
                colored('\n[-] Finished in ', 'green') +
                colored(completion_time, 'cyan', attrs=['bold']) +
                colored(' seconds\n', 'green')
            )
        else:
            quit(colored('\n[!] Not a valid encoding.\n', 'red'))


    def decode_from_image(self, image, mode):
        """
        `decode_from_image()` AKA "lame_steganography_challenge_solving_automated()" has two modes:
            - OCR Detection Mode: dectects base encodings in images
            - EXIF Data Mode: detects base encodings in an image's EXIF data
        """
        self.image_mode_call = True

        # check whether file exists
        if not Path(image).is_file():
            push_error('File does not exist.')
            quit()

        if mode == 'exif':
            import exifread

            read_image = open(image, 'rb')
            exif_tags = exifread.process_file(read_image)

            for tag in exif_tags:
                split_tag = str(exif_tags[tag]).split(' ')

                for base in split_tag:
                    if len(base) < 3 or '\\x' in base: continue

                    for base in base.splitlines():
                        if self.magic_mode_call:
                            self.magic_mode(base)
                        else:
                            self.decode_base(base)
        elif mode == 'ocr':
            import cv2, pytesseract

            # import tesseract for windows
            if platform.system() == 'Windows':
                load_config = json.loads(open('config.json', 'r').read())

                if len(load_config) > 0:
                    # load 32/64 bit executables
                    if sys.maxsize > 2**32:
                        # 64 bit
                        tesseract_path = load_config['tesseract_path']['32bit']
                    else:
                        # 32 bit
                        tesseract_path = load_config['tesseract_path']['64bit']

                # raw string to treat `\` as a literal character
                pytesseract.pytesseract.tesseract_cmd = r'{}'.format(tesseract_path)

            read_image = cv2.imread(image)
            get_text = pytesseract.image_to_string(read_image)
            strings_from_img = str(get_text).replace(' ', '')

            # cleaning the detected string with valid base chars for accurary
            base = re.sub('[^A-Za-z0-9+/=@]', '', strings_from_img)

            if self.magic_mode_call: self.magic_mode(base)
            else: self.decode_base(base)


    # ── Advanced: Export results to JSON ──────────────────────────────────────
    def export_json(self, filename):
        """Export all decode results to a JSON file."""
        with open(filename, 'w') as f:
            json.dump({
                'tool': 'CryptoBreak',
                'version': __version__,
                'author': __author__,
                'results': self.decode_log,
                'total_decoded': len(self.decode_log)
            }, f, indent=4)
        print(
            colored('\n[+] JSON Report Exported: ', 'green') +
            colored(filename, 'yellow')
        )


    # ── Advanced: Hash identification mode ────────────────────────────────────
    def hash_identify(self, hash_string):
        """Identify a hash type from its string representation."""
        matches = self.identify_hash(hash_string)
        if matches:
            print(colored('\n╔══════════════════════════════════════╗', 'magenta'))
            print(colored('║       HASH IDENTIFICATION            ║', 'magenta'))
            print(colored('╠══════════════════════════════════════╣', 'magenta'))
            for m in matches:
                bits_str = '{}bit'.format(m['bits']) if m['bits'] else 'N/A'
                print(
                    colored('║  ', 'magenta') +
                    colored('{:<12}'.format(m['type']), 'yellow') +
                    colored('{:<10}'.format(bits_str), 'cyan') +
                    colored('{:<14}'.format(m['confidence']), 'green') +
                    colored('║', 'magenta')
                )
            print(colored('╚══════════════════════════════════════╝\n', 'magenta'))
        else:
            print(colored('\n[!] No known hash pattern matched.\n', 'red'))


    # ── Advanced: Caesar cipher mode ──────────────────────────────────────────
    def caesar_mode(self, text):
        """Brute-force Caesar cipher shifts and display all 25 results."""
        results = self.caesar_bruteforce(text)
        print(colored('\n╔══════════════════════════════════════════════════════════╗', 'yellow'))
        print(colored('║            CAESAR CIPHER BRUTE-FORCE                    ║', 'yellow'))
        print(colored('╠══════════════════════════════════════════════════════════╣', 'yellow'))
        for shift, decoded in results:
            print(
                colored('║  Shift {:>2}: '.format(shift), 'yellow') +
                colored('{:<45}'.format(decoded[:45]), 'green') +
                colored('║', 'yellow')
            )
        print(colored('╚══════════════════════════════════════════════════════════╝\n', 'yellow'))

    # ── Advanced: ROT decode mode ─────────────────────────────────────────────
    def rot_decode(self, text):
        """Decode ROT13 and ROT47 and display results."""
        rot13_result = self.rot13_decode(text)
        rot47_result = self.rot47_decode(text)

        print(colored('\n╔══════════════════════════════════════════════════════════╗', 'green'))
        print(colored('║              ROT CIPHER DECODING                        ║', 'green'))
        print(colored('╠══════════════════════════════════════════════════════════╣', 'green'))
        print(
            colored('║  ROT13: ', 'green') +
            colored('{:<47}'.format(rot13_result[:47]), 'yellow') +
            colored('║', 'green')
        )
        print(
            colored('║  ROT47: ', 'green') +
            colored('{:<47}'.format(rot47_result[:47]), 'yellow') +
            colored('║', 'green')
        )
        print(colored('╚══════════════════════════════════════════════════════════╝\n', 'green'))


# print a banner to look cool
def banner():
    banner = '''
 ██████╗██████╗ ██╗   ██╗██████╗ ████████╗ ██████╗ ██████╗ ██████╗ ███████╗ █████╗ ██╗  ██╗
██╔════╝██╔══██╗╚██╗ ██╔╝██╔══██╗╚══██╔══╝██╔═══██╗██╔══██╗██╔══██╗██╔════╝██╔══██╗██║ ██╔╝
██║     ██████╔╝ ╚████╔╝ ██████╔╝   ██║   ██║   ██║██████╔╝██████╔╝█████╗  ███████║█████╔╝ 
██║     ██╔══██╗  ╚██╔╝  ██╔═══╝    ██║   ██║   ██║██╔══██╗██╔══██╗██╔══╝  ██╔══██║██╔═██╗ 
╚██████╗██║  ██║   ██║   ██║        ██║   ╚██████╔╝██████╔╝██║  ██║███████╗██║  ██║██║  ██╗
 ╚═════╝╚═╝  ╚═╝   ╚═╝   ╚═╝        ╚═╝    ╚═════╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝
    '''
    print(colored(banner, 'red'))
    print(colored('\t\t   [ CryptoBreak v{} by {} ]'.format(__version__, __author__), 'cyan'))
    print(colored('\t\tpython cryptobreak.py -h [FOR HELP]\n', 'green'))

def main():
    banner()

    # setting up argparse module to accept arguments
    parser = argparse.ArgumentParser(
        description='CryptoBreak v{} - Advanced Base Encoding Decoder & Crypto Toolkit by {}'.format(
            __version__, __author__
        )
    )
    parser.add_argument('-b', '--base', help='Decode a single encoded base from argument.')
    parser.add_argument('-f', '--file', help='Decode multiple encoded bases from a file.')
    parser.add_argument('-m', '--magic', help='Decode multi-encoded bases in one shot.', action='store_true')
    parser.add_argument('-i', '--image', help='Decode base encodings from image with OCR detection or EXIF data.')
    parser.add_argument('-c', '--ocr', help='OCR detection mode.', action='store_true')
    parser.add_argument('-e', '--exif', help='EXIF data detection mode. (default)', action='store_true')
    parser.add_argument('-o', '--output', help='Generate a wordlist/output with the decoded bases, enter filename as the value.')

    # ── Advanced arguments ───────────────────────────────────────────────────
    parser.add_argument('--rot', help='Decode ROT13 and ROT47 from argument.')
    parser.add_argument('--caesar', help='Brute-force Caesar cipher from argument.')
    parser.add_argument('--hash-id', help='Identify hash type from argument.')
    parser.add_argument('--json', help='Export results to a JSON file.', metavar='FILENAME')
    parser.add_argument('-v', '--verbose', help='Show confidence scores and extra details.', action='store_true')

    args = parser.parse_args()

    if args.output:
        print(
            colored('\n[>] ', 'yellow') +
            colored('Enabled Wordlist Generator Mode :: ', 'green') +
            colored(args.output+'\n', 'blue')
        )

    # ── Advanced: Hash identification mode ────────────────────────────────
    if args.hash_id:
        CryptoBreak(verbose=args.verbose).hash_identify(str(args.hash_id))
        return

    # ── Advanced: ROT decode mode ─────────────────────────────────────────
    if args.rot:
        CryptoBreak(verbose=args.verbose).rot_decode(str(args.rot))
        return

    # ── Advanced: Caesar brute-force mode ─────────────────────────────────
    if args.caesar:
        CryptoBreak(verbose=args.verbose).caesar_mode(str(args.caesar))
        return

    """
    decodes base encodings from file if argument is given
    else it accepts a single encoded base from user
    """
    cb = CryptoBreak(output=args.output, verbose=args.verbose)

    if args.file:
        if args.magic:
            CryptoBreak(
                output=args.output,
                magic_mode_call=True,
                verbose=args.verbose
            ).decode_from_file(str(args.file))
        else:
            CryptoBreak(output=args.output, verbose=args.verbose).decode_from_file(str(args.file))

    elif args.base:
        print(colored('[-] Encoded Base: ', 'yellow')+colored(str(args.base), 'red'))

        if args.magic:
            cb.magic_mode(str(args.base))
        else:
            cb.decode_base(str(args.base))

    elif args.image:
        print(colored('[-] Input Image: ', 'yellow')+colored(str(args.image), 'red'))

        if args.ocr:
            mode = 'ocr'
        elif args.exif:
            mode = 'exif'
        # default
        else:
            mode = 'exif'

        if args.magic:
            CryptoBreak(
                output=args.output, magic_mode_call=True, quit_after_fail=False,
                verbose=args.verbose
            ).decode_from_image(str(args.image), mode)
        else:
            CryptoBreak(
                quit_after_fail=False,
                verbose=args.verbose
            ).decode_from_image(str(args.image), mode)

    else:
        if sys.version_info >= (3, 0):
            encoded_base = input(colored('[>] Enter Encoded Base: ', 'yellow'))
        else:
            encoded_base = raw_input(colored('[>] Enter Encoded Base: ', 'yellow'))

        if args.magic:
            cb.magic_mode(encoded_base)
        else:
            cb.decode_base(encoded_base)

    # ── Advanced: JSON export ─────────────────────────────────────────────
    if args.json:
        cb.export_json(str(args.json))

    if args.output:
        print(
            colored('\n[-] Output Generated Successfully > ', 'green') +
            colored(args.output+'\n', 'yellow')
        )

if __name__ == '__main__':
    init()
    main()
