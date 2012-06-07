from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from vagabond import CATEGORIES as _CAT

CATEGORIES = sorted(_CAT)
MESSAGE = []
for i, cat in enumerate(CATEGORIES, start=1):
    MESSAGE.append('%d: %s' % (i, cat))
MESSAGE = '\n'.join(MESSAGE)

TRANS = '''
Account:     %s
Date:        %s
Description: %s
Amount:      %s
'''[1:-1]

def categorise(accounts):
    for account in accounts:
        for trans in account.trans:
            if trans.category:
                continue

            print('\n', MESSAGE, '\n', sep='')
            print(TRANS % (trans.account.name,
                           trans.date.strftime('%d/%m/%y'),
                           trans.desc, trans.amount), '\n', sep='')

            while True:
                try:
                    response = raw_input('Category: ')
                    if response:
                        trans.category = CATEGORIES[int(response) - 1]
                except KeyboardInterrupt:
                    print('\nStopping.')
                    return
                except:
                    print('Illegal input.')
                else:
                    break


