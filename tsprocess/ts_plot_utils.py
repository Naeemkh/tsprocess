"""
ts_plot_utils.py
====================================
The core module for timeseries plot helper functions.
"""

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.font_manager import FontProperties

from .ts_utils import check_opt_param_minmax, query_opt_params


def plot_velocity_helper(record, color_code, opt_params, list_inc, list_process):
    """ """
    # fig = plt.figure()
    with_details = False
    if query_opt_params(opt_params, 'save_figure'):  
        nrs = 7          
        fig, axarr = plt.subplots(nrows=nrs, ncols=3, figsize=(14, 9))
        counter = 2
        rspan = 2
        with_details = True
    else:
        nrs = 3
        fig, axarr = plt.subplots(nrows=nrs, ncols=3, figsize=(14, 9))
        counter = 1
        rspan = 1

    
    # h1, h2, UD
    for i in range(3):
        axarr[i][0] = plt.subplot2grid((nrs,3),(i*counter,0),rowspan=rspan, colspan=2)
        axarr[i][1] = plt.subplot2grid((nrs,3),(i*counter,2),rowspan=rspan, colspan=1)
        axarr[i][0].grid(True)
    
    if with_details:
        axarr[3][0] = plt.subplot2grid((7,3),(6,0),rowspan=1, colspan=3)
    
    x_lim_f = check_opt_param_minmax(opt_params, 'zoom_in_freq')
    x_lim_t = check_opt_param_minmax(opt_params, 'zoom_in_time')
    station_name = None
    epicentral_dist = None               
    for i,item in enumerate(record):
        if not item:
            continue
        axarr[0][0].plot(item.time_vec,item.vel_h1.value,
         color_code[i], label=list_inc[i])
        axarr[0][1].plot(item.freq_vec,abs(item.vel_h1.fft_value),
         color_code[i], label=list_inc[i])   
        axarr[1][1].plot(item.freq_vec,abs(item.vel_h2.fft_value),
         color_code[i], label=list_inc[i])  
        axarr[1][0].plot(item.time_vec,item.vel_h2.value,
         color_code[i], label=list_inc[i])
        axarr[2][0].plot(item.time_vec,item.vel_ver.value,
         color_code[i], label=list_inc[i])
        axarr[2][1].plot(item.freq_vec,abs(item.vel_ver.fft_value),
         color_code[i], label=list_inc[i])   
        # station name
        if not station_name:
            station_name = item.station.inc_st_name[list_inc[i]]
        
        # epicentral distance
        if not epicentral_dist:
            epicentral_dist = f"{item.epicentral_distance: 0.2f}"
    
    if with_details:
        footnote_font = FontProperties()
        footnote_font.set_family('sans-serif')
        footnote_font.set_name('Courier')
        footnote_font.set_size(10)
        max_height = 50 
        axarr[3][0].text(1,0.8 * max_height,"Processing details go here", fontproperties = footnote_font)
        
        axarr[3][0].set_xlim([0,50])
        axarr[3][0].set_ylim([0,50])
        axarr[3][0].get_xaxis().set_ticks([])
        axarr[3][0].get_yaxis().set_ticks([])
    
    for i in range(3):
    
        axarr[i][0].set_xlim(x_lim_t)
    
        axarr[i][1].set_xlim(x_lim_f)
    
    axarr[0][0].legend()
    axarr[0][0].set_title(
        f'Station at incident {list_inc[0]}:'
        f'{station_name} - epicenteral dist:'
        f'{epicentral_dist} km'
        )    
    
    fig.tight_layout()  

    return fig
