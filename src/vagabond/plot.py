from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from matplotlib import dates
from matplotlib import rc
from matplotlib import pyplot

import numpy

def plot(book):
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

