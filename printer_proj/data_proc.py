#!/usr/bin/env python3
"""
data_proc.py
Demo including:
 - reading data from a csv
 - deleting unnecessary data from initial file
 - plotting the results
"""

from __future__ import print_function
import sys
import pandas as pd
from argparse import ArgumentParser
import numpy as np
import matplotlib.pyplot as plt
import os


SUCCESS = 0
INVALID_DATA = 1
IO_ERROR = 2

DEFAULT_DATA_FILE_NAME = 'printer_data.csv'


def warning(*objs):
    """Writes a message to stderr."""
    print("WARNING: ", *objs, file=sys.stderr)


def data_processing(data1):
    """
    Process initial data in 'Printer Data.csv' and export important data in a new csv called 'key_data'
    Data in 'Printer Data.csv' is collected from Oct 7, 2017 12:00:00 AM to Oct 8, 2018 12:43:05 PM
    :param base_f_name: 
    :param data_stats: 
    :return: 
    """
    data1.drop(['Printer Name', 'Color Pages', 'Grayscale Pages', 'Jobs', 'Avg. Pages', 'Total Printed Pages'], axis=1, inplace=True)
    data1.dropna(axis=0, how='any', inplace=True)
    #Export a new file 'key_data'
    key_data = data1
    key_data.to_csv('data/key_data.csv')
    # The columns of 'key_data' are
    #Index(['Duplex Pages', 'Simplex Pages', 'Location / Department'], dtype='object')
    return key_data

def parse_cmdline(argv):
    """
    Returns the parsed argument list and return code.
    `argv` is a list of arguments, or `None` for ``sys.argv[1:]``.
    """
    if argv is None:
        argv = sys.argv[1:]

    # initialize the parser object:
    parser = ArgumentParser(description='Reads in a csv. There must be the same number of values in each row.')
    parser.add_argument("-c", "--csv_data_file", help="The location (directory and file name) of the csv file with "
                                                      "data to analyze",
                        default=DEFAULT_DATA_FILE_NAME)
    args = None
    try:
        args = parser.parse_args(argv)
        args.csv_data = pd.read_csv("data/printer_data.csv")
    except IOError as e:
        warning("Problems reading file:", e)
        parser.print_help()
        return args, IO_ERROR
    except ValueError as e:
        warning("Read invalid data:", e)
        parser.print_help()
        return args, INVALID_DATA

    return args, SUCCESS

def plot(base_f_name, key_data):
    """
    :param:base_f_name: str of base output name (without extension)
    :param: key_data: includes printer usage data and printer locations
    :return: a png file
    """
    #Plot
    barWidth = 0.85
    names = key_data['Location / Department']
    simplex = key_data['Simplex Pages']
    duplex = key_data['Duplex Pages']
    key_data.plot(kind='bar',stacked=True, title='Busiest Printers in North Campus',
        #Bar colors are Michigan Blue and Maize
        alpha=0.85, color=['#00274C', '#FFCB05'], width=barWidth)
    plt.xlabel('Printer Location')
    plt.ylabel('The Amount of Pages')
    plt.xticks(fontsize='10')
    out_name = base_f_name + ".png"
    plt.savefig(out_name)

def main(argv=None):
    args, ret = parse_cmdline(argv)
    if ret != SUCCESS:
        return ret
    key_data = data_processing(args.csv_data)

    # get the name of the input file without the directory it is in, if one was specified
    base_out_fname = os.path.basename(args.csv_data_file)
    # get the first part of the file name (omit extension) and add the suffix
    base_out_fname = os.path.splitext(base_out_fname)[0] + '_stats'
    # add suffix and extension
    out_fname = base_out_fname + '.csv'
    np.savetxt(out_fname, key_data, delimiter=',', fmt='%s')
    print("Wrote file: {}".format(out_fname))

    # send the base_out_fname and data to a new function that will plot the data
    plot(base_out_fname, key_data)
    return SUCCESS  # success


if __name__ == "__main__":
    status = main()
    sys.exit(status)
