import base64

from Crypto.Cipher import AES  # encryption library
from django.conf import settings


def encode(string):
    try:
        BLOCK_SIZE = 32

        # the character used for padding--with a block cipher such as AES, the value
        # you encrypt must be a multiple of BLOCK_SIZE in length.  This character is
        # used to ensure that your value is always a multiple of BLOCK_SIZE
        PADDING = '{'

        # one-liner to sufficiently pad the text to be encrypted
        def pad(s): return s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * PADDING

        # one-liners to encrypt/encode and decrypt/decode a string
        # encrypt with AES, encode with base64
        def EncodeAES(c, s): return base64.b64encode(c.encrypt(pad(s)))

        # create a cipher object
        cipher = AES.new(settings.SECURITY_AES_KEY)
        # encode a string
        encoded = EncodeAES(cipher, string)
        return encoded
    except:
        raise
        print "===================== Encrypted fails =========================="
        return string


def decode(string):
    try:
        BLOCK_SIZE = 32

        # the character used for padding--with a block cipher such as AES, the value
        # you encrypt must be a multiple of BLOCK_SIZE in length.  This character is
        # used to ensure that your value is always a multiple of BLOCK_SIZE
        PADDING = '{'

        # one-liner to sufficiently pad the text to be encrypted
        def pad(s): return s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * PADDING

        # one-liners to encrypt/encode and decrypt/decode a string
        # encrypt with AES, encode with base64
        def DecodeAES(c, e): return c.decrypt(
            base64.b64decode(e)).rstrip(PADDING)

        # create a cipher object
        cipher = AES.new(settings.SECURITY_AES_KEY)
        # encode a string
        decoded = DecodeAES(cipher, string)
        return decoded
    except:
        raise
        print "===================== Decrypted fails =========================="
        return string
