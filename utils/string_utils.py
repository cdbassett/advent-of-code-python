import re
import collections
import string
import six

try:
    from collections.abc import Iterable
except ImportError:
    from collections import Iterable


def isNonStringIterable(val):
    return not isinstance(val, six.string_types) and isinstance(val, Iterable)
#    return not isinstance(val, basestring) and isinstance(val, collections.Iterable)

# converts iterables to tuples
# non-iterables are returned as a tuple with one entry
def toTuple(fields):
    if isinstance(fields, six.string_types):
        fields = (fields,)

    if not isinstance(fields, tuple) and isinstance(fields, collections.Iterable):
        fields = tuple(fields)

    return fields


def CommaFields(fields):
    if isNonStringIterable(fields):
        return ",".join(fields)

    return fields

    # if fields is a comma-separated string, split it into a list
    # otherwise return as-is
def CommaToList(fields):
    if isinstance(fields, six.string_types):
        return fields.split(",")

    return fields

    # if fields is a comma-separated string, split it into a list
    # otherwise return as-is
def ListToComma(fields):
    if not isinstance(fields, six.string_types):
        return ",".join(fields)

    return fields


    # converts passed parameter to a list in case it's a single string
def getStringList(string):
    if isNonStringIterable(string):
        return string

    return [string]

def joinNonEmpty(s, l):
    return s.join(i for i in l if i)


# this is used to pull out of larger string (?<!,)\b(\d{1,3}(?:,\d{3})*(?:\.\d*)?)\b(?!,)

reProperlyFormattedCommaNumbers = re.compile(r"(\d{1,3}(?:,\d{3})*(?:\.\d*)?)")


    # attempt to convert string to float, but handle commas
    # may need to use locale instead
    # Qualtrics can have "1,234", "7,45" (which is probably a decimal point)
    # if we have "." then "," need to switch
    # if "," is perfectly every 3 digits, assume it's thousands separator
def parseFloat(s):
    if isinstance(s, float):
        return s # already float?

    if isinstance(s, int):
        return float(s) # already int?

    s = s.strip()

    if "," in s and reProperlyFormattedCommaNumbers.match(s):
        return float(s.replace(",", ""))

    return float(s)


    # match either comma separated number as recognized by parseFloat, or straightforward int or float number
rePossibleFloatNumber = re.compile(r"(-?(?:\d{1,3}(?:,\d{3})*(?:\.\d*)?\b(?!,))|(?:\d+(?:\.\d*)?))")

def tryFloat(s):
    try:
        return parseFloat(s)
    except:
        return s

    # allows to sort the given list in the way that humans expect.
def alphaNumKey(s):
    """ Turn a string into a list of string and number chunks.
        "z23a" -> ["z", 23, "a"]
    """
    key = rePossibleFloatNumber.split(s)
    key[1::2] = map(tryFloat, key[1::2])
    key[0::2] = map(string.lower, key[0::2])
    return key
#    return [ tryFloat(c) for c in  ]

def to_human(value, radix=1024.0):
    """Convert a value to a string using SI suffixes.

    Example output:

    >>> to_human(20)
    '20.0 '
    >>> to_human(20 * 1024)
    '20.0k'
    >>> to_human(20 * 1024 ** 2)
    '20.0M'
    >>> to_human(20 * 1024 ** 3)
    '20.0G'
    >>> to_human(20 * 1024 ** 4)
    '20480G'
    """

    i = 0
    while value >= radix and i < 3:
        value /= radix
        i += 1
    suffix = " kMG"[i]
    if value > 100:
        value = locale.format('%d', value)
    elif value < 10:
        value = locale.format('%.2f', value)
    else:
        value = locale.format('%.1f', value)

    return "%s%s" % (value, suffix)


    # alternate implemention of natural sortintg keys
def atoi(text):
    return int(text) if text.isdigit() else text

reDigitSplit = re.compile(r"(\d+)")


def natural_keys(text):
    '''
    alist.sort(key=natural_keys) sorts in human order
    http://nedbatchelder.com/blog/200712/human_sorting.html
    (See Toothy's implementation in the comments)
    '''
    return [ atoi(c) for c in reDigitSplit.split(text) ]


def atof(text):
    try:
        retval = float(text)
    except ValueError:
        retval = text
    return retval

def natural_keys_float(text):
    '''
    alist.sort(key=natural_keys) sorts in human order
    http://nedbatchelder.com/blog/200712/human_sorting.html
    (See Toothy's implementation in the comments)
    float regex comes from https://stackoverflow.com/a/12643073/190597
    '''
    return [ atof(c) for c in re.split(r'[+-]?([0-9]+(?:[.][0-9]*)?|[.][0-9]+)', text) ]



    # return st, nd, th, etc
def ordinalIntSuffix(num):
    if num > 9:
        secondToLastDigit = str(num)[-2]
        if secondToLastDigit == '1':
            return 'th'
    lastDigit = num % 10
    if (lastDigit == 1):
        return 'st'
    elif (lastDigit == 2):
        return 'nd'
    elif (lastDigit == 3):
        return 'rd'
    else:
        return 'th'

def prePadLines(text, padding):
    if padding:
        return ''.join(padding + line for line in text.splitlines(True))

    return text

def enstring(sequence):
    for elem in sequence:
        yield str(elem), elem

def strseq(sequence):
    for elem in sequence:
        yield str(elem)

def strlist(sequence):
    return [str(e) for e in sequence]

def strip_end(s, end):
    if s.endswith(end):
        return s[:-len(end)]

    return s

reStripMultipleSpaces = re.compile(" +")
reStripPar = re.compile("[\(\)\[\]]\"", re.I)

def strip_par(text):
    text = reStripPar.sub("", text)
    text = reStripMultipleSpaces.sub(' ', text)
#    text = re.sub("", "", text)
    return text




    # replace stupid M$ product-inserted characters that won't convert to ASCII
def cleanUnicode(cleantext):
    cleantext = cleantext.replace(u"\u2013", u"-")
    cleantext = cleantext.replace(u"\u2014", u"-")
    cleantext = cleantext.replace(u"\u0092", u"'")
    cleantext = cleantext.replace(u"\u0096", u"-")
    cleantext = cleantext.replace(u"\u2019", u"'")
    cleantext = cleantext.replace(u"\u201d", u"\"")
    cleantext = cleantext.replace(u"\u201c", u"\"")
    cleantext = cleantext.replace(u"\u2026", u"...")
    cleantext = cleantext.replace(u"\u00a0", u" ")
    return cleantext.strip()

class TextIndenter(object):
    def __init__(self, indent="    ", level = 0, out = None):
        self.indent = indent
        self.indentstr = indent * level
        self.level = level
        self._out = out  # this is to specify a function for output

    def __str__(self):
        return self.indentstr

    def __call__(self, s):
        return self.indented(s)

    def indented(self, s):
        return self.indentstr + s

    def out(self, s):
        self._out(self.indented(s))

    # define multiple levels aof indentation at once
    # e.g. tiStudy, tiTopic, tiQuestion, tiResp = TextIndenters(4)
def TextIndenters(num, indent="    ", start_level = 0, out = None):
    return (TextIndenter(indent, level, out = out) for level in range(start_level, start_level + num))

class NextIndent(TextIndenter):
    def __init__(self, indenter):
        self.indent = indenter.indent
        self.level = indenter.level + 1


