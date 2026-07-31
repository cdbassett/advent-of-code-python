from __future__ import print_function
# -*- coding: utf-8 -*-
import fnmatch
import sys
import os
import os.path
from os.path import join, dirname, abspath, exists, splitext, split, basename
import datetime
from datetime import timedelta
from collections import OrderedDict,namedtuple,Counter
import codecs
import json
import itertools
import msvcrt
import operator
import functools
from pathlib import Path
import csv

import six
import requests
from icecream import ic

from YAMLUtils import *
from StringUtils import *
from iter_utils import *

mbDivisor  = 1024.0 * 1024.0
gbDivisor  = 1024.0 * mbDivisor

def EnsureDirExists(d):
    if not os.path.exists(d):
#        logger.info("Could not find directory %s, creating." % d)
        os.makedirs(d)  # this will create itermediate dirs as well
        return False

    return True


#def getFiles(directory, pattern):
#    filesInDir = [entry for entry in os.listdir(directory) if os.path.isfile(os.path.join(directory, entry))]
#    return fnmatch.filter(filesInDir, pattern)

#def getFiles(directory, patterns):
#    filtered = []
#    filesInDir = [entry for entry in os.listdir(directory) if os.path.isfile(os.path.join(directory, entry))]
#
#    for pattern in getStringList(patterns):
#        filtered.extend(fnmatch.filter(filesInDir, pattern))
#
#    filtered.sort()
#    return filtered


    # like fnmatch but works with multiple patterns
def matchFiles(files, patterns):
    patterns = getStringList(patterns)
    filtered = []

    for pattern in patterns:
        filtered.extend(fnmatch.filter(files, pattern))

    return filtered


    # get list of files using multiple directories and match patterns
    # each file is only listed once, even if it exists in multiple passed directories
    # this allows "preferred" locations for files
    # note that path is not included, entry just means it exists in at least one directory
def getFiles(directories, patterns="*", regEx = False, use_dirs = False):
    filesInDir = []
    filesInDirSet = set()

    for d in getStringList(directories):
        if not os.path.isdir(d):
            continue

        if six.PY2 and isinstance(d, str):
            d = unicode(d)

        for entry in os.listdir(d):
            if os.path.isdir(join(d, entry)) == use_dirs:
                upperEntry = entry.upper()

                if upperEntry not in filesInDirSet:
                    filesInDirSet.add(upperEntry)
                    filesInDir.append(entry)

#    printList("filesInDir", filesInDir)


    if regEx:
        filtered = []
        patterns = getStringList(patterns)
        compiledPatterns = [re.compile(pattern, re.UNICODE) for pattern in patterns]

        for compiledPattern in compiledPatterns:
            filtered.extend(fileInDir for fileInDir in filesInDir if compiledPattern.match(fileInDir))
    else:
        filtered = matchFiles(filesInDir, patterns)

    filtered.sort()
#    printList("filtered", filtered)
    return filtered


def get_directories(directory):
    return list(path for path in os.listdir(unicode(directory)) if os.path.isdir(os.path.join(directory, path)))

def walk2(basedir,  excluded):
    """Traverse a directory tree in pre-order

    Walk2 is a thin wrapper around walk. It splits each path into a
    (relpath, root) tuple where root is the parent directory of
    basedir.
    """

    root = os.path.dirname(basedir)

    for sub in walk(basedir, excluded):
        yield sub[len(root):], root


def walk(dir_,  excluded):
    """Traverse a directory tree in pre-order.

    branches specified in exclude are ignored. Symbolic links are followed.
    """

    try:
        subs = os.listdir(dir_)
    except OSError:
        return

    subs = [os.path.join(dir_, sub) for sub in subs]
    subs = [sub for sub in subs if os.path.isdir(sub) and sub not in excluded]

    yield dir_

    for sub in subs:
        for res in walk(sub, excluded):
            yield res


    # delete file, ignoring errors
def AttemptKillFile(f, msg = False):
    try:
        os.unlink(f)
    except:
        if msg:
            print("failed to delete \"{}\"".format(f))

        pass

