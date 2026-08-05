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
from .util import Util
import hmac
import getpass
import argparse
import sys
import base64

class Twik(object):
    def injectcharacter(self, mhash, offset, reserved, seed, length, cstart, cnum):
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


    def removespecialcharacters(self, mhash, seed, length):
        inputchars = list(mhash)
        pivot = 0
        for i in range(0, length):
            if not inputchars[i].isdigit() and not inputchars[i].isalpha():
                inputchars[i] = chr(((seed + pivot) % 26 + ord('A')))
                pivot = i + 1
        return "".join(inputchars)

    def converttodigits(self, mhash, seed, length):
        inputchars = list(mhash)
        pivot = 0
        for i in range(0, length):
            if not inputchars[i].isdigit():
                inputchars[i] = chr(((seed + ord(inputchars[pivot])) % 10 +
                    ord('0')))
                pivot = i + 1
        return "".join(inputchars)

    def generatehash(self, tag, key, length, password_type):
        key=key.encode('utf-8')
        tag=tag.encode('utf-8')
        digest = hmac.new(key, tag, sha1).digest()
        mhash = base64.standard_b64encode(digest)[:-1]
        mhash = mhash.decode('utf-8')

        seed = 0
        for i in range(0, len(mhash)):
            seed += ord(mhash[i])

        """NUMERIC"""
        if password_type == 3:
            mhash = self.converttodigits(mhash, seed, length)
        else:
            mhash = self.injectcharacter(mhash, 0, 4, seed, length, '0', 10)
            """ALPHANUMERIC_AND_SPECIAL_CHARS"""
            if password_type == 1:
                mhash = self.injectcharacter(mhash, 1, 4, seed, length, '!', 15)
            mhash = self.injectcharacter(mhash, 2, 4, seed, length, 'A', 26)
            mhash = self.injectcharacter(mhash, 3, 4, seed, length, 'a', 26)

            """ALPHANUMERIC"""
            if password_type == 2:
                mhash = self.removespecialcharacters(mhash, seed, length)

        return mhash[:length]


    def getpassword(self, tag, private_key, master_key, length, password_type):
        if length > 26 or length < 4:
            return None
        mhash = self.generatehash(private_key, tag, 24, 1)
        password = self.generatehash(mhash, master_key, length, password_type)
        return password

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
