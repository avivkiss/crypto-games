from functools import partial
from StringIO import StringIO

def egcd(a, b):
    """
    Computes the extended GCD for (a,b). That is, it computes integers x and y
    such that ax + by = gcd(a, b) as well as gcd(a, b).

    :param a: First parameter for GCD.
    :param b: Second parameter for GCD.
    :return:
    """
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return g, x - (b // a) * y, y

def modinv(a, m):
    """
    Computes the modular inverse of a mod m.
    http://stackoverflow.com/questions/4798654/modular-multiplicative-inverse-function-in-python

    :param a: a in a^-1 mod m
    :param m: m in a^-1 mod m
    :return: a^-1 mod m or None if no inverse exists
    """
    g, x, y = egcd(a, m)
    if g != 1:
        return None
    else:
        return x % m


def join(s):
    """
    Turns an array of strings into one string.

    :param s: Array of string to join.
    :return: One string made by connecting all strings in the array.
    """
    return ''.join(s)

def split(s, n=None):
    """
    Split a string into portions of length n. If n is not supplied the
    string is split in half. Some examples:

    .. testcode::

        from crypto.tools import split

        print split("ABCDEF", 1)
        print split("ABCDEF", 2)
        print split("ABCDEF")

    .. testoutput::

        ['A', 'B', 'C', 'D', 'E', 'F']
        ['AB', 'CD', 'EF']
        ['ABC', 'DEF']


    :param s: A string
    :param n: the length of string portions
    :return s[]: an array of the portions of s
    """
    if n is None:
        return [s[:len(s) / 2], s[len(s) / 2:]]
    else:
        return [l for l in iter(partial(StringIO(s).read, n), '')]


def string_to_int(s):
    """
    Converts s to an int

    :param s: A string
    :return: The integer representation of the string s.
    """
    x = 0
    for i in range(len(s)):
        x += ord(s[i]) << (len(s)-1 - i) * 8
    return x


def int_to_string(x, l=None):
    """
    Converts a number to a string with length l

    :param x: A number between 0 and 2 ** l
    :param l: The length of the string to be returned
    :return: string
    """
    s = ''
    while x != 0:
        char = chr(x & 0xFF)
        x >>= 8
        s = char + s

    if l is None:
        return s
    else:
        return "\x00" * (l - len(s)) + s


def add_int_to_string(s, num, block_size):
    """
    Adds a number to a string

    :param s: String of length block_size
    :param num: A number s.t. 0 <= num < block_size
    :return: A string
    """
    x = (string_to_int(s) + num) % (2 ** block_size)
    s = int_to_string(x, block_size/8)
    return s


def xor_strings(s1, s2):
    """
    Returns the bitwise XOR of s1 and s2. If len(s1) != len(s2) the resulting
    XOR operation will be the size of the bigger string.

    :param s1: first string in XOR
    :param s2: second string in XOR
    :return: result of bitwise XOR of s1 and s2.
    """

    if len(s1) < len(s2):
        s1 = s1 + ("\x00" * (len(s2) - len(s1)))
    elif len(s2) < len(s1):
        s2 = s2 + ("\x00" * (len(s1) - len(s2)))


    return "".join(chr(ord(x) ^ ord(y)) for x, y in zip(s1, s2))