from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import time

from matplotlib import dates
from matplotlib import rc
from matplotlib import pyplot

import numpy

def plot(accounts):
    rc('font', family='serif')
    rc('text', usetex=True)
    data = numpy.array(accounts.get_balance_data())
    m, c = accounts.compute_saving_line()
    predict_dates = numpy.array((data[:,0].min(), data[:,0].max()))
    predict_unix = numpy.array([time.mktime(d.timetuple())
                                for d in predict_dates])
    predict_savings = predict_unix * m + c
    fig = pyplot.figure()
    plot = fig.add_subplot(111)
    plot.plot_date(data[:,0], data[:,1], drawstyle='steps-mid', fmt='b-')
    plot.plot_date(predict_dates, predict_savings, fmt='r-')
    plot.xaxis.set_major_locator(dates.MonthLocator())
    plot.xaxis.set_major_formatter(dates.DateFormatter('%b'))
    plot.grid(True)
    plot.set_title('Savings over time')
    plot.set_xlabel('Date')
    plot.set_ylabel(r'Savings (\textsterling)')
    pyplot.show()

