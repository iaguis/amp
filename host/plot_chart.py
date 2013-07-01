#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""plot_chart.py plots a stack chart from memory usage data in
   csv files generated by process.logs.py"""

__author__ = "Iago López Galeiras"

import numpy as np
import matplotlib.pyplot as plt
import sys
from itertools import chain

colors = ['#FF0001',
          '#BF3030',
          '#A60000',
          '#FF4040',
          '#FF7373',
          '#FF7400',
          '#BF7130',
          '#A64B00',
          '#FF9640',
          '#FFB273',
          '#CD0074',
          '#992667',
          '#85004B',
          '#E6399B',
          '#E667AF',
          '#00CC00',
          '#269926',
          '#008500',
          '#39E639',
          '#67E667']

tooltip = None

def get_stats_from_csv(filename):
    f = open(filename)
    stats = []
    for l in f:
        measurement = []
        line = [x.strip() for x in l.split(',')]
        measurement.append(line[0])
        processes_dict = {}
        for i in range(1,len(line)-1,2):
            processes_dict[line[i]] = line[i+1]
        measurement.append(processes_dict)
        measurement = tuple(measurement)
        stats.append(measurement)

    f.close()
    all_processes = get_all_processes(stats)
    fix_stats(stats, all_processes)
    stats.sort(key=lambda x: x[0])
    return stats, all_processes

def fix_stats(stats, all_processes):
    """include processes not present at a time with memory usage = 0"""
    for el in stats:
        for p in all_processes:
            if not p in el[1].keys():
                el[1][p] = 0

def get_all_processes(stats):
    """get all the processes ever started"""
    return list(set(list(chain.from_iterable([s[1].keys() for s in stats]))))

def plot_stats(stats, all_processes):
    uptime_arr = np.array([s[0] for s in stats], float)
    # convert to minutes
    uptime_arr = uptime_arr/60000
    procs = []

    for proc_name in all_processes:
        procs.append((proc_name, [float(s[1][proc_name]) for s in stats]))

    # sort depending on total memory usage
    procs, sorted_processes = zip(*[(x, y) for (x, y) in sorted(zip(procs, all_processes), key=lambda (x, y): sum(x[1]), reverse=True)])

    def onpick(event):
        global tooltip
        thisline = event.artist

        # get process index depending on label number
        label = thisline.get_label()
        proc_index = int(label[11:])

        # selected process
        process = sorted_processes[proc_index]

        if tooltip:
            tooltip.remove()
        tooltip = ax.text(event.mouseevent.xdata, event.mouseevent.ydata, process, style='italic',
        bbox={'facecolor':'yellow', 'alpha':1, 'pad':10})
        event.canvas.draw()

    procs = np.array([pr[1] for pr in procs])

    colormap = colors[:len(procs)]

    fig = plt.figure(figsize=(1,1), dpi=80)
    ax = fig.add_subplot(111)

    ax.stackplot(uptime_arr, procs, colors=colormap, picker=True, edgecolor = "none")
    fig.canvas.mpl_connect('pick_event', onpick)

    plt.xlabel('Uptime, minutes')
    plt.ylabel('Memory usage, KB')
    plt.title('Memory usage vs Uptime')

    plt.show()

if __name__=="__main__":
    if len(sys.argv) != 2:
        print "Usage: plot_chart.py stats_file.csv"
        exit(0)

    stats, all_processes = get_stats_from_csv(sys.argv[1])
    plot_stats(stats, all_processes)