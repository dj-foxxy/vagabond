from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from argparse import ArgumentParser
import sys

from vagabond import Book

def create_argument_parser():
    argument_parser = ArgumentParser()
    add = argument_parser.add_argument
    add('-i', '--import-iom')
    add('-p', '--plot', action='store_true', default=False)
    return argument_parser

def main(argv=None):
    if argv is None:
        argv = sys.argv
    args = create_argument_parser().parse_args(args=argv[1:])

    book = Book()

    if args.import_iom:
        book.import_iom(args.import_iom)

    print('Savings: %.2f' % book.get_balance())
    print('Predict broke date: %s' % book.predict_broken_date()[0])

    if args.plot:
        from vagabond.plot import plot
        plot(book)

    return 0

if __name__ == '__main__':
    exit(main())

