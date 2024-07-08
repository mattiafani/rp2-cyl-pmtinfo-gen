#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 26 12:37:29 2024

@author: Mattia Fanì (UMN) - mattia.fani@cern.ch

"""

from pathlib import Path
from math import sqrt as sqrt

# import math


def create_plots_dir(R, H):
    plots_directory = Path(f"./Plots/Plots_R{R}_H{H}")

    if not plots_directory.exists():
        plots_directory.mkdir(parents=True, exist_ok=True)
        print(f"The directory '{plots_directory}' has been created.")

    return plots_directory


def get_spacing(n_rows, n_cols, C, H):
    row_spacing = round(H / n_rows, 1)
    col_spacing = round(C / n_cols, 1)

    return row_spacing, col_spacing


def find_nrows_ncols(C, H, r, nL):
    ratio = C / H

    n_cols = round(sqrt(nL * ratio))
    n_rows = round(nL / n_cols)
    n_PMTs_L = n_cols * n_rows

    row_spacing, col_spacing = get_spacing(n_rows, n_cols, C, H)

    if row_spacing < 2 * r or col_spacing < 2 * r:
        print("\nWARNING! PMT size exceeds spacing\n")
        print(f"PMT diameter = {2*r}; Column spacing = {col_spacing}, Row spacing = {row_spacing})")

    return n_rows, n_cols


def store_list_to_txtfile(listname, file_name, R, H):
    plots_directory = create_plots_dir(R, H)
    filename = f"{plots_directory}/{file_name}.txt"

    with open(filename, "w") as file:
        file.write("[")
        for element in listname:
            file.write(str(element) + ",")
        file.write("]")

    print(f"{file_name} data has been saved to file ", filename)


def write_PMTINFO_file(file_name, x, y, z, dir_x, dir_y, dir_z, pmt_type, R, H):
    plots_directory = create_plots_dir(R, H)
    filename = f"{plots_directory}/{file_name}.ratdb"
    with open(filename, "w") as file:
        file.write("{")
        file.write(f"\n// total number of inner PMTs: {len(x)}\n")
        file.write(f'"name": "{file_name}",\n')
        file.write('"valid_begin": [0, 0],\n')
        file.write('"valid_end": [0, 0],\n')

        file.write('"x": ')
        file.write("[")
        for element in x:
            file.write(str(element) + ",")
        file.write("],\n")
        print(f"len(x) = {len(x)} elements")

        file.write('"y": ')
        file.write("[")
        for element in y:
            file.write(str(element) + ",")
        file.write("],\n")
        print(f"len(y) = {len(y)} elements")

        file.write('"z": ')
        file.write("[")
        for element in z:
            file.write(str(element) + ",")
        file.write("],\n")
        print(f"len(z) = {len(z)} elements")

        file.write('"dir_x": ')
        file.write("[")
        for element in dir_x:
            file.write(str(element) + ",")
        file.write("],\n")
        print(f"len(dir_x) = {len(dir_x)} elements")

        file.write('"dir_y": ')
        file.write("[")
        for element in dir_y:
            file.write(str(element) + ",")
        file.write("],\n")
        print(f"len(dir_y) = {len(dir_y)} elements")

        file.write('"dir_z": ')
        file.write("[")
        for element in dir_z:
            file.write(str(element) + ",")
        file.write("],\n")
        print(f"len(dir_z) = {len(dir_z)} elements")

        file.write('"pmt_type": ')
        file.write("[")
        for element in pmt_type:
            file.write(str(element) + ",")
        file.write("]\n")
        file.write("}")
        print(f"len(pmt_type) = {len(pmt_type)} elements")

    print(f"{file_name} data has been saved to file ", filename)
