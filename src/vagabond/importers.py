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
            account = accounts.create(account_num, initial_amount=ts[0][4],
                                      name=ts[0][5])
        for t in ts:
            account.add_trans(t[3], t[0], t[2])

