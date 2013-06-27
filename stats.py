#!/usr/bin/env python

import glob
import re
from itertools import chain
import numpy as np
import matplotlib.pyplot as plt
import sys

def get_processes(file_name):
    f = open(file_name)
    content = f.read()
    process_list =  list(set(re.findall(r"kB: ((?:(?:\w+)\.?)+) \(", content)))
    f.close()
    return process_list

def get_mem_from_processes(processes, file_name):
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
    f = open(file_name)
    content = f.read()
    uptime = re.search(r"Uptime: (\d+)", content).group(1)
    f.close()
    return uptime

def get_stats(directory):
    all_stats = []

    for f in glob.glob(directory + "/*.log"):
        stats = get_mem_from_processes(get_processes(f), f)
        uptime = get_uptime(f)
        all_stats.append((uptime, stats))

    fix_stats(all_stats)
    all_stats.sort(key=lambda x: x[0])

    return all_stats

def get_all_processes(stats):
    return list(set(list(chain.from_iterable([s[1].keys() for s in stats]))))

def fix_stats(stats):
    for el in stats:
        for p in get_all_processes(stats):
            if not p in el[1].keys():
                el[1][p] = 0

colors = \
    ['#FF0000',
    '#00FF00',
    '#0000FF',
    '#FFFF00',
    '#FF00FF',
    '#00FFFF',
    '#000000',
    '#800000',
    '#008000',
    '#000080',
    '#808000',
    '#800080',
    '#008080',
    '#808080',
    '#C00000',
    '#00C000',
    '#0000C0',
    '#C0C000',
    '#C000C0',
    '#00C0C0',
    '#C0C0C0',
    '#400000',
    '#004000',
    '#000040',
    '#404000',
    '#400040',
    '#004040',
    '#404040',
    '#200000',
    '#002000',
    '#000020',
    '#202000',
    '#200020',
    '#002020',
    '#202020',
    '#600000',
    '#006000',
    '#000060',
    '#606000',
    '#600060',
    '#006060',
    '#606060',
    '#A00000',
    '#00A000',
    '#0000A0',
    '#A0A000',
    '#A000A0',
    '#00A0A0',
    '#A0A0A0',
    '#E00000',
    '#00E000',
    '#0000E0',
    '#E0E000',
    '#E000E0',
    '#00E0E0',
    '#E0E0E0']

txt = None


def plot_stats(stats, all_processes):
    uptime_arr = np.array([s[0] for s in stats], float)
    uptime_arr = uptime_arr/60000
    procs = []

    for proc_name in all_processes:
        procs.append((proc_name, [float(s[1][proc_name]) for s in stats]))

    sorted_processes = [y for (x, y) in sorted(zip(procs, all_processes), key=lambda (x, y): sum(x[1]), reverse=True)]

    def onpick3(event):
        global txt
        thisline = event.artist
        label = thisline.get_label()
        proc_index = int(label[11:])
        process = sorted_processes[proc_index]
        if txt:
            txt.remove()
        txt = ax.text(event.mouseevent.xdata, event.mouseevent.ydata, process, style='italic',
        bbox={'facecolor':'red', 'alpha':1, 'pad':10})
        event.canvas.draw()

    procs.sort(key=lambda x: sum(x[1]), reverse=True)

    procs = np.array([pr[1] for pr in procs])

    fig = plt.figure(figsize=(1,1), dpi=80)
    ax = fig.add_subplot(111)
    ax.stackplot(uptime_arr, procs, picker=True)
    fig.canvas.mpl_connect('pick_event', onpick3)

    plt.xlabel('Uptime, minutes')
    plt.ylabel('Memory usage, KB')
    plt.title('Memory usage vs Uptime')

    plt.show()

if __name__=="__main__":
    if len(sys.argv) != 2:
        print "Usage: stats.py log-directory"
        exit(0)

    stats = get_stats(sys.argv[1])
    processes = get_all_processes(stats)
    plot_stats(stats, processes)
