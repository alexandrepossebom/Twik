import os
import os.path
import tempfile
import unittest
from twik import twik
from twik import util

class ConfigPathTest(unittest.TestCase):
    """
    The configuration file holds the private key, so moving it to the XDG
    path must never leave the old one behind: a missing file generates a new
    private key and changes every password without warning.
    """
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.environ = dict(os.environ)
        os.environ['HOME'] = self.tmp.name
        os.environ.pop('XDG_CONFIG_HOME', None)
        self.legacy = os.path.join(self.tmp.name, '.twik.conf')
        self.config = os.path.join(self.tmp.name, '.config', 'twik',
                'twik.conf')

    def writelegacy(self, private_key):
        with open(self.legacy, 'w') as fileconfig:
            fileconfig.write('[Personal]\nprivate_key = %s\ndefault = 1\n' %
                    private_key)

    def testDefaultPathIsUsedWithoutXdgVariable(self):
        self.assertEqual(util.configpath(), self.config)

    def testXdgVariableIsUsedWhenAbsolute(self):
        os.environ['XDG_CONFIG_HOME'] = '/somewhere/config'
        self.assertEqual(util.configpath(),
                os.path.join('/somewhere/config', 'twik', 'twik.conf'))

    def testRelativeXdgVariableIsIgnored(self):
        os.environ['XDG_CONFIG_HOME'] = 'relative/config'
        self.assertEqual(util.configpath(), self.config)

    def testLegacyConfigIsMoved(self):
        self.writelegacy('TFCY2AJI-NBPU-V01E-F7CP-PJIZNRKPF25W')
        self.assertTrue(util.migrateconfig(self.legacy, self.config))
        self.assertFalse(os.path.exists(self.legacy))
        with open(self.config) as fileconfig:
            self.assertIn('TFCY2AJI-NBPU-V01E-F7CP-PJIZNRKPF25W',
                    fileconfig.read())

    def testExistingConfigIsNotOverwritten(self):
        self.writelegacy('LEGACY2A-NBPU-V01E-F7CP-PJIZNRKPF25W')
        os.makedirs(os.path.dirname(self.config))
        with open(self.config, 'w') as fileconfig:
            fileconfig.write('[Personal]\nprivate_key = CURRENT\n')
        self.assertFalse(util.migrateconfig(self.legacy, self.config))
        self.assertTrue(os.path.exists(self.legacy))
        with open(self.config) as fileconfig:
            self.assertIn('CURRENT', fileconfig.read())

    def testPrivateKeySurvivesMigration(self):
        key = 'TFCY2AJI-NBPU-V01E-F7CP-PJIZNRKPF25W'
        self.writelegacy(key)
        self.assertEqual(util.Util('tag', 12, 1, None).get_privatekey(), key)

    def testPrivateKeyIsKeptBetweenRuns(self):
        key = util.Util('tag', 12, 1, None).get_privatekey()
        self.assertEqual(util.Util('tag', 12, 1, None).get_privatekey(), key)

    def tearDown(self):
        os.environ.clear()
        os.environ.update(self.environ)
        self.tmp.cleanup()

class SiteExtractionTest(unittest.TestCase):
    """
    A website used as identifier must produce the same tag as the Android app,
    which hashes only the site name: 'https://www.example.com/' -> 'example'
    """
    def testUrlIsReducedToSiteName(self):
        self.assertEqual(util.extractsite('https://www.example.com/'),
                'example')
        self.assertEqual(util.extractsite('http://example.com'), 'example')
        self.assertEqual(util.extractsite('https://mail.google.com'), 'google')
        self.assertEqual(util.extractsite('https://www.google.co.uk/search?q=x'),
                'google')
        self.assertEqual(
                util.extractsite('https://github.com/alexandrepossebom/Twik'),
                'github')
        self.assertEqual(util.extractsite('https://WWW.EXAMPLE.COM/'),
                'example')

    def testTagWithoutSchemeIsNotModified(self):
        self.assertEqual(util.extractsite('tag'), 'tag')
        self.assertEqual(util.extractsite('example.com'), 'example.com')
        self.assertEqual(util.extractsite('my.mail'), 'my.mail')

    def testUrlWithoutSiteNameIsNotModified(self):
        self.assertEqual(util.extractsite('http://localhost:8080/'),
                'http://localhost:8080/')
        self.assertEqual(util.extractsite('https://'), 'https://')