def findFile(d, pattern):
    fileNames = os.listdir(d)
    fileNames.sort()

    for fileName in fileNames:
        if fnmatch.fnmatch(fileName, pattern):
            return os.path.join(d, fileName)

    return None

def findFiles(d, patterns):
    filtered = matchFiles(os.listdir(d), patterns)
#    filtered.sort()
    filtered = sorted(filtered, key=str.casefold)
    return [os.path.join(d, fileName) for fileName in filtered]

def kill_files(d, pattern):
    for fileName in findFiles(d, pattern):
        AttemptKillFile(fileName)


def printList(title, lst, inset = "", file=sys.stdout):
    print("{}{}".format(inset, title), file=file)

    for item in lst:
        print(u"{}\t{}".format(inset, item), file=file)

def printDict(title, dct, inset = "", file=sys.stdout):
    printPairs(title, dct.items(), inset, file=file)

def printPairs(title, pairs, indent = "", file=sys.stdout):
    print("{}{}".format(indent, title), file=file)

    for key, value in pairs:
        print(u"{}\t{}: {}".format(indent, key, value), file=file)


def printDictRecursive(d, indent = 0, out=sys.stdout):
    indentString = "\t" * indent

    for key, value in d.iteritems():
        if isinstance(value, dict):
            print("%s%s: " % (indentString, key), file=out)

            printDictRecursive(value, indent + 1, out)
        elif isNonStringIterable(value):
            indentString = "\t" * (indent + 1)

            for item in value:
                print(u"{}\t{}".format(indentString, repr(item)))
        else:
            print("%s%s: %s" % (indentString, key, repr(value)), file=out)


def writeDictLists(filename, dl):
    with codecs.open(filename, "wb", "utf-8") as f:
        for key, lst in dl.iteritems():
            f.write("%s:\r\n" % key)

            for l in lst:
                f.write("    %s\n" % l)

def writeDictSets(filename, dl):
    with open(fname, "w") as f:
        for key, s in dl.iteritems():
            f.write("%s:\r\n" % key)
            lst = list(s)
            lst.sort()

            for l in lst:
                f.write("    %s\r\n" % l)


def writeListTupleLists(filename, dl):
    with codecs.open(filename, "wb", "utf-8") as f:
        for header, lst in dl:
            f.write("%s:\r\n" % header)

            for item in lst:
                f.write("    %s\r\n" % item)

def writeList(fname, dl):
    with codecs.open(fname, "wb", "utf-8") as f:
        f.writelines([l + "\r\n" for l in dl])

def writeSet(filename, dl):
    lst = list(dl)
    lst.sort()

    with codecs.open(filename, "wb", "utf-8") as f:
        f.writelines([l + "\r\n" for l in lst])

def read_text_list(filename):
    with open(filename, "r", encoding = "utf-8") as f:
        return [line.rstrip() for line in f.readlines()]

def WriteUtf8File(filename, text):
    with codecs.open(filename, "wb", "utf-8") as f:
        f.write(text)

def ReadUtf8File(filename):
    with codecs.open(filename, "rb", "utf-8") as f:
        return f.read()

def WriteUtf8JsonFile(filename, contents):
    with codecs.open(filename, "wb", "utf-8") as outfile:
        json.dump(contents, outfile, indent=4)

def WriteUtf8JsonAndYamlFile(filename, contents):
    with codecs.open(filename, "wb", "utf-8") as outfile:
        json.dump(contents, outfile, indent=4)

    base_path = os.path.splitext(filename)[0]
    yaml_path = base_path + ".yaml"
    outputYAMLFile(yaml_path, contents)

def ReadUtf8JsonFile(filename):
    with open(filename, encoding = "utf-8") as f:
        return json.load(f)

def format_filename(s):
    """Take a string and return a valid filename constructed from the string.
Uses a whitelist approach: any characters not present in valid_chars are
removed. Also spaces are replaced with underscores.

Note: this method may produce invalid filenames such as ``, `.` or `..`
When I use this method I prepend a date string like '2009_01_15_19_46_32_'
and append a file extension like '.txt', so I avoid the potential of using
an invalid filename.

"""
    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    filename = ''.join(c for c in s if c in valid_chars)
    filename = filename.replace(' ','_') # I don't like spaces in filenames.
    return filename


