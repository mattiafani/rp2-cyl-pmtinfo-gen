#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 19 15:54:07 2024

@author: Mattia Fanì (UMN) - mattia.fani@cern.ch

"""

import matplotlib.pyplot as plt
from utils import create_plots_dir


def plot_rectangle(R, C, H, r, rectangle_positions, plot_title=None, save_file=None, file_name=None, run_batch=False):
    plots_directory = create_plots_dir(R, H)

    # Create a figure and axis
    fig, ax = plt.subplots()

    # Plot rectangle
    rectangle = plt.Rectangle((-C / 2, -H / 2), C, H, color="lightblue")
    ax.add_patch(rectangle)

    # Plot PMTs as circles with uniform radius
    for x, y in rectangle_positions:
        pmt = plt.Circle((x, y), r, color="blue", alpha=0.5, linewidth=0.5)
        # WARNING!!! Dimensions of linewidth are not on scale: the PMTs may appear bigger in the plot
        ax.add_patch(pmt)

    # Set plot limits and labels
    ax.set_xlim(0, C)
    ax.set_ylim(0, H / 2)
    ax.set_xlabel("[mm]")
    ax.set_ylabel("[mm]")

    # Show plot
    plt.axis("equal")

    # Plot

    if save_file:
        plt.savefig(f"{plots_directory}/{file_name}.pdf", format="pdf")
        print(f"Plot saved as {plots_directory}/{file_name}.pdf")

    if not run_batch:
        plt.show()

    plt.close()

    fig.clear()


def plot_circle_top(R, H, circle_positions, r, plot_title=None, save_file=None, file_name=None, run_batch=False):
    plots_directory = create_plots_dir(R, H)

    # Create a figure and axis
    fig, ax = plt.subplots()

    # Plot rectangle
    circle = plt.Circle((0, 0), R, color="lightblue")
    ax.add_patch(circle)

    # Plot PMTs as circles with uniform radius
    for x, y, z in circle_positions:
        pmt = plt.Circle((x, y), r, color="blue", alpha=0.5, linewidth=0.5)
        # WARNING!!! Dimensions of linewidth are not on scale: the PMTs may appear bigger in the plot
        ax.add_patch(pmt)

    # Set plot limits and labels
    ax.set_xlim(-1.5 * R, 1.5 * R)
    ax.set_ylim(-1.5 * R, 1.5 * R)
    ax.set_xlabel("[mm]")
    ax.set_ylabel("[mm]")

    # Show plot
    plt.axis("equal")

    # Plot

    if save_file:
        plt.savefig(f"{plots_directory}/{file_name}.pdf", format="pdf")
        print(f"Plot saved as {plots_directory}/{file_name}.pdf")

    if not run_batch:
        plt.show()

    plt.close()

    fig.clear()
