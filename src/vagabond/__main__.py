from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from argparse import ArgumentParser
import logging
import os
import sys

from vagabond import Accounts

DEF_LOG_LEVEL = 'INFO'

def create_argument_parser():
    argument_parser = ArgumentParser()
    add = argument_parser.add_argument
    add('-c', '--categorise', action='store_true', default=False)
    add('--create', action='store_true', default=False)
    add('-d', '--dry-run', action='store_true', default=False)
    add('-f', '--forcast', action='store_true', default=False)
    add('-ff', '--forgetting-factor', type=float,
            default=Accounts.DEF_FORGETTING_FACTOR)
    add('-ii', '--import-iom', nargs='+')
    add('-is', '--import-santander', nargs='+')
    add('-l', '--log-level', default=DEF_LOG_LEVEL)
    add('-p', '--plot', action='store_true', default=False)
    add('csv')
    return argument_parser

def main(argv=None):
    if argv is None:
        argv = sys.argv
    args = create_argument_parser().parse_args(args=argv[1:])

    log_numeric_level = getattr(logging, args.log_level.upper(), None)
    if not isinstance(log_numeric_level, int):
        raise ValueError('Invalid log level %s', args.log_level)
    logging.basicConfig(format='%(levelname)s: %(asctime)s: %(message)s',
                        level=log_numeric_level)

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

    if args.categorise:
        from vagabond.categorise import categorise
        categorise(accounts)


    if args.plot:
        from vagabond.plot import plot
        plot(accounts, forgetting_factor=args.forgetting_factor)

    if args.forcast:
        print('Savings: %.2f' % accounts.get_balance())
        print('Predict broke date: %s' % accounts.predict_broke_date(
                forgetting_factor=args.forgetting_factor))

    if not args.dry_run:
        accounts.csv_to_file(args.csv)

    return 0

if __name__ == '__main__':
    exit(main())

