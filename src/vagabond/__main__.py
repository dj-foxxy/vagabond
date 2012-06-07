from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from argparse import ArgumentParser
import os
import sys

from vagabond import Accounts

def create_argument_parser():
    argument_parser = ArgumentParser()
    add = argument_parser.add_argument
    add('--create', action='store_true', default=False)
    add('-d', '--dry-run', action='store_true', default=False)
    add('-ff', '--forgetting-factor', type=float,
            default=Accounts.DEF_FORGETTING_FACTOR)
    add('-ii', '--import-iom', nargs='+')
    add('-is', '--import-santander', nargs='+')
    add('-p', '--plot', action='store_true', default=False)
    add('csv')
    return argument_parser

def main(argv=None):
    if argv is None:
        argv = sys.argv
    args = create_argument_parser().parse_args(args=argv[1:])

    if not args.create and os.path.isfile(args.csv):
        accounts = Accounts.from_csv(args.csv)
    else:
        accounts = Accounts()

    if args.import_iom:
        from vagabond.importers import import_iom
        for path in args.import_iom:
            import_iom(accounts, path)

    if args.import_santander:
        from vagabond.importers import import_santander
        for path in args.import_santander:
            import_santander(accounts, path)

    print('Savings: %.2f' % accounts.get_balance())
    print('Predict broke date: %s' % accounts.predict_broke_date(
            forgetting_factor=args.forgetting_factor))

    if args.plot:
        from vagabond.plot import plot
        plot(accounts, forgetting_factor=args.forgetting_factor)

    if not args.dry_run:
        accounts.csv_to_file(args.csv)

    return 0

if __name__ == '__main__':
    exit(main())

