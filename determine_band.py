"""
    Scripts to determine the band corresponding to a given frequency range.

    Last updated: 27/08/2024        
    Author: Sandra Snyman
"""

import numpy as np

# result_band determines the band corresponding to the user-provided start and stop frequencies
def result_band(start_freq, stop_freq):
    """[Summary]

    :param [ParamName]: [ParamDescription], defaults to [DefaultParamVal]
    :type [ParamName]: [ParamType](, optional)
    ...
    :raises [ErrorType]: [ErrorDescription]
    ...
    :return: [ReturnDescription]
    :rtype: [ReturnType]
    """
    bands = np.zeros((7,3))
    bands[0][0] = 20
    bands[0][1] = 800
    bands[0][2] = 0
    bands[1][0] = 700
    bands[1][1] = 1100
    bands[1][2] = 1
    bands[2][0] = 1000
    bands[2][1] = 1700
    bands[2][2] = 2
    bands[3][0] = 1540
    bands[3][1] = 2060
    bands[3][2] = 3
    bands[4][0] = 1900
    bands[4][1] = 2600
    bands[4][2] = 4
    bands[5][0] = 2414
    bands[5][1] = 2985
    bands[5][2] = 5
    bands[6][0] = 2800
    bands[6][1] = 3500
    bands[6][2] = 6

    correct_band = None
    for band in bands:
        if start_freq>=band[0] and stop_freq<=band[1]:
            if correct_band is None:
                correct_band = band[2]
                print("Frequency band = ", str(int(correct_band)))
            else:
                print("Multiple bands match")
    if correct_band is None: print("No bands match")
    return int(correct_band)

# station_band determines the band corresponding to the specific h5 file frequency range
def station_band(start_freq, stop_freq):
    bands = np.zeros((7,3))
    bands[0][0] = 20
    bands[0][1] = 800
    bands[0][2] = 0
    bands[1][0] = 700
    bands[1][1] = 1100
    bands[1][2] = 1
    bands[2][0] = 1000
    bands[2][1] = 1700
    bands[2][2] = 2
    bands[3][0] = 1540
    bands[3][1] = 2060
    bands[3][2] = 3
    bands[4][0] = 1900
    bands[4][1] = 2600
    bands[4][2] = 4
    bands[5][0] = 2414
    bands[5][1] = 2985
    bands[5][2] = 5
    bands[6][0] = 2800
    bands[6][1] = 3500
    bands[6][2] = 6

    correct_band = None
    for band in bands:
        if (start_freq>=band[0]-200) and (stop_freq<=band[1]+200):
            if correct_band is None:
                correct_band = band[2]
                # print("Station band = ", str(int(correct_band)))
            else:
                print("Multiple bands match")
    if correct_band is None: print("No bands match")
    return int(correct_band)

def resample(freq_range, start_freq, stop_freq, wfall_data, to_data):
    max_start_freq = 0
    min_stop_freq = 1e9
    min_num_samples = 1e9
    for freqs in freq_range:
        num_samples = len(freqs)
        if freqs[0]>max_start_freq:
            max_start_freq = freqs[0]
        if freqs[-1]<min_stop_freq:
            min_stop_freq = freqs[-1]
        if len(freqs)<min_num_samples:
            min_num_samples = len(freqs)

    new_freq = np.linspace(max_start_freq, min_stop_freq, min_num_samples)

    difference_array = np.absolute(new_freq-start_freq)
    start_index = difference_array.argmin()
    difference_array = np.absolute(new_freq-stop_freq)
    stop_index = difference_array.argmin()

    new_wfall_data = []
    new_to_data = []
    for i,freq in enumerate(freq_range):
        wfall_datum = np.interp(new_freq, freq_range[i], wfall_data[i])
        new_wfall_data.append(wfall_datum[start_index:stop_index])
        to_datum = np.interp(new_freq, freq_range[i], to_data[i])
        new_to_data.append(np.max(to_datum[start_index:stop_index]))            

    return new_freq[start_index:stop_index], new_wfall_data, new_to_data