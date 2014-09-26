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
from util import Util
import hmac
import getpass
import argparse

def enum(**enums):
    return type('Enum', (), enums)

def injectcharacter(mhash, offset, reserved, seed, length, cstart, cnum):
    pos0 = seed % length
    pos = (pos0 + offset) % length
    for i in range(0, length - reserved):
        tmp = (pos0 + reserved + i) % length
        char = ord(mhash[tmp])
        if char >= ord(cstart) and char < ord(cstart) + cnum:
            return mhash
    head = mhash[:pos] if pos > 0 else ""
    inject = ((seed + ord(mhash[pos])) % cnum) + ord(cstart)
    tail = mhash[pos+1:] if (pos + 1 < len(mhash)) else mhash
    return head + chr(inject) + tail


def removespecialcharacters(mhash, seed, length):
    inputchars = list(mhash)
    pivot = 0
    for i in range(0, length):
        if not inputchars[i].isdigit() and not inputchars[i].isalpha():
            inputchars[i] = chr(((seed + pivot) % 26 + ord('A')))
            pivot = i + 1
    return "".join(inputchars)

def converttodigits(mhash, seed, length):
    inputchars = list(mhash)
    pivot = 0
    for i in range(0, length):
        if not inputchars[i].isdigit():
            inputchars[i] = chr(((seed + ord(inputchars[pivot])) % 10 +
                ord('0')))
            pivot = i + 1
    return "".join(inputchars)

def generatehash(tag, key, length, password_type):
    digest = hmac.new(key, tag, sha1).digest()
    mhash = digest.encode('base64')[:-2]

    seed = 0
    for i in range(0, len(mhash)):
        seed += ord(mhash[i])

    if password_type == PASSWORDTYPE.NUMERIC:
        mhash = converttodigits(mhash, seed, length)
    else:
        mhash = injectcharacter(mhash, 0, 4, seed, length, '0', 10)
        if password_type == PASSWORDTYPE.ALPHANUMERIC_AND_SPECIAL_CHARS:
            mhash = injectcharacter(mhash, 1, 4, seed, length, '!', 15)
        mhash = injectcharacter(mhash, 2, 4, seed, length, 'A', 26)
        mhash = injectcharacter(mhash, 3, 4, seed, length, 'a', 26)

        if password_type == PASSWORDTYPE.ALPHANUMERIC:
            mhash = removespecialcharacters(mhash, seed, length)

    return mhash[:length]


def getpassword(tag, private_key, master_key, length, password_type):
    mhash = generatehash(private_key, tag, 24, 1)
    password = generatehash(mhash, master_key, length, password_type)
    print "Your password is %s" % password

def main():
    global PASSWORDTYPE
    PASSWORDTYPE = enum(ALPHANUMERIC_AND_SPECIAL_CHARS=1, ALPHANUMERIC=2,
        NUMERIC=3)
    parser = argparse.ArgumentParser()
    parser.add_argument("tag", type=str,
            help="generate password for a specified tag")
    parser.add_argument("-c", "--chars", type=int, default=-1,
            help="length of generated password. Default: 12")
    parser.add_argument("-p", "--profile", type=str, default='Profile',
            help="profile to use. Default:'Profile'")
    parser.add_argument("-t", "--passwordtype", type=int, choices=[1, 2, 3],
            default=-1,
            help='''
            1 for ALPHANUMERIC_AND_SPECIAL_CHAR
            2 for ALPHANUMERIC
            3 for NUMERIC
            Default: 1
            ''')
    args = parser.parse_args()

    util = Util(args.tag, args.chars, args.passwordtype, args.profile)

    master_key = getpass.getpass(prompt='Master Key: ')

    getpassword(args.tag, util.get_privatekey(), master_key,
            util.get_chars(), util.get_passord_type())

if __name__ == "__main__":
    main()

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
