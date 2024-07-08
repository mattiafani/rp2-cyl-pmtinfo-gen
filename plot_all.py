#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  8 23:29:30 2024

@author: Mattia Fanì (UMN) - mattia.fani@cern.ch

"""

from math import pi
from plot_open import plot_rectangle, plot_circle_top
from plot_cylinder import plot_cylinder


def plot_all(
    R, H, r, rectangle_positions, top_positions, bot_positions, lateral_positions, filename, plot_nicer_plots, run_batch
):
    plot_rectangle(
        R,
        2 * pi * R,
        H,
        r,
        rectangle_positions,
        plot_title=f"Lateral surface; R = {R/1000} m, H = {H/1000} m",
        save_file=True,
        file_name=f"01_open_lateral_R{R}_H{H}",
        run_batch=run_batch,
    )
    plot_circle_top(
        R,
        H,
        top_positions,
        r,
        plot_title=f"Top/Bot surface; R = {R/1000} m, H = {H/1000} m",
        save_file=True,
        file_name=f"02_open_top_bot_R{R}_H{H}",
        run_batch=run_batch,
    )
    plot_cylinder(
        R,
        H,
        r,
        lateral_positions,
        is_nice_pointer=False,
        plot_title=f"Lateral surface; R = {R/1000} m, H = {H/1000} m",
        save_file=True,
        file_name=f"03_3d_lateral_R{R}_H{H}",
        run_batch=run_batch,
    )
    plot_cylinder(
        R,
        H,
        r,
        top_positions + bot_positions,
        is_nice_pointer=False,
        plot_title=f"Top/Bot surface; R = {R/1000} m, H = {H/1000} m",
        save_file=True,
        file_name=f"04_3d_top_bot_R{R}_H{H}",
        run_batch=run_batch,
    )
    plot_cylinder(
        R,
        H,
        r,
        lateral_positions + top_positions + bot_positions,
        is_nice_pointer=False,
        plot_title=f"Detector - R = {R/1000} m, H = {H/1000} m",
        save_file=True,
        file_name=f"05_3d_R{R}_H{H}",
        run_batch=run_batch,
    )

    if plot_nicer_plots:
        plot_cylinder(
            R,
            H,
            r,
            lateral_positions,
            True,
            plot_title=f"Lateral surface; R = {R/1000} m, H = {H/1000} m",
            save_file=True,
            file_name=f"06_3d_lateral_pmtscale_R{R}_H{H}",
            run_batch=run_batch,
        )
        plot_cylinder(
            R,
            H,
            r,
            top_positions + bot_positions,
            True,
            plot_title=f"Top/Bot surface; R = {R/1000} m, H = {H/1000} m",
            save_file=True,
            file_name=f"07_3d_top_bot_pmtscale_R{R}_H{H}",
            run_batch=run_batch,
        )
        plot_cylinder(
            R,
            H,
            r,
            lateral_positions + top_positions + bot_positions,
            True,
            plot_title=f"Detector - R = {R/1000} m, H = {H/1000} m",
            save_file=True,
            file_name=f"08_3d_pmtscale_R{R}_H{H}",
            run_batch=run_batch,
        )
