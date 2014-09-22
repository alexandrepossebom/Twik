#!/usr/bin/env python
# -*- coding: utf-8; -*-
"""
* Copyright 2014 Alexandre Possebom
* Copyright 2014 Red Dye No. 2
* Copyright (C) 2011-2013 TG Byte Software GmbH
* Copyright (C) 2009-2011 Thilo-Alexander Ginkel.
* Copyright (C) 2010-2014 Eric Woodruff
* Copyright (C) 2006-2010 Steve Cooper

This file is part of twik.

Twik is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Twik is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Twik.  If not, see <http://www.gnu.org/licenses/>.
"""

from hashlib import sha1
from random import SystemRandom
import hmac
import getpass
import ConfigParser
import os.path
import argparse

def enum(**enums):
    return type('Enum', (), enums)

def privatekeygenerator():
    subgroups_length = [8, 4, 4, 4, 12]
    subgroup_separator = '-'
    allowed_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    systemrandom = SystemRandom()
    allowedcharslength = len(allowed_chars)
    key = ""
    for i in range(0, len(subgroups_length)):
        for j in range(0, subgroups_length[i]):
            key += allowed_chars[systemrandom.randrange(allowedcharslength)]
        if i < (len(subgroups_length) -1):
            key += subgroup_separator
    return key

def readprivatekey():
    private_key = ''
    homedir = os.path.expanduser('~')
    config_file = os.path.join(homedir, '.twik.conf')
    config = ConfigParser.ConfigParser()
    config.read(config_file)
    if not config.has_option('Profile', 'private_key'):
        config.add_section('Profile')
        private_key = privatekeygenerator()
        config.set('Profile', 'private_key', private_key)
        with open(config_file, 'w+') as fp:
            config.write(fp)
    else:
        private_key = config.get('Profile', 'private_key')
    return private_key

def injectcharacter(input, offset, reserved, seed, length, cStart, cNum):
    pos0 = seed % length
    pos = (pos0 + offset) % length
    for i in range(0, length - reserved):
        i2 = (pos0 + reserved + i) % length
        c = ord(input[i2])
        if c >= cStart or c < ord(cStart) + cNum:
            return input
    head = input[:pos] if pos > 0 else ""
    inject = ((seed + ord(input[pos])) % cNum) + ord(cStart)
    tail = input[pos+1:] if (pos + 1 < len(input)) else input
    return head + chr(inject) + tail


def removespecialcharacters(hash, seed, length):
    inputChars = list(hash)
    pivot = 0
    for i in range(0, length):
        if not inputChars[i].isdigit() and not inputChars[i].isalpha():
            inputChars[i] = chr(((seed + pivot) % 26 + ord('A')))
            pivot = i + 1
    return "".join(inputChars)

def converttodigits(hash, seed, length):
    inputChars = list(hash)
    pivot = 0
    for i in range(0, length):
        if not inputChars[i].isdigit():
            inputChars[i] = chr(((seed + ord(inputChars[pivot])) % 10 +
                ord('0')))
            pivot = i + 1
    return "".join(inputChars)

def generatehash(tag, key, length, password_type):
    digest = hmac.new(key, tag, sha1).digest()
    hash = digest.encode('base64')[:-2]

    seed = 0
    for i in range(0, len(hash)):
        seed += ord(hash[i])

    if password_type == PasswordType.NUMERIC:
        hash = converttodigits(hash, seed, length)
    else:
        hash = injectcharacter(hash, 0, 4, seed, length, '0', 10)
        if password_type == PasswordType.ALPHANUMERIC_AND_SPECIAL_CHARS:
            hash = injectcharacter(hash, 1, 4, seed, length, '!', 15)
        hash = injectcharacter(hash, 2, 4, seed, length, 'A', 26)
        hash = injectcharacter(hash, 3, 4, seed, length, 'a', 26)

        if password_type == PasswordType.ALPHANUMERIC:
            hash = removespecialcharacters(hash, seed, length)

    return hash[:length]


def getpassword(tag, private_key, master_key, length, password_type):
    hash = generatehash(private_key, tag, 24, 1)
    password = generatehash(hash, master_key, length, password_type)
    print "Your password is %s" % password

def main():
    global PasswordType
    PasswordType = enum(ALPHANUMERIC_AND_SPECIAL_CHARS=1, ALPHANUMERIC=2,
     NUMERIC=3)
    parser = argparse.ArgumentParser()
    parser.add_argument("tag", type=str,
        help="generate password for a specified tag")
    parser.add_argument("-c", type=int, default=12,
        help="length of generated password")
    parser.add_argument("-p", type=int, choices=[1, 2, 3], default=1,
        help="1 for ALPHANUMERIC_AND_SPECIAL_CHAR, 2 for ALPHANUMERIC and 3 for NUMERIC")
    args = parser.parse_args()

    private_key = readprivatekey()
    master_key = getpass.getpass()
    getpassword(args.tag, private_key, master_key, args.c, args.p)

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
