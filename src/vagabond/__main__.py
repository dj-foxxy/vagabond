from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from argparse import ArgumentParser
import sys

from vagabond import Accounts

def create_argument_parser():
    argument_parser = ArgumentParser()
    add = argument_parser.add_argument
    add('-ii', '--import-iom')
    add('-is', '--import-santander')
    add('-p', '--plot', action='store_true', default=False)
    return argument_parser

def main(argv=None):
    if argv is None:
        argv = sys.argv
    args = create_argument_parser().parse_args(args=argv[1:])

    accounts = Accounts()

    if args.import_iom:
        from vagabond.importers import import_iom
        import_iom(accounts, args.import_iom)

    if args.import_santander:
        from vagabond.importers import import_santander
        import_santander(accounts, args.import_santander)

    print('Savings: %.2f' % accounts.get_balance())
    print('Predict broke date: %s' % accounts.predict_broken_date())

    if args.plot:
        from vagabond.plot import plot
        plot(accounts)

    return 0

if __name__ == '__main__':
    exit(main())

