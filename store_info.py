#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  8 23:39:08 2024

@author: Mattia Fanì (UMN) - mattia.fani@cern.ch

"""

import numpy as np
from utils import store_list_to_txtfile, write_PMTINFO_file


def store_positions_and_directions(positions, directions, R, H, filename):
    positions_x = [pos[0] for pos in positions]
    positions_y = [pos[1] for pos in positions]
    positions_z = [pos[2] for pos in positions]

    directions_x = [dir[0] for dir in directions]
    directions_y = [dir[1] for dir in directions]
    directions_z = [dir[2] for dir in directions]

    store_list_to_txtfile(positions_x, "positions_x", R, H)
    store_list_to_txtfile(positions_y, "positions_y", R, H)
    store_list_to_txtfile(positions_z, "positions_z", R, H)
    store_list_to_txtfile(directions_x, "directions_x", R, H)
    store_list_to_txtfile(directions_y, "directions_y", R, H)
    store_list_to_txtfile(directions_z, "directions_z", R, H)

    pmt_type = np.ones(len(positions_x))
    store_list_to_txtfile(pmt_type, "pmt_type", R, H)

    write_PMTINFO_file(
        "PMTINFO_" + filename,
        positions_x,
        positions_y,
        positions_z,
        directions_x,
        directions_y,
        directions_z,
        pmt_type,
        R,
        H,
    )
