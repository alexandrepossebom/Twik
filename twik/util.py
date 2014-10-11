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

import os.path
import ConfigParser
from random import SystemRandom

def privatekeygenerator():
    """
    Generate new private key
    """
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

class Util(object):
    """
    Class for deal with config file
    """
    def __init__(self, tag, chars, pass_type, profile):
        """
        Constructor
        """
        homedir = os.path.expanduser('~')
        self.filename = os.path.join(homedir, '.twik.conf')
        self.config = ConfigParser.ConfigParser()
        self.config.read(self.filename)
        self.tag = tag
        self.chars = chars
        self.profile = profile
        self.pass_type = pass_type
        #Initialize default values
        self.get_privatekey()

    def writeconfig(self):
        """
        Write config file
        """
        with open(self.filename, 'w+') as fileconfig:
            self.config.write(fileconfig)

    def get_privatekey(self):
        """
        Get private key if not exists create new one
        """
        private_key = ''
        if self.profile == None and len(self.config.sections()) > 0:
            for session in self.config.sections():
                if self.config.has_option(session, 'default') and self.config.getboolean(session, 'default') == True:
                    self.profile = session
                    break
            if self.profile == None:
                self.profile = self.config.sections()[0]
            print 'Using profile : %s' % self.profile

        if self.profile and self.config.has_option(self.profile, 'private_key'):
            private_key = self.config.get(self.profile, 'private_key')
        else:
            private_key = privatekeygenerator()
            if self.profile == None:
                self.profile = 'Personal'
            self.config.add_section(self.profile)
            self.config.set(self.profile, 'private_key', private_key)
            chars = self.chars
            if chars == None:
                chars = 12
            pass_type = self.pass_type
            if pass_type == None:
                pass_type = 1
            self.config.set(self.profile, 'chars', chars)
            self.config.set(self.profile, 'password_type', pass_type)
            if self.profile == 'Personal':
                self.config.set(self.profile, 'default', 1)
            self.writeconfig()
            print 'New profile is generated'
            self.config.read(self.filename)
        return private_key

    def get_chars(self):
        config_key = '%s_chars' % self.tag

        if self.config.has_option(self.profile, config_key) and self.chars == None:
            self.chars = self.config.getint(self.profile, config_key)
        else:
            if self.chars == None and self.config.has_option(self.profile, 'chars'):
                self.chars = self.config.getint(self.profile, 'chars')
            self.config.set(self.profile, config_key, self.chars)
            self.writeconfig()

        if self.chars < 4 or self.chars > 26:
            print 'invalid password length value from configuration using default'
            self.chars = 12

        return self.chars

    def get_passord_type(self):
        config_key = '%s_password_type' % self.tag

        if self.config.has_option(self.profile, config_key) and self.pass_type == None:
            self.pass_type = self.config.getint(self.profile, config_key)
        else:
            if self.pass_type == None and self.config.has_option(self.profile, 'password_type'):
                self.pass_type = self.config.getint(self.profile, 'password_type')

            self.config.set(self.profile, config_key, self.pass_type)
            self.writeconfig()

        if self.pass_type < 1 or self.pass_type > 3:
            print 'invalid password type value from configuration using default'
            self.pass_type = 1

        return self.pass_type

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
