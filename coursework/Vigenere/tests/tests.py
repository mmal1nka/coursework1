import unittest

from coursework.Vigenere.vigenerecipher import msg_and_key, cipher_encryption


class ShiphrTest(unittest.TestCase):
    def setUp(self):
        pass

    def test1(self):
        key = msg_and_key('I love TUSUR', 'Yes')
        result = cipher_encryption('I love TUSUR', key)
        self.assertEqual('G pgni LSWMP', result)

    def test2(self):
        key = msg_and_key('Hello, World!', 'Hi')
        result = cipher_encryption('Hello, World!', key)
        self.assertEqual('Ommtp, Epzml!', result)

    def test3(self):
        key = msg_and_key('How are you doing?', 'dog')
        result = cipher_encryption('How are you doing?', key)
        self.assertEqual('Kcc dfk bca gcoqu?', result)

    def test4(self):
        key = msg_and_key('', 'cat')
        result = cipher_encryption('', key)
        self.assertEqual('', result)

    def test5(self):
        key = msg_and_key('', '')
        result = cipher_encryption('', key)
        self.assertEqual('', result)

    def test6(self):
        key = msg_and_key('+7959834430567', 'language')
        result = cipher_encryption('+7959834430567', key)
        self.assertEqual('+7959834430567', result)