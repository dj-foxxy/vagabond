#!/usr/bin/env python2
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from argparse import ArgumentParser
from datetime import datetime
from itertools import groupby
import csv
import sys
import time

import numpy

class Transaction(object):
    def __init__(self, account, amount, date, desc):
        self.account = account
        self.amount = amount
        self.date = date
        self.desc = desc

    def __repr__(self):
        return str(self)

    def __str__(self):
        return '(%s)' % (','.join(map(str, (self.date, self.desc, self.amount,
                                            self.account.name))),)


class Account(object):
    def __init__(self, number, initial_amount=0, name=None):
        self.number = number
        self.name = name
        self.initial_amount = initial_amount
        self.trans= []

    def __str__(self):
        return 'Account[%s]{%s}' % (self.name, ','.join(map(str, self.trans)))

    def add_trans(self, amount, date, desc):
        self.trans.append(Transaction(self, amount, date, desc))


class Accounts(object):
    def __init__(self):
        self.accounts = set()
        self.accounts_lookup = {}

    def __str__(self):
        return ','.join(map(str, self.accounts))

    def __contains__(self, account):
        return account in self.accounts or account in self.accounts_lookup

    def __getitem__(self, account_number_or_name):
        return self.accounts_lookup[account_number_or_name]

    def __iter__(self):
        return iter(self.accounts)

    def create(self, *args, **kwargs):
        account = Account(*args, **kwargs)
        if account in self.accounts:
            raise ValueError('Account already added.')
        self.accounts.add(account)
        if account.number in self.accounts_lookup:
            raise ValueError('Account with number %r already added.'
                             % (account.number,))
        self.accounts_lookup[account.number] = account
        if account.name is not None and account.number != account.name:
            if account.name in self.accounts_lookup:
                raise ValueError('Account with name $r alreadt added.'
                                 % (account.name,))
            self.accounts_lookup[account.name] = account
        return account


class Book(object):
    def __init__(self):
        self.accounts = Accounts()

    def predict_broken_date(self):
        data = self.get_balance_data()
        for i, (date, running_balance) in enumerate(data):
            data[i][0] = time.mktime(date.timetuple())
        data = numpy.array(data)
        m, c = numpy.polyfit(data[:,0], data[:,1], 1)
        return datetime.fromtimestamp(-c / m), m, c

    def get_balance(self):
        return self.get_balance_data()[-1][1]

    def get_balance_data(self):
        balance = sum(acc.initial_amount for acc in self.accounts)
        trans = []
        for acc in self.accounts:
            trans.extend(acc.trans)
        trans.sort(key=lambda tran: tran.date)
        running_balance = []
        for date, trans_on_date in groupby(trans, lambda tran: tran.date):
            balance += sum(tran.amount for tran in trans_on_date)
            running_balance.append([date, balance])
        return running_balance

    def import_iom(self, path):
        trans = {}
        with open(path) as trans_file:
            for tran in filter(None, csv.reader(trans_file))[1:]:
                date = datetime.strptime(tran[0], '%d/%m/%Y')
                trans_type = tran[1]
                desc = tran[2][1:]
                amount = float(tran[3])
                balance = float(tran[4])
                account_name = tran[5][1:]
                account_num = tran[6][1:]

                if account_num not in trans:
                    trans[account_num] = []

                trans[account_num].append((date, trans_type, desc, amount,
                                           balance, account_name, account_num))
        for account_num, ts in trans.iteritems():
            ts.sort()
            if account_num in self.accounts:
                account = self.accounts[account_num]
            else:
                account = self.accounts.create(
                        account_num, initial_amount=ts[0][4], name=ts[0][5])
            for t in ts:
                account.add_trans(t[3], t[0], t[2])


def plot(book):
    from matplotlib import dates
    from matplotlib import rc
    from matplotlib import pyplot
    rc('font', family='serif')
    rc('text', usetex=True)
    data = numpy.array(book.get_balance_data())
    fig = pyplot.figure()
    plot = fig.add_subplot(111)
    plot.plot_date(data[:,0], data[:,1], drawstyle='steps-mid', fmt='b-')
    plot.xaxis.set_major_locator(dates.MonthLocator())
    plot.xaxis.set_major_formatter(dates.DateFormatter('%b'))
    plot.grid(True)
    plot.set_title('Savings over time')
    plot.set_xlabel('Date')
    plot.set_ylabel(r'Savings (\textsterling)')
    pyplot.show()

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
        plot(book)

    return 0

if __name__ == '__main__':
    exit(main())

