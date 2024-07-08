#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 15 23:59:20 2024

@author: Mattia Fanì (UMN) - mattia.fani@cern.ch
"""

import sys
import numpy as np
from math import pi, ceil
from utils import get_spacing, find_nrows_ncols, store_list_to_txtfile, write_PMTINFO_file
from generate_pmt_positions import generate_rectangle_positions, generate_lateral_positions, generate_circle_positions
from plot_all import plot_all
from store_info import store_positions_and_directions


def print_detector_info(R, H, C, S, V, STop, SLat):
    print(f"Detector dimensions: R = {R/1e3} m, H = {H/1e3} m; C = {round(C/1e3, 3)} m")
    print(f"Detector Surface = {round(S/1e6, 2)} m^2; Detector Volume = {round(V/1e9, 2)} m^3")
    print(f"Face surfaces: Top/Bot = {round(STop/1e6, 2)} m^2; Lateral = {round(SLat/1e6, 2)} m^2")


def calculate_pmt_coverage(coverage, S, s):
    npmts = coverage * S / s
    return ceil(npmts / 10) * 10


def calculate_pmt_fractions(S, STop, SLat, n):
    T = B = STop / S  # Fraction Top and Bottom surface
    L = SLat / S  # Fraction Lateral surface
    nT = round(n * T)
    nB = round(n * B)
    nL = round(n * L)
    return nT, nB, nL


def main(R, H, plot_nicer_plots, run_batch):
    print("\nDetermination of PMT positions - Cylindrical Detector\n")

    # Desired coverage
    coverage = 0.4  # [%]

    # PMTs - R7081
    r = 254  # [mm] 10"
    s = pi * r**2

    # Detector dimensions

    C = 2 * pi * R
    V = pi * R**2 * H
    S = 2 * pi * R * (H + R)
    STop = pi * R**2
    SLat = 2 * pi * R * H

    filename = f"Theia_Cyl_R{R}_H{H}"

    print_detector_info(R, H, C, S, V, STop, SLat)
    print(f"PMT radius = {r} mm")

    # Find number of PMTs to position
    n = calculate_pmt_coverage(coverage, S, s)
    print(f"Desired PMT coverage: {coverage * 100}%")
    print(f"\nRequired number of PMTs: {n}")

    # PMT fractions
    nT, nB, nL = calculate_pmt_fractions(S, STop, SLat, n)
    print(f" Top surface: {nT}\n Bottom surface: {nB}\n Lateral surface: {nL}\n PMTs to place: {nT + nB + nL}")

    #########################################################
    # PMT positions
    #########################################################

    # Lateral Surface
    print("\nLateral Surface")
    n_rows, n_cols = find_nrows_ncols(C, H, r, nL)
    row_spacing, col_spacing = get_spacing(n_rows, n_cols, C, H)
    print(f"Rows: {n_rows}, Columns: {n_cols}; Row spacing: {row_spacing} mm, Column spacing: {col_spacing} mm")

    # Top/Bot Surfaces
    print("\nTop/Bot Surface")
    n_circles = int(R / col_spacing)
    print(f"PMTs distributed in {n_circles} circles:")

    # Generate positions
    rectangle_positions = generate_rectangle_positions(n_rows, n_cols, C, H)
    lateral_positions, lateral_directions = generate_lateral_positions(R, H, n_rows, n_cols)
    top_positions, top_directions = generate_circle_positions(R, H, r, nT, n_circles, level=H / 2)
    bot_positions, bot_directions = generate_circle_positions(R, H, r, nB, n_circles, level=-H / 2)

    print("\nDistributed PMTs on the detector's inner surface: ")
    print(f" Top surface     : {len(top_positions)} PMTs")
    print(f" Lateral surface : {len(rectangle_positions)} PMTs")
    print(f" Bottom surface  : {len(bot_positions)} PMTs")
    print(f" -> Total PMT placed: {len(top_positions) + len(bot_positions) + len(rectangle_positions)}\n")

    # Write PMT positions to text file
    all_positions = top_positions + lateral_positions + bot_positions
    all_directions = top_directions + lateral_directions + bot_directions

    store_positions_and_directions(all_positions, all_directions, R, H, filename)

    # Plots
    plot_all(
        R,
        H,
        r,
        rectangle_positions,
        top_positions,
        bot_positions,
        lateral_positions,
        filename,
        plot_nicer_plots,
        run_batch,
    )


if __name__ == "__main__":
    run_batch = True

    if len(sys.argv) == 4:
        R = int(sys.argv[1])
        H = int(sys.argv[2])
        plot_nicer_plots = bool(sys.argv[3])

    else:
        run_batch = False
        plot_nicer_plots = False

        # WbLS detector 1000 times smaller than SK
        # R = 4000  # [mm]
        # H = 8000  # [mm]

        # SK-like
        # R = 20000  # [mm]
        # H = 40000  # [mm]

        # SK
        R = 16900  # [mm]
        H = 18100  # [mm]

    main(R, H, plot_nicer_plots, run_batch)
