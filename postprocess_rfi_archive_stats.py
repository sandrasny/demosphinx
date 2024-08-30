"""
    Script that processes FMS RFI archive data over multiple months to generate a 
    waterfall plot and maximum hourly time occupancy plot over a long period.

    The 'stats_xx.spec.h5' files with daily data are processed.
    
    This script requires local copies of the various FMS RFI archive files.
    Required folder structure is ./station/year/month/stats_day.spec.h5, for example: ./ASC/2024/01/stats_01.spec.h5.

        ToDo:
            -   

    Last updated: 27/08/2024        
    Author: Sandra Snyman
"""

import matplotlib as mpl
import sys
import time
from datetime import datetime
import os
import h5py
import numpy as np
from matplotlib import cm, colors
from matplotlib import gridspec
import matplotlib.pyplot as plt
import RFIEq as rfi

try:
    print("Received Input:")
    print("MonthStart =", sys.argv[1])
    print("DayStart =", sys.argv[2])
    print("MonthEnd =", sys.argv[3])
    print("DayEnd =", sys.argv[4])
    print("FreqStart =", sys.argv[5])
    print("FreqEnd =", sys.argv[6])
    print("Station =", sys.argv[7])
except:
    print("Incorrect Input Parameters...")
    print("Required Input (all int, except station): MonthStart  DayStart  MonthEnd  DayEnd FreqStart  FreqEnd  Station (ASC, HERA, Losberg, VSK)")
    sys.exit(1)

year_list = ["2024"]
date_start = time.mktime((2024, int(sys.argv[1]), int(sys.argv[2]), 0, 0, 0, 0, 0, 0))
date_stop = time.mktime((2024, int(sys.argv[3]), int(sys.argv[4]), 0, 0, 0, 0, 0, 0))
start_freq = int(sys.argv[5])
stop_freq = int(sys.argv[6])
band = rfi.get_result_band(start_freq, stop_freq)
station = sys.argv[7]

for year in year_list:
    month_path = os.path.join("Data/" + station + "/" + ("%s" %year))
    # determine list of months with data available from the folders present in the year folder:
    month_list = os.listdir(month_path)
    time_range = []
    freq_range = []
    wfall_data = []
    to_data = []
    for month in month_list:
        day_path = os.path.join(month_path, "%s" %month)
        day_list = os.listdir(day_path)
        # determine list of days with data available from the .h5 files present in the month folder:
        day_list = sorted(map(lambda x: "%s" %("%02i" %int(x.split("_")[1])), [day.split(".")[0] for day in day_list if len(day.split(".")[0])>0 and day.split("_")[0]=="stats"]))
        for day in day_list:      
            # open .h5 file for this day    
            day_file = h5py.File(day_path + "/stats_" + day + ".spec.h5")
            date_tmp = time.mktime((int(year), int(month), int(day), 0, 0, 0, 0, 0, 0))
            # check if the current date falls within range requested by the user, continue to process and save the data
            # otherwise, ignore this date            
            if (date_tmp >= date_start) and (date_tmp <= date_stop):
                try:
                    # get frequency range, maximum and mean measured power, and time occupancy over frequency of one day
                    freq = day_file['freqs']['freqs-'+ str(band)][:]
                    max = day_file['max']['max-'+ str(band)][:]
                    mean = day_file['mean']['mean-'+ str(band)][:]
                    to = day_file['to']['to-'+ str(band)][:]

                    time_range.append(time.ctime(date_tmp))
                    to_data.append(to)
                    wfall_data.append(max)
                    freq_range.append(freq)                        
                except:
                    print("Band %s not observed on %s" %(str(band),datetime.strptime(time.ctime(date_tmp),"%a %b %d %H:%M:%S %Y").strftime('%d %b')))
            day_file.close()

# use the different frequency ranges from the .h5 files to determine a new frequency range
# resample the waterfall and time occupancy data accordingly
new_freq, new_wfall_data, new_to_data = rfi.resample(freq_range, start_freq, stop_freq, wfall_data, to_data)

# format date/time information for plotting
time_format = []
for date in time_range: 
    d = datetime.strptime(date,"%a %b %d %H:%M:%S %Y")
    time_format.append(d.strftime('%d %b'))

# X, Y, Z for waterfall plot
X = new_freq
Y = time_format
Z = np.array(new_wfall_data)

# scale date/time labels being plotted for readability
target = 40
label_inc = np.ceil(len(time_format)/target)
date_labels = time_format[::int(label_inc)]

# setup waterfall plot 
cmap = mpl.colormaps["inferno"]
zmin = np.mean(np.mean(Z, axis=0))
zmax = Z.max()
# zmin = -125
# zmax = -85
fig1, ax1 = plt.subplots()
wf = plt.pcolormesh(X, Y, Z, cmap=cmap, vmin=zmin, vmax=zmax)
wf.set_clim(zmin, zmax)
ax1.set_yticks(date_labels)
ax1.set_xticks(np.arange((np.round(X[0])), (np.round(X[-1])), int(np.ceil((X[-1] - X[0]) / 10.0))))
ax1.set_title("Maximum measured power at " + station)
ax1.set_xlabel("Frequency (MHz)")
plt.colorbar()
plt.show()

# setup time occupancy plot
fig2, ax2 = plt.subplots()
plt.plot(time_format, new_to_data)
ax2.set_title("Time occupancy at %s between %s and %s MHz" %(station, str(start_freq), str(stop_freq)))
ax2.set_ylabel("Maximum daily time occupancy (%)")
ax2.set_ylim(0, 100)
plt.xticks(date_labels, rotation ='vertical')
plt.show()
