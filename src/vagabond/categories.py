from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

CATEGORIES = {
    'ATM',
    'Charity',
    'Council tax',
    'Eating out',
    'Education',
    'Entertainment',
    'Fashion',
    'Foxdog Studios',
    'Gifts',
    'Going out',
    'Groceries',
    'Income tax',
    'Household',
    'Interest',
    'Living',
    'National insurance',
    'Phone',
    'Utilities',
    'Rent',
    'Student loan',
    'Technology',
    'Travel',
    'Vechicle costs',
    'Vehicle insurance',
    'Vehicle tax',
    'Wages'
}

def _init():
    import re
    import sys

    this_module = sys.modules[__name__]
    subber = re.compile(r'[^a-z0-9_]+', flags=re.IGNORECASE).sub

    for cat in CATEGORIES:
        if not cat[0].isalpha() and not cat.startswith('_'):
            raise ValueError('Category name cannot start with digit')
        cat_var_name = subber('_', cat).upper()
        if hasattr(this_module, cat_var_name):
            raise ValueError('Transformed category name must be unique (have '
                             'a look at your non-alphanumeric characters)')
        setattr(this_module, cat_var_name, cat)

_init()
del _init

