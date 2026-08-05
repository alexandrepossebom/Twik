Twik
====

Python version of Twik

[![Build Status](https://travis-ci.org/coxande/Twik.svg?branch=master)](https://travis-ci.org/coxande/Twik)


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
usage: twik [-h] [-c CHARS] [-p PROFILE] [-t {1,2,3}] tag

positional arguments:
  tag                   generate password for a specified tag

optional arguments:
  -h, --help            show this help message and exit
  -c [4-26], --chars [4-26]
                        length of generated password [4-26]. Default: 12
  -p PROFILE, --profile PROFILE
                        profile to use. Default:'Profile'
  -t {1,2,3}, --passwordtype {1,2,3}
                        1 for ALPHANUMERIC_AND_SPECIAL_CHAR
                        2 for ALPHANUMERIC
                        3 for NUMERIC
                        Default: 1


```

Private Keys is stored in $XDG_CONFIG_HOME/twik/twik.conf, or in
~/.config/twik/twik.conf when that variable is not set, you need change it to
match with chrome extension and android app:

```
[Personal]
private_key = TFCY2AJI-NBPU-V01E-F7CP-PJIZNRKPF25W
chars = 8
password_type = 1
github_chars = 12
github_password_type = 1

[foobar]
# for set foobar as default profile
default = 1
private_key = VBHF4HAR-8M5Z-NK3B-KQWH-KG9ZYLER4916
chars = 22
password_type = 1
reddit_chars = 22
reddit_password_type = 2
```

Older versions stored this file in ~/.twik.conf. It is moved to the path above
on the first run, keeping your private keys and your passwords unchanged.

