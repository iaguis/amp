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
    get_procs_str = "\d+[ \t]+\d+K[ \t]+\d+K[ \t]+\d+K[ \t]+\d+K[ \t]+((?:[/]?(?:\w+)[/]?\.?)+)"
    process_list = list(set(re.findall(get_procs_str, content)))
    f.close()
    return process_list

def get_mem_from_processes(processes, file_name):
    """get memory usage for processes at a time"""
    f = open(file_name)
    content = f.read()
    stats = {}
    procs_mem = 0
    for proc in processes:
        search_string = "\d+[ \t]+\d+K[ \t]+\d+K[ \t]+(\d+)K[ \t]+\d+K[ \t]+(" + proc + ")"
        mem_proc = re.search(search_string, content)
        mem = mem_proc.group(1)
        proc = mem_proc.group(2)
        stats[proc] = mem
        procs_mem += int(mem)
    total_mem = re.search("RAM: (\d+)K", content).group(1)
    free_mem = re.search("MemFree:[ \t]+(\d+) kB", content).group(1)
    buffers_mem = re.search("Buffers:[ \t]+(\d+) kB", content).group(1)
    cached_mem = re.search("Cached:[ \t]+(\d+) kB", content).group(1)
    slab_mem = re.search("Slab:[ \t]+(\d+) kB", content).group(1)
    sh_mem = re.search("Shmem:[ \t]+(\d+) kB", content).group(1)

    stats["Free"] = free_mem
    stats["Buffers"] = buffers_mem
    stats["Cached"] = cached_mem
    stats["Slab"] = slab_mem
    stats["Shmem"] = sh_mem
    stats["Unknown"] = int(total_mem) - int(free_mem) - procs_mem - int(buffers_mem) - \
    int(cached_mem) - int(sh_mem) - int(slab_mem)
    f.close()
    return stats

def get_date(file_name):
    """get date at a time"""
    f = open(file_name)
    content = f.read()
    date = re.search(r"Date: (\d+)", content).group(1)
    f.close()
    return date

def process_logs(directory, output_file):
    out = open(output_file, "w")

    lines = []
    for f in glob.glob(directory + "/*.log"):
        stats = get_mem_from_processes(get_processes(f), f)
        date = get_date(f)
        line = str(date)
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
