#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""process_logs.py process memory usage data generated in target so that
plot_chart.py can generate a memory usage over time chart"""

__author__ = "Iago López Galeiras"

import glob
import re
import sys

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

def process_logs(directory, output_file):
    out = open(output_file, "w")

    lines = []
    for f in glob.glob(directory + "/*.log"):
        stats = get_mem_from_processes(get_processes(f), f)
        uptime = get_uptime(f)
        line = str(uptime)
        line += ","
        for proc in stats.keys():
            line += str(proc)
            line += ","
            line += str(stats[proc])
            line += ","
        line = line[:-1]
        line += "\n"
        lines.append(line)
    out.writelines(lines)
    out.close()


if __name__=="__main__":
    if len(sys.argv) != 3:
        print "Usage: process_logs.py log-directory output-file.csv"
        exit(0)

    process_logs(sys.argv[1], sys.argv[2])