def write_tabbed_line(file, seq):
    file.write(u"{}\r\n".format(u"\t".join(six.text_type(s) for s in seq)))

def write_tabbed_file(filename, header, lines):
    with codecs.open(filename, "wb", "utf-8-sig") as f:
        write_tabbed_line(f, header)

        for line in lines:
            write_tabbed_line(f, line)


def write_namedtuple_tabbed_file(filename, header, lines):
    with codecs.open(filename, "wb", "utf-8-sig") as f:
        write_tabbed_line(f, header)

        for line in lines:
#            write_tabbed_line(f, line)
#            print(line)
            print(u"\t".join(six.text_type(getattr(line, h)) for h in header), file=f)


def write_sorted_by_lists(l, base_path, prefix, headers, sort_by = 0):
    def get_filename(add=""):
        return os.path.join(base_path, "_".join(s for s in (prefix, add) if s) + ".csv")

    def rearrange(line, index):
        return line[index:index+1] + line[0:index] + line[index+1:]

    headers = CommaToList(headers)
    sort_headers = headers[:sort_by] if sort_by else headers

    for index, hdr in enumerate(sort_headers):
        write_tabbed_file(get_filename(hdr), rearrange(headers, index), sorted((rearrange(line, index) for line in l), reverse=index==0))

def write_counter_file(counter, base_path, prefix, tag_name):
    def get_filename(add=""):
        return os.path.join(base_path, "_".join(s for s in (prefix, add) if s) + ".csv")

    write_tabbed_file(get_filename("frequency"), ("Count", tag_name), ((str(count), tag) for (tag, count) in sorted(counter.items(), key=lambda x: x[1], reverse=True)))
    write_tabbed_file(get_filename("alpha"), (tag_name, "Count"), ((tag, str(count)) for (tag, count) in sorted(counter.items(), key=lambda x: x[0])))

def write_tsv_file(fname, data):
    with open(fname, encoding="utf-8") as out_f:
        for line in data:
            print("\t".join(line), file=out_f)

def read_tsv_file(fname):
    with open(fname, encoding="utf-8") as in_f:
        reader = csv.reader(in_f, delimiter="\t")
        yield from reader

class FileCache:
    """
    Usage:
    reader = FileCache('data.txt')
    print(reader.get_content()) # First read, populates cache
    print(reader.get_content()) # Second read, returns cache
    """
    def __init__(self, filepath, process=None):
        self.filepath = filepath
        self.cache = None
        self.last_mtime = 0
        self.process = process

    def get_content(self, indicate_cached=False):
        # 1. Get the current modification time of the file
        current_mtime = os.path.getmtime(self.filepath)
        cached = True

        # 2. Compare current mtime with stored mtime
        if current_mtime != self.last_mtime:
            cached = False
#            print("File changed. Re-reading from disk...")
            if self.process:
                self.cache = self.process(self.filepath)
            else:
                with open(self.filepath, 'r') as f:
                    self.cache = f.read()

            self.last_mtime = current_mtime
#        else:
#            print("Returning cached content...")

        return (self.cache, cached) if indicate_cached else self.cache

def updateRetrieveCachePage(filename, url, max_age = timedelta(days=1)):
    print("Using {}".format(filename))
    needUpdate = False

    if not os.path.isfile(filename):
        print("Couldn't find {}, will retrieve".format(filename))
        needUpdate = True
    else:
        file_mod_time = datetime.datetime.fromtimestamp(os.stat(filename).st_mtime)  # This is a datetime.datetime object!
        now = datetime.datetime.today()
#        max_age = timedelta(minutes=5)
#        print(now)
#        print(file_mod_time)
#        print(max_age)

        if now - file_mod_time > max_age:
            print("{} is old, will retrieve".format(filename))
            needUpdate = True


    if needUpdate:
        response = requests.get(url)
        pageContent = response.text
        WriteUtf8File(filename, pageContent)
    else:
        pageContent = ReadUtf8File(filename)

    return needUpdate