class SimpleTest(unittest.TestCase):
    def setUp(self):
        self.t = twik.Twik()

    def testPasswordAphanumericAndSpecialChars(self):
        for chars in range(4, 27):
            password = self.t.getpassword('tag',
                'TFCY2AJI-NBPU-V01E-F7CP-PJIZNRKPF25W', 'foobar', chars, 1)
            if chars == 4:
                    self.assertEqual(password, 'm3/I')
            if chars == 8:
                    self.assertEqual(password, 'mb/5AsJ9')
            if chars == 12:
                    self.assertEqual(password, 'mb/5AsJ9Uon7')
            if chars == 22:
                    self.assertEqual(password, 'mb15As*9Uon7ZzvcsXMjpV')
            if chars == 26:
                    self.assertEqual(password, 'mb15AsJ9&on7ZzvcsXMjpVLTqQ')


    def testPasswordAlphanumeric(self):
        for chars in range(4, 27):
            password = self.t.getpassword('tag',
                    'TFCY2AJI-NBPU-V01E-F7CP-PJIZNRKPF25W', 'foobar', chars, 2)
            if chars == 4:
                    self.assertEqual(password, 'm31I')
            if chars == 8:
                    self.assertEqual(password, 'mb15AsJ9')
            if chars == 12:
                    self.assertEqual(password, 'mb15AsJ9Uon7')
            if chars == 22:
                    self.assertEqual(password, 'mb15AsJ9Uon7ZzvcsXMjpV')
            if chars == 26:
                    self.assertEqual(password, 'mb15AsJ9Uon7ZzvcsXMjpVLTqQ')

    def testPasswordNumeric(self):
        for chars in range(4, 27):
            password = self.t.getpassword('tag',
                'TFCY2AJI-NBPU-V01E-F7CP-PJIZNRKPF25W', 'foobar', chars, 3)
            if chars == 4:
                    self.assertEqual(password, '4315')
            if chars == 8:
                    self.assertEqual(password, '43154099')
            if chars == 12:
                    self.assertEqual(password, '431540992657')
            if chars == 22:
                    self.assertEqual(password, '4315409926570734032171')
            if chars == 26:
                    self.assertEqual(password, '43154099265707340321711986')

    def testSize(self):
        for chars in range(4, 27):
            password = self.t.getpassword('tag',
                'TFCY2AJI-NBPU-V01E-F7CP-PJIZNRKPF25W', 'foobar', chars, 1)
            self.assertEqual(len(password), chars)

    def testUrlAndSiteNameGiveSamePassword(self):
        key = 'TFCY2AJI-NBPU-V01E-F7CP-PJIZNRKPF25W'
        expected = self.t.getpassword('example', key, 'foobar', 12, 1)
        for url in ['https://www.example.com/', 'http://example.com',
                'https://example.com/login?next=/']:
            password = self.t.getpassword(util.extractsite(url), key, 'foobar',
                    12, 1)
            self.assertEqual(password, expected)

    def testSizeWrong(self):
        password = self.t.getpassword('tag',
                'TFCY2AJI-NBPU-V01E-F7CP-PJIZNRKPF25W', 'foobar', 100, 1)
        self.assertEqual(password, None)
    def testSize(self):
        password = self.t.getpassword('tag',
                'TFCY2AJI-NBPU-V01E-F7CP-PJIZNRKPF25W', 'foobar', 0, 1)
        self.assertEqual(password, None)

    def tearDown(self):
        self.t = None

if __name__ == '__main__':
   unittest.main()

