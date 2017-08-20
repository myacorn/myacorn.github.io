"""
Update the `/toys.rst' file from an Excel spreadsheet.

The toys data is in the first sheet. Each section heading is preceeded by any empty row.

    sudo pip install tablib

    python update_toys.py path/to/source.xlsx path/to/dest.rst

"""
import collections
import sys

from tablib import Databook


Toy = collections.namedtuple('Toy', 'name make')


class Toys(object):
    def __init__(self, src):
        # Create an empty Databook object, the workbook (and multiple sheets from Excel)
        with open(src, 'rb') as excel_data:
          book = Databook().load(None, excel_data.read())
          sheets = book.sheets()
          toys = sheets[0]
        
        is_header_next = False
        self.toys = {}

        for i, row in enumerate(toys):
            if not i or is_header_next:
                # header rows have no data in second column
                assert not row[1]
                heading = row[0]
                self.toys[heading] = []
                is_header_next = False
            elif not row[0]:
                # a blank line indicates that a header row is next
                is_header_next = True
                continue
            else:
                # this is a normal row, add to the current group
                self.toys[heading].append(Toy(row[0], row[1]))

    def save(self, dest):
        print self.toys


if __name__ == '__main__':
    src, dest = sys.argv[1:]
    Toys(src).save(dest)
