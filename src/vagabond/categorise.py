from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import logging
import re

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

def categorise(accounts):
    bags, cat_probs = calculate_bags_of_words(accounts)
    for account in accounts:
        for trans in account.trans:
            if trans.category:
                continue
            print('\n', MESSAGE, '\n', sep='')
            print(TRANS % (trans.account.name,
                           trans.date.strftime('%d/%m/%y'),
                           trans.desc, trans.amount), '\n', sep='')

            while True:
                words = set(filter(lambda x: x in bags,
                                   splitter(trans.desc)))
                logging.debug(words)
                likelihoods = dict((cat, cat_probs[cat]) for cat in CATEGORIES)
                for word in words:
                    bag = bags[word]
                    for cat, prob in bag.iteritems():
                        likelihoods[cat] *= prob
                words_significance = sum(likelihoods.itervalues())
                probs = {}
                for cat, likelihood in likelihoods.iteritems():
                    probs[cat] = likelihood / words_significance
                logging.debug(sorted(probs.iteritems(),
                                     key=lambda (cat, val) : val,
                                     reverse=True))
                most_likely_cat = max(probs, key=lambda cat: probs[cat])
                try:
                    response = raw_input('Category [%s] (%s to refresh '
                                         'VAG-BRAIN): '
                                         % (most_likely_cat, REFRESH_KEY))
                    if response:
                        if response == REFRESH_KEY:
                            bags, cat_probs = calculate_bags_of_words(accounts)
                            continue
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

splitter = re.compile('[^a-z]+', flags=re.IGNORECASE).split

def calculate_bags_of_words(accounts):
    bags = {}
    cat_probs = dict((cat, 1) for cat in CATEGORIES)
    total_trans = 0
    for account in accounts:
        for tran in account.trans:
            total_trans += 1
            category = tran.category
            if not category:
                continue
            cat_probs[category] += 1
            words = set(filter(None, splitter(tran.desc)))
            for word in words:
                if word not in bags:
                    bags[word] = dict((cat, 1) for cat in CATEGORIES)
                bags[word][category] += 1
    for bag in bags.itervalues():
        total = sum(bag.itervalues())
        for word in bag:
            bag[word] /= total
    for cat in cat_probs:
        cat_probs[cat] /= total_trans
    return bags, cat_probs

