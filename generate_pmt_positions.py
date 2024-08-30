#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 26 19:59:23 2024

@author: Mattia Fanì (UMN) - mattia.fani@cern.ch

"""

from numpy import pi as pi, sign as sign
from utils import get_spacing  # , check_overlapping_pmts

# from math import ceil as ceil, floor as floor, sqrt as sqrt
from math import cos as cos, sin as sin


def generate_rectangle_positions(n_rows, n_cols, C, H):
    positions = []
    row_spacing, col_spacing = get_spacing(n_rows, n_cols, C, H)
    origin_x = row_spacing / 2 - (C / 2)
    origin_y = col_spacing / 2 - (H / 2)
    for i_row in range(n_rows):
        for i_col in range(n_cols):
            positions.append((round(origin_x + i_col * col_spacing, 2), round(origin_y + i_row * row_spacing, 2)))
    return positions


def generate_lateral_positions(R, H, n_rows, n_cols):
    positions = []
    directions = []
    C = 2 * pi * R
    row_spacing, col_spacing = get_spacing(n_rows, n_cols, C, H)

    d_theta = 2 * pi / n_cols

    for i_row in range(n_rows):
        for i_col in range(n_cols):
            theta = d_theta / 2 + i_col * d_theta
            x = round(R * cos(theta), 2)
            y = round(R * sin(theta), 2)
            z = round(-H / 2 + row_spacing / 2 + i_row * row_spacing, 2)
            positions.append((x, y, z))
            directions.append((-1 * round(cos(theta), 4), (-1 * round(sin(theta), 4)), 0))

    return positions, directions


def generate_circle_positions(R, H, r, nT, n_circles, level=0):
    positions = []
    directions = []
    angles = []
    circles = []

    offset = pi / 8

    dR = round(R / n_circles, 1)
    circle_r = dR / 2

    # # check PMTs overlapping in the smallest circumference
    # if

    circles.append((dR / 2, 2 * pi * dR / 2, 0, 0))  # (circ_radius, circle_length, offset, offset_polar)
    for i_r in range(n_circles - 1):
        circle_r += dR
        # offset = round(col_spacing / (n_circles - i_r), 1)
        offset_angle = round(offset / circle_r, 2)
        circles.append((round(circle_r, 1), round(2 * pi * circle_r, 1), offset, offset_angle))

    # find circles total length
    circ_total_length = 0
    for circle in circles:
        circ_length = circle[1]
        if circ_length < 0.1:
            circ_length = 1

        circ_total_length += circ_length

    n_pmts_per_circle = []
    for circle in circles:
        n_pmt = int(circle[1] / circ_total_length * nT)
        if n_pmt == 0:
            n_pmt = 1

        # check on overlapping pmts
        circ_pmt = n_pmt * 2 * r  # sum of all pmt diameters in a circle

        while 1.1 * circ_pmt > circle[1]:  # 1.1 to leave room for pmt installation
            circ_pmt = n_pmt * 2 * r
            n_pmt = n_pmt - 1

        if n_pmt == 0:
            n_pmt = 1

        n_pmts_per_circle.append(n_pmt)

    for j in range(len(n_pmts_per_circle)):
        dtheta = 2 * pi / n_pmts_per_circle[j]
        angles.append(dtheta)

    for i in range(len(n_pmts_per_circle)):  # loop over circles
        radius = circles[i][0]
        offset_polar = circles[i][3]

        n_pmts_this_circle = n_pmts_per_circle[i]

        for k in range(n_pmts_this_circle):  # loop over pmts in a circle
            theta = offset_polar + k * angles[i]
            x = round(radius * cos(theta), 1)
            y = round(radius * sin(theta), 1)
            positions.append((x, y, level))
            # directions.append((-1 * round(cos(theta), 4), (-1 * round(sin(theta), 4)), -1 * sign(level))) # this is only okay on lateral surfaces
            directions.append((0, 0, -1 * sign(level)))

        if level > 0:
            print(
                f"{i+1}: r = {round(radius)} mm, angular offset = {180*offset_polar/pi} deg; PMTs = {n_pmts_per_circle[i]}"
            )

    # print(positions)
    # print(directions)

    return positions, directions
