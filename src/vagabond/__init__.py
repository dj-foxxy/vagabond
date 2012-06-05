from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from datetime import datetime
from itertools import groupby
import csv
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


