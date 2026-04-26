<h1 align="center">CryptoBreak</h1>
<h4 align="center">Advanced Base Encoding Decoder & Crypto Toolkit</h4>
<p align="center">
	<img src="https://img.shields.io/badge/version-5.0-blue.svg" title="version" alt="version">
	<a href="https://github.com/Hardikvats713/cryptobreak/blob/master/LICENSE"><img alt="GitHub license" src="https://img.shields.io/github/license/Hardikvats713/cryptobreak.svg"></a>
</p>

**CryptoBreak** is an advanced tool written in Python that can decode all alphanumeric base encoding schemes. This tool can accept single user input, multiple inputs from a file, input from argument, **multi-encoded bases**, **bases in image EXIF data**, **bases on images with OCR** and decode them incredibly fast.

It also features **ROT13/ROT47 decoding**, **Caesar cipher brute-forcing**, **hash identification**, **confidence scoring**, **JSON report export**, and **batch decode statistics**.

## Table of Contents
- [Features](#features)
- [Supported Encoding Schemes](#supported-encoding-schemes)
- [Advanced Features](#advanced-features)
- [Installation](#installation)
- [Usage](#usage)
- [API](#api)
- [Contribution](#contribution)
- [License](#license)

## Features

- Decode multi-encoded bases of any pattern.
- Decode bases in image EXIF data.
- Decode bases on images with OCR detection.
- Can decode multiple base encodings from a file.
- Generate a wordlist/output with the decoded bases.
- Predicts the type of encoding scheme.

## Supported Encoding Schemes
- Base2
- Base8
- Base16
- Base32
- Base36
- Base45
- Base58
- Base62
- Base64
- Base64Url
- Base85
- Ascii85
- Base91
- Base92
- Base100
- Morse Code
- Baconian Cipher
- URL Encoding
- HTML Entity
- Unicode Escape
- Quoted-Printable

## Advanced Features

| Feature | Flag | Description |
|---|---|---|
| ROT13/ROT47 Decoding | `--rot` | Instantly decode ROT13 and ROT47 ciphered text |
| Caesar Brute-Force | `--caesar` | Show all 25 shift outputs for Caesar cipher |
| Hash Identification | `--hash-id` | Identify MD5, SHA-1, SHA-256, SHA-512, Bcrypt, etc. |
| JSON Export | `--json FILE` | Export all decode results to a structured JSON report |
| Verbose Mode | `-v / --verbose` | Show confidence scores and decoded string lengths |
| Batch Statistics | _(automatic)_ | Summary table after batch file decoding |
| Encoding Chain View | _(magic mode)_ | Visual tree of multi-layer encoding patterns |

## Installation

    $ git clone https://github.com/Hardikvats713/cryptobreak.git
    $ cd cryptobreak
    $ pip3 install -r requirements.txt
    $ python3 cryptobreak.py -h

**NOTE:** Python3 is recommended to use!

**Linux:**

    $ sudo apt-get update
    $ sudo apt-get install tesseract-ocr libtesseract-dev

**MacOS:**

    $ brew install tesseract

**Windows:**

OCR Detection is implemented with [Tesseract](https://github.com/tesseract-ocr/tesseract) and Windows requires installation of the Tesseract executable. Installing the dependencies from `requirements.txt` which includes `pytesseract` should install it. If in case it doesn't, here's how you can set it up:

1. First check whether you have it installed or not in the `Program Files`/`Program Files (x86)` under the `Tesseract-OCR` directory.
2. If there is, give that path in the `config.json` and you're all set! If you don't have it, install it from [here](https://github.com/UB-Mannheim/tesseract/wiki) and set the path in `config.json`.

**Tesseract Docs:** https://tesseract-ocr.github.io/

## Usage

Get a list of all the arguments:

    python3 cryptobreak.py -h

To decode a single base encoding from user input:

    python3 cryptobreak.py

To decode a single base encoding from argument **(-b/--base)**:

    python3 cryptobreak.py -b SGVsbG8gV29ybGQh

To decode multiple base encodings from a file **(-f/--file)**:

    python3 cryptobreak.py -f file.txt

**Magic Mode:** To decode multi-encoded base of any pattern **(-m/--magic)**:

    python3 cryptobreak.py --magic

To input an image for **EXIF/OCR** detection mode **(-i/--image)**:

    python3 cryptobreak.py -i image.jpg (--exif/--ocr)

**EXIF Data:** To decode bases in image EXIF data **(-e/--exif)**:

    python cryptobreak.py -i image.jpg --exif

**OCR Base Detection:** To decode bases on image with OCR detection **(-c/--ocr)**:

    python cryptobreak.py -i image.jpg --ocr

To generate a wordlist/output with the decoded bases **(-o/--output)**:

    python cryptobreak.py -f file.txt -o output-wordlist.txt

### Advanced Usage

**ROT13/ROT47 Decoding:**

    python3 cryptobreak.py --rot "Uryyb Jbeyq"

**Caesar Cipher Brute-Force:**

    python3 cryptobreak.py --caesar "Ifmmp Xpsme"

**Hash Identification:**

    python3 cryptobreak.py --hash-id "d41d8cd98f00b204e9800998ecf8427e"

**JSON Export:**

    python3 cryptobreak.py -b SGVsbG8= --json report.json

**Verbose Mode (with confidence scores):**

    python3 cryptobreak.py -b SGVsbG8= -v
    
## Magic Mode

Now you can **decode multi-encoded bases** of any pattern in a single shot.

Have you ever stumbled upon that one lame CTF challenge that gives you an encoded string which is just encoded over and over with Base64, Base91, Base85 and so on? Just give that to CryptoBreak and you're done with it! ;)

Want to test it out? Just give it this input:

```
IX(Fp@nNG6ef<,*TFE]IT^zdINAb9EVbp,e<u=O6nN)/u+MTnU;Fo#VvQ&cK;mLZI#Jbdook<O{W#+gY%ooe#6pTkTa.9YPU8Uc=pl9BhSM9%kISw2k:8..u/6F2BwNndPZ2o#7NHNP3g,HlZu><*[Nv+T8
```

and see for yourself! :)

### CryptoBreak API

CryptoBreak can now be used as a library! Just import the `CryptoBreak()` class and call the `decode()` function.

See [**API**](https://github.com/Hardikvats713/cryptobreak#api).

## API

Want to use CryptoBreak as a library? We got you covered!

Just put `cryptobreak` in your project's directory and you're ready to go!

**Example:**

```python
# import the CryptoBreak class from cryptobreak.py
from cryptobreak import CryptoBreak

# calling the api function decode() with the encoded base
result = CryptoBreak().decode('c3BhZ2hldHRp')

# printing the output
"""
result is tuple where:
result[0] = DECODED STRING
result[1] = ENCODING SCHEME
"""
print('Decoded String: {}'.format(result[0]))
print('Encoding Scheme: {}'.format(result[1]))
```

**Output:**

```
Decoded String: spaghetti
Encoding Scheme: Base64
```

## Contribution

Ways to contribute
- Suggest a feature
- Report a bug
- Fix something and open a pull request
- Help me document the code
- Spread the word

Before you open a PR, make sure everything's good by running the tests:

**Unit Tests:**

    python3 -m unittest discover -v -s tests

## License
Licensed under the MIT License, see <a href="https://github.com/Hardikvats713/cryptobreak/blob/master/LICENSE">LICENSE</a> for more information.

## Author

**Hardik** - [GitHub](https://github.com/Hardikvats713)
