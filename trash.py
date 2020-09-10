import numpy as np
import pandas as pd
from calendar import timegm
from datetime import date
import time
from os import path
from libs_persistence import simple, xcorr_tim
from obs_dhm import observe_clim

#   Hydrograph separation plot
dt_ini1 = date(2008, 9, 1)  
dt_end1 = date(2008, 11, 1)  

for k in range(len(link_list[0])):
    code = link_list[0][k]
    A = area[0][k]/1.609**2
    size = hysep_window(A)
    ts = observe_clim(path.join(data_dir, basins[0]), code)
    id1 = np.where(ts['yr'] == 2008)[0][0]
    id2 = np.where(ts['yr'] == 2008)[0][-1]
    dates = [date(ts['yr'][k], ts['mon'][k], ts['day'][k]) for k in range(len(ts))]
    data = pd.Series(ts['Q'].values, name = 'discharge', index = ts.index)
    b, q = sliding_interval_filter(data, size) # choose the method of separation
    q_r = simple(q.values, 1)  # Define persistence method 
    # unix = [timegm(x.timetuple()) for x in dates]
    # obss = [(unix[x], q.values[x]) for x in range(len(unix))]
    # tsim_unix, q_r = simple_flat_mod(obss, 3)  # Define persistence method
    # date_qr = [datetime.utcfromtimestamp(y) for y in tsim_unix]
    # id11 = np.where(np.array([x.year for x in date_qr]) == 2008)[0][0]
    # id22 = np.where(np.array([x.year for x in date_qr]) == 2008)[0][-1]
    
    plt.style.use('seaborn-white')
    fig = plt.figure(figsize=(7, 4))
    ax0 = fig.add_subplot(111)
    ax0.grid()
    ax0.set_facecolor((0.94,0.94,0.94))
    # lns1 = plt.plot(dates[id1:id2], np.array(ts['Q'].values)[id1:id2], 'k-', markersize = 1, 
    #                 label= 'Streamflow') 
    lns2 = plt.plot(dates[id1:id2], np.array(q.values)[id1:id2], 'k-', markersize = 1, label= 'Observed flow') 
    lns3 = plt.plot(dates[id1:id2], np.array(q_r)[id1:id2], 'b-', markersize = 1, label= 'Forecasted flow') 

#    lns3 = plt.plot(dates[-365:], b[-365:], 'b-', markersize = 1, label= 'Base Flow') 
    # ax0.fill_between(dates[id1:id2], b[id1:id2], color = 'b', label = 'Base Flow')
    plt.xlabel(r'Date')
    plt.ylabel(r'Discharge [$m^3/s$]')
    ax0.xaxis.label.set_size(13)
    ax0.yaxis.label.set_size(13)
    ax0.xaxis.set_major_locator(mdates.DayLocator(interval = 14))
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m-%d')) # only for monthly scales
    plt.tick_params(axis='both', which='major', labelsize=13, pad = 10)
    plt.ylim(0, 10000)
    plt.xlim(dt_ini1, dt_end1)
    # plt.legend(loc='upper right', frameon = True, fancybox = True, 
    #       borderpad = 0.5, fontsize=10)
    #plt.show()
    DPI = 300
    plt.savefig(path.join(plt_dir, code + '_sliding_hysep_42890.png'),
                dpi=DPI, bbox_inches='tight', pad_inches=0.25)
    plt.close()
    
#%%


