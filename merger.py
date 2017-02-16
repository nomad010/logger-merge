import os
import re
import datetime
from dateutil.parser import parserinfo, parse
import sys

pinfo = parserinfo(dayfirst=False)

class FileIterator(object):
    def _find_datetime(self):
        bracketing_re = r'(?=\[(?P<date>.*?)\])'
        matches = re.finditer(bracketing_re, self.line)
        for match in matches:
            try:
                new_date = parse(match.group('date'), pinfo, fuzzy=True)
                self.datetime = new_date
                break
            except Exception as e:
                pass

    def _read(self):
        try:
            self.line = next(self.input_iterator)
            self.has_line = True
            self._find_datetime()
        except StopIteration:
            self.line = ''
            self.has_line = False

    def __init__(self, fname, name=None):
        self.name = os.path.basename(fname) if name is None else name
        self.input_iterator = open(fname, 'r')
        self.datetime = datetime.datetime.min
        self._read()

    def next(self):
        if self.name:
            result = '[{}] '.format(self.name) + self.line
        else:
            result = line
        self._read()
        return result

    def valid(self):
        return self.has_line

    def line_dt(self):
        return self.datetime

    def __cmp__(self, other):
        return cmp(self.line_dt(), other.line_dt())  # noqa


def merge(*iterables):
    usable_iterables = list(iterables)
    while len(usable_iterables) > 0:
        idx = 0
        for i, v in enumerate(usable_iterables):
            if v < usable_iterables[idx]:
                idx = i
        yield next(usable_iterables[idx])
        if not usable_iterables[idx].valid():
            usable_iterables.pop(idx)


files = sys.argv[1:]
iterators = map(FileIterator, files)
sys.stdout.writelines(merge(*iterators))
