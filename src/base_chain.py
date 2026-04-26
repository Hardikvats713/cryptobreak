import anybase32
import base36
import base58
import base62
import base64
import base91
import src.base92 as base92
import pybase100

from termcolor import colored

class DecodeBase:
    def __init__(self, encoded_base, api_call=False, image_mode=False):
        self.encoded_base = encoded_base
        self.b32_once = False
        self.b64_once = False
        self.b64_url = False
        self.encoding_type = []
        self.results = []

        # state conditions
        self.api_call = api_call
        self.image_mode_call = image_mode

    def decode(self):
        self.decode_base()
        return (
            self.encoding_type,
            self.results
        )

    def contains_replacement_char(self, res):
        """
        `contains_replacement_char()` checks whether the decoded base
        contains an unknown unicode, ie: invalid character.
        these are replaced with 'replacement character',
        which is '�' and 'U+FFFD' in unicode and
        also checks for unicode chars after `127`.
        """
        if u'\ufffd' in res: return True
        else:
            count = 0
            for char in res:
                if ord(char) > 127: count += 1
            return True if count > 0 else False

    def process_decode(self, decode_string, scheme):
        """
        `process_decode()` stores the result if the encoding is valid
        after checks from `contains_replacement_char()` and
        prints the output if it isn't an API call
        """
        encoding_type = self.encoding_type
        results = self.results

        if len(decode_string) < 3: return
        if not self.contains_replacement_char(decode_string):
            # don't repeat `base64url` when `base64` has already passed and it's not a URL
            if scheme == 'Base64' and '://' not in decode_string:
                self.b64_once = True
                
            if self.b64_once and (scheme == 'Base64URL'):
                return
            
            # append results to the respective lists
            encoding_type.append(scheme)
            results.append(decode_string)

            if not self.api_call:
                if self.image_mode_call:
                    print(
                        colored('\n[-] Attempting Base: ', 'yellow') +
                        colored(self.encoded_base, 'red')
                    )

                print(
                    colored('\n[>] Decoding as {}: '.format(scheme), 'blue') +
                    colored(decode_string, 'green')
                )

    def decode_base(self):
        encoded_base = self.encoded_base
        process_decode = self.process_decode

        # decoding as URL Encoding
        try:
            from urllib.parse import unquote
            decoded_url = unquote(encoded_base)
            if decoded_url != encoded_base and len(decoded_url) > 0:
                process_decode(decoded_url, 'URL Encoding')
        except Exception as _: pass

        # decoding as HTML Entity
        try:
            import html
            decoded_html = html.unescape(encoded_base)
            if decoded_html != encoded_base and len(decoded_html) > 0:
                process_decode(decoded_html, 'HTML Entity')
        except Exception as _: pass

        # decoding as Baconian Cipher
        try:
            clean_base = encoded_base.replace(' ', '').upper()
            if set(clean_base) <= {'A', 'B'} and len(clean_base) > 0 and len(clean_base) % 5 == 0:
                bacon_dict = {'AAAAA':'A', 'AAAAB':'B', 'AAABA':'C', 'AAABB':'D', 'AABAA':'E', 'AABAB':'F', 'AABBA':'G', 'AABBB':'H', 'ABAAA':'I', 'ABAAB':'J', 'ABABA':'K', 'ABABB':'L', 'ABBAA':'M', 'ABBAB':'N', 'ABBBA':'O', 'ABBBB':'P', 'BAAAA':'Q', 'BAAAB':'R', 'BAABA':'S', 'BAABB':'T', 'BABAA':'U', 'BABAB':'V', 'BABBA':'W', 'BABBB':'X', 'BBAAA':'Y', 'BBAAB':'Z'}
                res = ''
                valid = True
                for i in range(0, len(clean_base), 5):
                    chunk = clean_base[i:i+5]
                    if chunk in bacon_dict: res += bacon_dict[chunk]
                    else: valid = False; break
                if valid and len(res) > 0:
                    process_decode(res, 'Baconian Cipher')
        except Exception as _: pass

        # decoding as Unicode Escape
        try:
            if '\\u' in encoded_base or '\\U' in encoded_base:
                import codecs
                decoded_uni = codecs.decode(encoded_base, 'unicode_escape')
                if decoded_uni != encoded_base and len(decoded_uni) > 0:
                    process_decode(decoded_uni, 'Unicode Escape')
        except Exception as _: pass

        # decoding as Quoted-Printable
        try:
            if '=' in encoded_base:
                import quopri
                decoded_qp = quopri.decodestring(encoded_base.encode('ascii')).decode('utf-8', 'replace')
                if decoded_qp != encoded_base and len(decoded_qp) > 0:
                    process_decode(decoded_qp, 'Quoted-Printable')
        except Exception as _: pass

        # decoding as base2
        try:
            clean_base = encoded_base.replace(' ', '')
            if set(clean_base) <= {'0', '1'} and len(clean_base) % 8 == 0:
                b_str = bytes(int(clean_base[i:i+8], 2) for i in range(0, len(clean_base), 8))
                process_decode(b_str.decode('utf-8', 'replace'), 'Base2')
        except Exception as _: pass

        # decoding as base8
        try:
            clean_base = encoded_base.replace(' ', '')
            if set(clean_base) <= set('01234567') and len(clean_base) % 3 == 0:
                b_str = bytes(int(clean_base[i:i+3], 8) for i in range(0, len(clean_base), 3))
                process_decode(b_str.decode('utf-8', 'replace'), 'Base8')
        except Exception as _: pass

        # decoding as Morse Code
        try:
            clean_base = encoded_base.strip()
            if set(clean_base) <= set('.- /'):
                morse_dict = {'.-': 'A', '-...': 'B', '-.-.': 'C', '-..': 'D', '.': 'E', '..-.': 'F', '--.': 'G', '....': 'H', '..': 'I', '.---': 'J', '-.-': 'K', '.-..': 'L', '--': 'M', '-.': 'N', '---': 'O', '.--.': 'P', '--.-': 'Q', '.-.': 'R', '...': 'S', '-': 'T', '..-': 'U', '...-': 'V', '.--': 'W', '-..-': 'X', '-.--': 'Y', '--..': 'Z', '.----': '1', '..---': '2', '...--': '3', '....-': '4', '.....': '5', '-....': '6', '--...': '7', '---..': '8', '----.': '9', '-----': '0', '--..--': ', ', '.-.-.-': '.', '..--..': '?', '-..-.': '/', '-....-': '-', '-.--.': '(', '-.--.-': ')'}
                words = clean_base.replace('/', ' / ').split(' ')
                decoded_morse = ''
                valid = True
                for char in words:
                    if char == '': continue
                    if char == '/': decoded_morse += ' '
                    elif char in morse_dict: decoded_morse += morse_dict[char]
                    else: valid = False; break
                if valid and len(decoded_morse.strip()) > 0:
                    process_decode(decoded_morse.strip(), 'Morse Code')
        except Exception as _: pass

        # decoding as base16
        try:
            clean_hex = encoded_base.replace('0x', '').replace('\\x', '').replace(' ', '').replace('\n', '')
            process_decode(bytes.fromhex(clean_hex).decode('utf-8', 'replace'), 'Base16')
        except Exception as _: pass

        # decoding as base32
        try:
            process_decode(
                base64.b32decode(
                    encoded_base, casefold=False, map01=None
                ).decode('utf-8', 'replace'),
                'Base32'
            )
            self.b32_once = True
        except Exception as _: pass

        # decoding as base32 (RFC 3548)
        if not self.b32_once:
            try:
                """
                Base32 charset can differ based on their spec, this requires stripping
                the padding or changing charsets to get the correct results.
                By default this `anybase32` implementation follows the RFC 3548 spec.
                """
                temp_clean_base = str.encode(encoded_base.replace('=', ''))
                process_decode(
                    anybase32.decode(temp_clean_base).decode('utf-8', 'replace'),
                    'Base32'
                )
            except Exception as _: pass                

        # decoding as base36
        try:
            val = int(encoded_base, 36)
            b_str = val.to_bytes((val.bit_length() + 7) // 8, byteorder='big')
            if len(b_str) > 0:
                process_decode(b_str.decode('utf-8', 'replace'), 'Base36')
        except Exception as _: pass

        # decoding as base45
        try:
            b45_charset = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ $%*+-./:"
            if set(encoded_base) <= set(b45_charset) and len(encoded_base) > 0:
                res = []
                valid = True
                for i in range(0, len(encoded_base), 3):
                    chunk = encoded_base[i:i+3]
                    if len(chunk) == 3:
                        val = b45_charset.index(chunk[0]) + b45_charset.index(chunk[1])*45 + b45_charset.index(chunk[2])*45*45
                        if val > 65535:
                            valid = False
                            break
                        res.extend([val >> 8, val & 0xff])
                    elif len(chunk) == 2:
                        val = b45_charset.index(chunk[0]) + b45_charset.index(chunk[1])*45
                        if val > 255:
                            valid = False
                            break
                        res.append(val)
                    else:
                        valid = False
                        break
                if valid:
                    process_decode(bytes(res).decode('utf-8', 'replace'), 'Base45')
        except Exception as _: pass

        # decoding as base58
        try:
            process_decode(
                base58.b58decode(encoded_base.encode()).decode('utf-8', 'replace'),
                'Base58'
            )
        except Exception as _: pass

        # decoding as base62
        try:
            process_decode(
                base62.decodebytes(encoded_base).decode('utf-8', 'replace'),
                'Base62'
            )
        except Exception as _: pass

        # decoding as base64
        try:
            process_decode(
                base64.b64decode(encoded_base).decode('utf-8', 'replace'),
                'Base64'
            )
        except Exception as _: pass

        # decoding as base64url
        try:
            process_decode(
                base64.urlsafe_b64decode(
                    encoded_base + '=' * (4 - len(encoded_base) % 4)
                ).decode('utf-8', 'replace'),
                'Base64URL'
            )
        except Exception as _: pass

        # decoding as base85
        try:
            process_decode(
                base64.b85decode(encoded_base).decode('utf-8', 'replace'),
                'Base85'
            )
        except Exception as _: pass

        # decoding as ascii85
        try:
            process_decode(
                base64.a85decode(encoded_base).decode('utf-8', 'replace'),
                'Ascii85'
            )
        except Exception as _: pass

        # decoding as base91
        try:
            process_decode(
                base91.decode(encoded_base).decode('utf-8', 'replace'),
                'Base91'
            )
        except Exception as _: pass

        # decoding as base92
        try:
            process_decode(
                base92.decode(encoded_base),
                'Base92'
            )
        except Exception as _: pass

        # decoding as base100 lol why??!!
        try:
            process_decode(
                pybase100.decode(encoded_base).decode(),
                'Base100'
            )
        except Exception as _:
            pass