def get_cached_file(file_path, getter, params=(), only_if_older_than = None, writer=WriteUtf8File, reader=ReadUtf8File):
    needUpdate = False

    if not os.path.isfile(file_path):
        print(u"Couldn't find {}, will retrieve".format(file_path))
        needUpdate = True
    else:
        if only_if_older_than:
            file_mod_time = datetime.datetime.fromtimestamp(os.stat(file_path).st_mtime)  # This is a datetime.datetime object!

            if file_mod_time < only_if_older_than:
                print(u"{} is old, will retrieve".format(file_path))
                needUpdate = True

    contents = None

    if not needUpdate:
        contents = reader(file_path)
        needUpdate = not contents

    if needUpdate:
        contents = getter(*params)

        if contents != None:
            writer(file_path, contents)

    return contents, needUpdate

def get_cached_json(file_path, getter, params=(), only_if_older_than = None):
    return get_cached_file(file_path, getter, params, only_if_older_than, writer=WriteUtf8JsonAndYamlFile, reader=ReadUtf8JsonFile)

def get_file_datetime(path):
    return datetime.datetime.fromtimestamp(os.stat(path).st_mtime)


def WriteFile(filename, text):
    with codecs.open(filename, "wb", "utf-8") as f:
        f.write(text)

def ReadFile(filename):
    with codecs.open(filename, "rb", "utf-8") as f:
        return f.read()


def updateRetrieveCachePage(filename, url):
    print(filename)
    needUpdate = False

    if not os.path.exists(filename):
        print("Couldn't find {}, will retrieve".format(filename))
        needUpdate = True
    else:
        file_mod_time = datetime.datetime.fromtimestamp(os.stat(filename).st_mtime)  # This is a datetime.datetime object!
        now = datetime.datetime.today()
        max_delay = timedelta(days=1)
#        max_delay = timedelta(minutes=5)
#        print(now)
#        print(file_mod_time)
#        print(max_delay)

        if now - file_mod_time > max_delay:
            print("{} is old, will retrieve".format(filename))
            needUpdate = True


    if needUpdate:
        response = requests.get(url)
        pageContent = response.text
        WriteFile(filename, pageContent)
    else:
        pageContent = ReadFile(filename)

    return pageContent


def get_keys_or_list(obj):
    return obj.keys() if isinstance(obj, dict) else obj or []


escape_keys = (27, chr(27))

def escape_was_pressed():
   return msvcrt.kbhit() and (msvcrt.getch()[0] in escape_keys)


def exit_if_escape_was_pressed():
      if escape_was_pressed():
        sys.exit(1) # allow aborting

# backup a file, with versioned numbers
# if rename, will rename file, otherwise will make a copy
# return True on success (False likely means file did not exist)
# example: version_file('test.txt')
def version_file_old(file_spec, rename=False):
    import os, shutil

    if os.path.isfile(file_spec):
        # Determine root filename so the extension doesn't get longer
        n, e = os.path.splitext(file_spec)

        # Is e an integer?
        try:
             num = int(e)
             root = n
        except ValueError:
             root = file_spec

        # Find next available file version
        for i in xrange(1000):
             new_file = '%s.%03d' % (root, i)

             if not os.path.isfile(new_file):
                  if rename:
                      os.rename(file_spec, new_file)
                  else:
                      shutil.copy(file_spec, new_file)

                  return new_file

    return 0


def first_version_int(file_spec):
    for n, e in enumerate(Path(file_spec).suffixes):
        try:
            num = int(e)
#            print(f"    version={num}")
            return n, num
        except ValueError:
            pass

    return -1, None


def file_version(file_spec):
    if os.path.isfile(file_spec):
        return first_version_int(file_spec)[1]
            # Determine root filename so the extension doesn't get longer
        name, ext = os.path.splitext(file_spec)
        numname, number = os.path.splitext(name)
        number = number[1:]
#        print(f"{file_spec}: name={name}, ext={ext}, numname={numname}, number={number}")
#        print(f"{file_spec}: name={name}, ext={ext}, number={number}")

            # Is number an integer?
        try:
            num = int(number)
#            print(f"    version={num}")
            return num
        except ValueError:
            pass

        try:
            num = int(ext)
