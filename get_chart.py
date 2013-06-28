#!/usr/bin/env python

import glob
import re
from itertools import chain
import numpy as np
import matplotlib.pyplot as plt
import sys

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

def get_processes(file_name):
    """get processes at a time"""
    f = open(file_name)
    content = f.read()
    process_list =  list(set(re.findall(r"kB: ((?:(?:\w+)\.?)+) \(", content)))
    f.close()
    return process_list

def get_mem_from_processes(processes, file_name):
    """get memory usage for processes at a time"""
    f = open(file_name)
    content = f.read()
    stats = {}
    for proc in processes:
        search_string = "(\d+) kB: (" + proc + ")"
        mem_proc = re.search(search_string, content)
        mem = mem_proc.group(1)
        proc = mem_proc.group(2)
        stats[proc] = mem
    f.close()
    return stats

def get_uptime(file_name):
    """get uptime at a time"""
    f = open(file_name)
    content = f.read()
    uptime = re.search(r"Uptime: (\d+)", content).group(1)
    f.close()
    return uptime

def get_stats(directory):
    """get stats from a log directory"""
    all_stats = []

    for f in glob.glob(directory + "/*.log"):
        stats = get_mem_from_processes(get_processes(f), f)
        uptime = get_uptime(f)
        all_stats.append((uptime, stats))

    fix_stats(all_stats)
    all_stats.sort(key=lambda x: x[0])

    return all_stats

def get_all_processes(stats):
    """get all the processes ever started"""
    return list(set(list(chain.from_iterable([s[1].keys() for s in stats]))))

def fix_stats(stats):
    """include processes not present at a time with memory usage = 0"""
    for el in stats:
        for p in get_all_processes(stats):
            if not p in el[1].keys():
                el[1][p] = 0

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

    # remove black borders
    ax.xaxis.set_ticks([])
    ax.yaxis.set_ticks([])
    for spine in ax.spines.itervalues():
        spine.set_visible(False)

    ax.stackplot(uptime_arr, procs, colors=colormap, picker=True, edgecolor = "none")
    fig.canvas.mpl_connect('pick_event', onpick)

    plt.xlabel('Uptime, minutes')
    plt.ylabel('Memory usage, KB')
    plt.title('Memory usage vs Uptime')

    plt.show()

if __name__=="__main__":
    if len(sys.argv) != 2:
        print "Usage: get_chart.py log-directory"
        exit(0)

    stats = get_stats(sys.argv[1])
    processes = get_all_processes(stats)
    plot_stats(stats, processes)
