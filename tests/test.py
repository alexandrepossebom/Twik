import unittest
from twik import twik

class SimplisticTest(unittest.TestCase):
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