#            print(f"    version={num}")
            return num
        except ValueError:
            pass

    return None


    # make a backup copy of a file, before you overwrite it, with the standard protocol of appending a three-digit version number to the name of the old file.
    # originally taken from https://www.oreilly.com/library/view/python-cookbook/0596001673/ch04s26.html
    # modified to use same extension and put numeric part before extension and to use "rename" instead of vtype, and to return filename
def version_file(file_spec, rename=False, version_last=False):
    import os, shutil

    if os.path.isfile(file_spec):
#        suffixes = Path(file_spec).suffixes
#        idx, vers = first_version_int(file_spec)

            # Determine root filename so the extension doesn't get longer
        name, ext = os.path.splitext(file_spec)
        numname, number = os.path.splitext(name)

            # Is number an integer?
        try:
            num = int((ext if version_last else number)[1:])
            root = numname
        except ValueError:
            root = name

#        ic(name, ext, numname, number, root)

            # Find next available file version
        for i in range(1000):
            new_file = f"{root}{ext}.{i:03d}" if version_last else f"{root}.{i:03d}{ext}"

            if not os.path.isfile(new_file):
                if not rename:
                    shutil.copy(file_spec, new_file)
                else:
                    os.rename(file_spec, new_file)

                return new_file

    return 0

def is_versioned_file(file_spec):
    version = file_version(file_spec)
    result = version != None
    ic(file_spec, version, result)
    return result

mb = 1 << 27 #2 ^ 30
gb = 1 << 30 #2 ^ 30

def getFormattedSizeInMB(size):
    return str(round(float(size) / mb, 2)) + "Mb"

def getFormattedSizeInGB(size):
    return str(round(float(size) / gb, 2)) + "Gb"


def get_integers_from_string(s):
    return (int("".join(c)) for match, c in itertools.groupby(s, lambda c: c.isdigit() or c =="-") if match)



def get_vis_map(dots, reversed = False, min_val=None, max_val=None):
    def get_dim(dims):
        dims = list(dims)
#        assert(dots)
        negative_x = min(dims) if min_val is None else min_val
        positive_x = max(dims) + 1 if max_val is None else max_val
        return -negative_x, max(15, positive_x - negative_x)

    assert(dots)
    min_x, width = get_dim(p.x for p in dots)
    min_y, height = get_dim(p.y for p in dots)
#    ics(min_x, min_y)
    vis_map = [["."] * width for r in range(height)]

    for p in dots:
        try:
            if reversed:
                vis_map[height - (p.y + min_y) - 1][p.x + min_x] = "#"
            else:
                vis_map[p.y + min_y][p.x + min_x] = "#"
        except IndexError:
            ic(p.y, p.x)
            raise

    vis_map = [f"({-min_x},{-min_y})"] + ["".join(e) for e in vis_map]
#        vis_map = "\n".join("".join(e) for e in vis_map)
    return vis_map


from typing import Protocol, Iterator, Tuple, TypeVar, Optional
T = TypeVar('T')

#import heapq
#
#class PriorityQueue:
#    def __init__(self):
#        self.elements: list[tuple[float, T]] = []
#
#    def empty(self) -> bool:
#        return not self.elements
#
#    def put(self, item: T, priority: float):
#        heapq.heappush(self.elements, (priority, item))
#
#    def get(self) -> T:
#        return heapq.heappop(self.elements)[1]
#
#import collections
#
#class Queue:
#    def __init__(self):
#        self.elements = collections.deque()
#
#    def empty(self) -> bool:
#        return not self.elements
#
#    def put(self, x: T):
#        self.elements.append(x)
#
#    def get(self) -> T:
#        return self.elements.popleft()
#

class PrintMaxTimes(object):
    def __init__(self, max_count, out_method = print):
        self.max_count = max_count
        self.printed_count = 0
        self.out_method = out_method

    def print(self, *msg):
        if self.printed_count < self.max_count:
            self.out_method(*msg)
            self.printed_count += 1

    def should_print_and_inc(self):
        result = self.printed_count < self.max_count
        self.printed_count += 1
        return result

    def should_print(self):
        return self.printed_count < self.max_count

def typename(x):
    return type(x).__name__

