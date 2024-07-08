#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 19 15:54:07 2024

@author: Mattia Fanì (Los Alamos National Laboratory, US) - mattia.fani@cern.ch

"""

import matplotlib.pyplot as plt


def plot_rectangle(C, H, r, rectangle_positions, run_batch):
    # Create a figure and axis
    fig, ax = plt.subplots()

    # Plot rectangle
    rectangle = plt.Rectangle((0, -H / 2), C, H, color="lightblue")
    ax.add_patch(rectangle)

    # Plot PMTs as circles with uniform radius
    for x, y in rectangle_positions:
        circle = plt.Circle((x, y), r, color="red", alpha=0.5)
        ax.add_patch(circle)

    # Set plot limits and labels
    ax.set_xlim(0, C)
    ax.set_ylim(0, H)
    ax.set_xlabel("[mm]")
    ax.set_ylabel("[mm]")

    # Show plot
    plt.axis("equal")
    if not run_batch:
        plt.show()
