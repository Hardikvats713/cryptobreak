from cryptobreak import CryptoBreak
import unittest

class TestBase(unittest.TestCase):
    def test_base16(self):
        assert CryptoBreak().decode('436865636B537472696E67')[0] == 'CheckString', "Base16 test failed."

    def test_base32(self):
        assert CryptoBreak().decode('INUGKY3LKN2HE2LOM4======')[0] == 'CheckString', "Base32 test failed."

    def test_base36(self):
        assert CryptoBreak().decode('45640901731484716')[0] == 'checkstring', "Base36 test failed."

    def test_base58(self):
        assert CryptoBreak().decode('HiVkR1foHM1ZXjk')[0] == 'CheckString', "Base58 test failed."

    def test_base62(self):
        assert CryptoBreak().decode('6ZOc3cWz3dWiylL')[0] == 'CheckString', "Base62 test failed."

    def test_base64(self):
        assert CryptoBreak().decode('Q2hlY2tTdHJpbmc=')[0] == 'CheckString', "Base64 test failed."

    def test_base64url(self):
        assert CryptoBreak().decode('Q2hlY2tTdHJpbmc')[0] == 'CheckString', "Base64Url test failed."

    def test_ascii85(self):
        assert CryptoBreak().decode('6YL%@CK#=qBl7P')[0] == 'CheckString', "ASCII85 test failed."

    def test_base85(self):
        assert CryptoBreak().decode('Luh4VYg2S`X>Ml')[0] == 'CheckString', "Base85 test failed."

    def test_base91(self):                      
        assert CryptoBreak().decode('WXn>v;eYM%Z%xE')[0] == 'CheckString', "Base91 test failed."

    def test_base92(self):
        assert CryptoBreak().decode('9c&KSm]a;#m/X(')[0] == 'CheckString', "Base92 test failed."

    def test_base100(self):
        encode = '👫👟👜🐗👨👬👠👚👢🐗👙👩👦👮👥🐗👝👦👯🐗👡👬👤👧👜👛🐗👦👭👜👩🐗👫👟👜🐗👣👘👱👰🐗👛👦👞🐁'
        assert CryptoBreak().decode(encode)[0] == 'the quick brown fox jumped over the lazy dog', "Base100 test failed."

    # ── Advanced: Test ROT13 ─────────────────────────────────────────────
    def test_rot13(self):
        assert CryptoBreak.rot13_decode('Uryyb') == 'Hello', "ROT13 test failed."

    # ── Advanced: Test ROT47 ─────────────────────────────────────────────
    def test_rot47(self):
        assert CryptoBreak.rot47_decode('w6==@') == 'Hello', "ROT47 test failed."

    # ── Advanced: Test Caesar brute-force ─────────────────────────────────
    def test_caesar_bruteforce(self):
        results = CryptoBreak.caesar_bruteforce('Ifmmp')
        shifts = {shift: decoded for shift, decoded in results}
        assert shifts[25] == 'Hello', "Caesar brute-force test failed."

    # ── Advanced: Test hash identification ────────────────────────────────
    def test_hash_identify_md5(self):
        matches = CryptoBreak.identify_hash('d41d8cd98f00b204e9800998ecf8427e')
        types = [m['type'] for m in matches]
        assert 'MD5' in types, "Hash identification test failed."

    def test_hash_identify_sha256(self):
        matches = CryptoBreak.identify_hash('e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855')
        types = [m['type'] for m in matches]
        assert 'SHA-256' in types, "Hash identification test failed."

    # ── Advanced: Test confidence score ───────────────────────────────────
    def test_confidence_score(self):
        score = CryptoBreak.confidence_score('Hello World')
        assert score == 100.0, "Confidence score test failed."

if __name__ == "__main__":
    unittest.main()
