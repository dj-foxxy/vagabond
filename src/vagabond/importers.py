from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from datetime import datetime
import csv

def import_iom(accounts, path):
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
        if account_num in accounts:
            account = accounts[account_num]
        else:
            account = accounts.create(account_num,
                                      initial_amount=ts[0][4]-ts[0][3],
                                      name=ts[0][5])
        for t in ts:
            account.add_trans(t[3], t[0], t[2])

def import_santander(accounts, path):
    trans = []

    with open(path) as satander_file:
        for index in xrange(2):
            next(satander_file)
        account_num = next(satander_file).split()[-1]
        for index, line in enumerate(satander_file):
            field_index = index % 5
            if field_index == 0:
                if index > 0:
                    trans.append((date, balance, desc, amount))
                continue
            field = line.split(':')[1].split('\xa0')[1].strip()
            if field_index == 1:
                date = datetime.strptime(field, '%d/%m/%Y')
            elif field_index == 2:
                desc = field
            elif field_index == 3:
                amount = float(field)
            elif field_index == 4:
                balance = float(field)
        trans.append((date, balance, desc, amount))

    trans.sort(key=lambda t: t[0])

    if account_num in accounts:
        account = accounts[account_num]
    else:
        account = accounts.create(account_num,
                                  initial_amount=trans[0][1] - trans[0][3])
    for t in trans:
        account.add_trans(t[3], t[0], t[2])

