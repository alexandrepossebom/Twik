Twik
====

Python version of Twik


## Installation instructions:
  * Using PIP
  
```pip install twik```

  * Using easy_install
  
```easy_install twik```

  * Manual
```
git clone https://github.com/coxande/Twik.git
cd Twik
python setup.py install
```

## Usage instructions :

```
Usage: twik [-h] [-c C] [-p {1,2,3}] tag

positional arguments:
  tag         generate password for a specified tag

  optional arguments:
    -h, --help  show this help message and exit
    -c C        length of generated password
    -p {1,2,3}  1 for ALPHANUMERIC_AND_SPECIAL_CHAR, 2 for ALPHANUMERIC
                and 3 for NUMERIC
```

Private Key is stored in ~/.twik.conf you need change it to match with chrome extension and android app:

```
[Profile]
private_key = TFCY2AJI-NBPU-V01E-F7CP-PJIZNRKPF25W
```

