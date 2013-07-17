Android Memory Plotter
======================

Android Memory Plotter (AMP) collects memory usage info from an Android device
and generates a stack plot of memory usage vs. uptime of all Android processes
running allowing to see graphically how memory usage of each process changes
while using the device.

Inspired by:

http://heap-of-notes.blogspot.de/2013/05/investigation-of-android-apps-memory.html

Screenshot
----------

![sample screenshot](https://raw.github.com/iaguis/amp/master/screenshots/sample.png)

Dependencies
------------

- Python
- Matplotlib >= 1.2
- Numpy
- Android SDK

It was found that in some setups matplotlib didn't show anything. The problem
was solved by adding to the file ~/.matplotlib/matplotlibrc the line:

backend : Qt4Agg

Reference: http://stackoverflow.com/a/7534680

Utilities
---------

* amp_start_measuring.sh measure time

    * Starts collecting memory usage logs for "time" seconds

* amp_get_logs.sh measure_name output_dir

    * Gets the memory usage logs identified by "measure_name" from the device to
      "output_dir"

* amp_clean_logs.sh

    * Cleans memory usage logs from the device

* amp_process_logs.py log_dir output_file.csv

    * Process memory usage logs and generates an "output_file.csv"

* amp_plot_chart.py data_file.csv

    * Plots memory usage from a csv file

