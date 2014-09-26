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
from util import Util
from twik import Twik
import getpass
import argparse
import sys

def main():
    """
    ALPHANUMERIC_AND_SPECIAL_CHARS=1
    ALPHANUMERIC=2
    NUMERIC=3
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("tag", type=str,
            help="generate password for a specified tag")
    parser.add_argument("-c", "--chars", type=int,
            choices=range(4, 27),
            metavar="[4-26]",
            help="length of generated password [4-26]. Default: 12")
    parser.add_argument("-p", "--profile", type=str, default='Profile',
            help="profile to use. Default:'Profile'")
    parser.add_argument("-t", "--passwordtype", type=int, choices=[1, 2, 3],
            help='''
            1 for ALPHANUMERIC_AND_SPECIAL_CHAR
            2 for ALPHANUMERIC
            3 for NUMERIC
            Default: 1
            ''')
    args = parser.parse_args()

    util = Util(args.tag, args.chars, args.passwordtype, args.profile)

    master_key = getpass.getpass(prompt='Master Key: ')

    twik = Twik()
    password = twik.getpassword(args.tag, util.get_privatekey(), master_key,
            util.get_chars(), util.get_passord_type())

    print "Your password is %s" % password

if __name__ == "__main__":
    main()

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
