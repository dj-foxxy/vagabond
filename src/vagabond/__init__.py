from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from datetime import datetime
from itertools import groupby
import csv
import time

import numpy

class Transaction(object):
    def __init__(self, account, amount, date, desc, category=None):
        self.account = account
        self.amount = amount
        self.date = date
        self.desc = desc
        self.category = category

    def __repr__(self):
        return str(self)

    def __str__(self):
        return '(%s)' % (','.join(
                map(str, (self.date, self.desc, self.amount, self.account.name,
                          self.category))),)

    def csv(self):
        return (self.account.number, self.amount, self.date, self.desc,
                self.category)


class Account(object):
    def __init__(self, number, initial_amount=0, name=None):
        self.number = number
        self.name = name
        self.initial_amount = initial_amount
        self.trans= []

    def __str__(self):
        return 'Account[%s]{%s}' % (self.name, ','.join(map(str, self.trans)))

    def add_trans(self, *args, **kwargs):
        self.trans.append(Transaction(self, *args, **kwargs))

    def csv_account(self):
        return (self.number, self.name, self.initial_amount)

    def csv_trans(self):
        return [tran.csv() for tran in self.trans]


class Accounts(object):
    DEF_FORGETTING_FACTOR = 0.95

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

    def csv(self):
        trans = []
        for account in self.accounts:
            trans.extend(account.csv_trans())
        return [('accounts',)] \
                + [account.csv_account() for account in self.accounts] \
                + [('transactions',)] \
                + trans

    def csv_to_file(self, path):
        rows = self.csv()
        with open(path, 'w') as csv_file:
            csv.writer(csv_file).writerows(rows)

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

    def compute_saving_line(self, forgetting_factor=DEF_FORGETTING_FACTOR):
        data = numpy.matrix([(1, time.mktime(date.timetuple()), balance)
                             for date, balance in self.get_balance_data()])
        X = data[:,:2]
        y = data[:,2]
        ff = numpy.diag([forgetting_factor ** i
                         for i in xrange(X.shape[0], 0,-1)])
        theta = X.T.dot(ff).dot(X).getI().dot(X.T).dot(ff).dot(y)
        return theta[0,0], theta[1,0]

    def predict_broke_date(self, forgetting_factor=DEF_FORGETTING_FACTOR):
        c, m = self.compute_saving_line(forgetting_factor=forgetting_factor)
        return datetime.fromtimestamp(-c / m)

    def get_balance(self):
        return self.get_balance_data()[-1][1]

    @classmethod
    def from_csv(cls, path):
        accounts = cls()
        with open(path) as csv_file:
            for row in csv.reader(csv_file):
                if len(row) == 1:
                    if row[0] == 'accounts':
                        state = 1
                    elif row[0] == 'transactions':
                        state = 2
                    else:
                        raise ValueError('Illegal format: %r' % (row,))
                elif state == 1:
                    accounts.create(row[0], initial_amount=float(row[2]),
                                    name=row[1])
                elif state == 2:
                    account = accounts[row[0]]
                    date = datetime.strptime(row[2], '%Y-%m-%d').date()
                    category = row[4] if row[4] else None
                    account.add_trans(float(row[1]), date, row[3],
                                      category=category)
        return accounts


