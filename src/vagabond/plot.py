from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import time

from matplotlib import dates
from matplotlib import rc
from matplotlib import pyplot

import numpy

from vagabond import Accounts

def plot(accounts, forgetting_factor=Accounts.DEF_FORGETTING_FACTOR):
    rc('font', family='serif')
    rc('text', usetex=True)
    data = numpy.array(accounts.get_balance_data())
    c, m = accounts.compute_saving_line(forgetting_factor=forgetting_factor)
    predict_dates = numpy.array((data[:,0].min(), data[:,0].max()))
    predict_unix = numpy.array([time.mktime(d.timetuple())
                                for d in predict_dates])
    predict_savings = predict_unix * m + c
    fig = pyplot.figure()
    plot = fig.add_subplot(111)
    plot.plot_date(data[:,0], data[:,1], drawstyle='steps-mid', fmt='b-',
                   label='Actual')
    plot.plot_date(predict_dates, predict_savings, fmt='r-', label='Forecast')
    plot.xaxis.set_major_locator(dates.MonthLocator())
    plot.xaxis.set_major_formatter(dates.DateFormatter('%b'))
    plot.grid(True)
    plot.set_title('Savings over time')
    plot.set_xlabel('Date')
    plot.set_ylabel(r'Savings (\textsterling)')
    plot.set_ylim((data[:,1].min(), data[:,1].max()))
    handles, labels = plot.get_legend_handles_labels()
    plot.legend(handles[::-1], labels[::-1])
    pyplot.show()

