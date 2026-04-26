from setuptools import setup

setup(
    name='cryptobreak',
    version=5.0 ,
    description='CryptoBreak - Advanced Base Encoding Decoder & Crypto Toolkit',
    author='Hardik',
    url='https://github.com/Hardikvats713/cryptobreak',
    license='MIT',
    packages=[
        'src'
    ],
    py_modules=[
        'cryptobreak'
    ],
    install_requires=[
        'argparse',
        'colorama',
        'termcolor',
        'pathlib',
        'anybase32',
        'base36',
        'base58',
        'pybase62',
        'base91',
        'pybase100',
        'exifread',
        'opencv-python',
        'pytesseract'
    ],
    python_requires='>=3.0.0',
    entry_points={
        'console_scripts': [
            'cryptobreak = cryptobreak:main'
        ]
    }
)
