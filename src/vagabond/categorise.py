from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import logging
import re

from fds.classification import BagOfWords

from vagabond.categories import CATEGORIES as _CAT

CATEGORIES = sorted(_CAT)
MESSAGE = []
for i, cat in enumerate(CATEGORIES, start=1):
    MESSAGE.append('%2d: %s' % (i, cat))
MESSAGE = '\n'.join(MESSAGE)

TRANS = '''
Account:     %s
Date:        %s
Description: %s
Amount:      %s
'''[1:-1]

REFRESH_KEY = 'r'
SKIP_KEY = 's'

splitter = re.compile('[^a-z]+', flags=re.IGNORECASE).split

def categorise(accounts):
    classifier = create_classifier(accounts)
    print(classifier)
    for account in accounts:
        for trans in account.trans:
            if trans.category:
                continue

            print('\n', MESSAGE, '\n', sep='')
            print(TRANS % (trans.account.name,
                           trans.date.strftime('%d/%m/%y'),
                           trans.desc, trans.amount), '\n', sep='')

            words = set(filter(lambda x: x in classifier.dictionary,
                               splitter(trans.desc)))

            while True:
                most_likely_cat = classifier.classify(words)

                try:
                    response = raw_input('Category [%s] (%s to refresh '
                                         'VAG-BRAIN): '
                                         % (most_likely_cat, REFRESH_KEY))
                    if response:
                        if response == REFRESH_KEY:
                            classifier = create_classifier(accounts)
                            continue
                        elif response == SKIP_KEY:
                            break
                        trans.category = CATEGORIES[int(response) - 1]
                    else:
                        trans.category = most_likely_cat

                except KeyboardInterrupt:
                    print('\nStopping.')
                    return
                except:
                    print('Illegal input.')
                else:
                    break

def create_classifier(accounts):
    dictionary = set()
    training_examples = []
    for account in accounts:
        for trans in account.trans:
            if not trans.category:
                continue
            words = splitter(trans.desc)
            for word in words:
                dictionary.add(word)
            training_examples.append((trans.category, words))
    return BagOfWords(CATEGORIES, dictionary, training_examples,
                      smoothing=1)

