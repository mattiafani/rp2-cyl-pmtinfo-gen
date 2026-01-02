#!/usr/bin/env python3
"""
RAT-PAC 2 Cylindrical Detector PMT Info Generator
Generates geometry files with optimal PMT placement based on coverage requirements

Created on Fri Mar 15 23:59:20 2024
@author: Mattia Fanì (UMN) - mattia.fani@cern.ch
Modified: 2026 - Added argparse for better parameter handling
"""

import sys
import argparse
import numpy as np
from math import pi, ceil
from utils import get_spacing, find_nrows_ncols, store_list_to_txtfile, write_PMTINFO_file
from generate_pmt_positions import generate_rectangle_positions, generate_lateral_positions
from generate_pmt_positions import generate_circle_positions, generate_circle_grid_positions
from plot_all import plot_all
from store_info import store_positions_and_directions


def print_detector_info(R, H, C, S, V, STop, SLat):
    print(f"Detector dimensions: \
          R = {R/1e3} m, H = {H/1e3} m; C = {round(C/1e3, 3)} m")
    print(f"Detector Surface = {round(S/1e6, 2)} m^2; \
          Detector Volume = {round(V/1e9, 2)} m^3")
    print(f"Face surfaces: Top/Bot = \
          {round(STop/1e6, 2)} m^2; Lateral = {round(SLat/1e6, 2)} m^2")


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


def parse_arguments():
    """Parse command line arguments with proper validation"""
    parser = argparse.ArgumentParser(
        description='Generate RAT-PAC 2 geometry files for cylindrical detectors',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s -r 16900 -H 18100 -c 0.30
  %(prog)s -r 16900 -H 18100 -c 0.30 --endcaps --batch
  %(prog)s -r 16900 -H 18100 -c 0.40 --endcaps --nice-plots
  %(prog)s -r 3540 -H 5480 -c 0.35  # Small detector example
        """
    )

    # Required arguments
    parser.add_argument(
        '-r', '--radius',
        type=float,
        required=True,
        help='Radius of the cylindrical detector in millimeters (e.g., 16900)'
    )

    parser.add_argument(
        '-H', '--height',
        type=float,
        required=True,
        help='Height of the cylindrical detector in millimeters (e.g., 18100)'
    )

    parser.add_argument(
        '-c', '--coverage',
        type=float,
        required=True,
        help='Desired PMT coverage as a fraction (e.g., 0.40 for 40%% coverage)'
    )

    # Optional arguments
    parser.add_argument(
        '--endcaps',
        action='store_true',
        help='Use grid layout for endcap PMTs (default: circular layout)'
    )

    parser.add_argument(
        '--nice-plots',
        action='store_true',
        help='Enable enhanced visualization with nicer plots'
    )

    parser.add_argument(
        '--batch',
        action='store_true',
        help='Enable batch processing mode'
    )

    parser.add_argument(
        '--pmt-radius',
        type=float,
        default=254.0,
        help='PMT radius in millimeters (default: 254.0 mm for R7081 10-inch PMTs)'
    )

    args = parser.parse_args()

    # Validate arguments
    if args.radius <= 0:
        parser.error("Radius must be positive")

    if args.height <= 0:
        parser.error("Height must be positive")

    if not (0.0 < args.coverage <= 1.0):
        parser.error("Coverage must be between 0 and 1 (e.g., 0.30 for 30%)")

    if args.pmt_radius <= 0:
        parser.error("PMT radius must be positive")

    return args


def main(R, H, coverage, top_bot_grid, plot_nicer_plots, run_batch, r=254):
    print("\nDetermination of PMT positions - Cylindrical Detector\n")

    # PMTs - R7081
    s = pi * r**2

    # Detector dimensions
    C = 2 * pi * R
    V = pi * R**2 * H
    S = 2 * pi * R * (H + R)
    STop = pi * R**2
    SLat = 2 * pi * R * H

    filename = f"Theia_Cyl_R{int(R)}_H{int(H)}"

    print_detector_info(R, H, C, S, V, STop, SLat)
    print(f"PMT radius = {r} mm")

    # Find number of PMTs to position
    n = calculate_pmt_coverage(coverage, S, s)
    print(f"Desired PMT coverage: {coverage * 100}%")
    print(f"\nRequired number of PMTs: {n}")

    # PMT fractions
    nT, nB, nL = calculate_pmt_fractions(S, STop, SLat, n)
    print(f" Top surface: {nT}\n Bottom surface:\
          {nB}\n Lateral surface: {nL}\n PMTs to place: {nT + nB + nL}")

    #########################################################
    # PMT positions
    #########################################################

    # Lateral Surface
    print("\nLateral Surface")
    n_rows, n_cols = find_nrows_ncols(C, H, r, nL)
    row_spacing, col_spacing = get_spacing(n_rows, n_cols, C, H)
    print(f"Rows: {n_rows}, Columns: {n_cols}; Row spacing:\
          {row_spacing} mm, Column spacing: {col_spacing} mm")

    if not top_bot_grid:
        # Top/Bot Surfaces
        print("\nTop/Bot Surface")
        n_circles = int(R / col_spacing)
        print(f"PMTs distributed in {n_circles} circles")

    # Generate positions
    rectangle_positions = generate_rectangle_positions(n_rows, n_cols, C, H)
    lateral_positions, lateral_directions = generate_lateral_positions(
        R, H, n_rows, n_cols)

    if (not top_bot_grid):
        top_positions, top_directions = generate_circle_positions(
            R, H, r, nT, n_circles, level=-1*H/2)
        bot_positions, bot_directions = generate_circle_positions(
            R, H, r, nT, n_circles, level=H/2)
    else:
        top_positions, top_directions = generate_circle_grid_positions(
            R, H, r, n_rows, n_cols, top=True)  # function adapted from A. Rothman
        bot_positions, bot_directions = generate_circle_grid_positions(
            R, H, r, n_rows, n_cols, top=False)  # function adapted from A. Rothman

    print("\nDistributed PMTs on the detector's inner surface: ")
    print(f" Top surface     : {len(top_positions)} PMTs")
    print(f" Lateral surface : {len(rectangle_positions)} PMTs")
    print(f" Bottom surface  : {len(bot_positions)} PMTs")
    print(f" -> Total PMT placed:\
          {len(top_positions) + len(bot_positions) + len(rectangle_positions)}\n")

    # Write PMT positions to text file
    all_positions = top_positions + lateral_positions + bot_positions
    all_directions = top_directions + lateral_directions + bot_directions

    store_positions_and_directions(
        all_positions, all_directions, R, H, filename)

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
    # Check if using new argparse interface or old positional arguments
    if len(sys.argv) > 1 and sys.argv[1] in ['-r', '--radius', '-h', '--help']:
        # New argparse interface
        args = parse_arguments()

        print("=" * 70)
        print("RAT-PAC 2 Cylindrical Detector Geometry Generator")
        print("=" * 70)
        print(f"Configuration:")
        print(f"  Radius:          \
              {args.radius:.1f} mm ({args.radius/1000:.2f} m)")
        print(f"  Height:          \
              {args.height:.1f} mm ({args.height/1000:.2f} m)")
        print(f"  Target Coverage: {args.coverage*100:.1f}%")
        print(f"  PMT Radius:      {args.pmt_radius:.1f} mm")
        print(f"  Endcap Layout:   {'Grid' if args.endcaps else 'Circular'}")
        print(f"  Nice Plots:      \
              {'Enabled' if args.nice_plots else 'Disabled'}")
        print(f"  Batch Mode:      {'Enabled' if args.batch else 'Disabled'}")
        print("=" * 70)

        main(
            R=args.radius,
            H=args.height,
            coverage=args.coverage,
            top_bot_grid=args.endcaps,
            plot_nicer_plots=args.nice_plots,
            run_batch=args.batch,
            r=args.pmt_radius
        )

    elif len(sys.argv) == 6:
        # Old interface for backward compatibility
        # python3 py.py <R> <H> <coverage> <top_bot_grid> <plot_nicer_plots>
        R = float(sys.argv[1])
        H = float(sys.argv[2])
        coverage = float(sys.argv[3])
        top_bot_grid = sys.argv[4].lower() in ['true', '1', 'yes']
        plot_nicer_plots = sys.argv[5].lower() in ['true', '1', 'yes']

        print("Note: Using old interface. Consider using new flags:")
        print(f"  python3 py.py -r {R} -H {H} -c {coverage}\
              {'--endcaps' if top_bot_grid else ''} {'--nice-plots' if plot_nicer_plots else ''}")
        print()

        main(R, H, coverage, top_bot_grid, plot_nicer_plots, run_batch=True)

    else:
        # Interactive mode with defaults (your original fallback)
        run_batch = False
        top_bot_grid = True
        plot_nicer_plots = False
        coverage = 0.30  # Default coverage

        # Default example configurations (uncomment as needed)
        R = 3200  # [mm]
        H = 5400  # [mm]

        print("Running in interactive mode with default parameters:")
        print(f"  R = {R} mm, H = {H} mm, Coverage = {coverage*100}%")
        print("\nFor better control, use command-line arguments:")
        print("  python3 py.py -r 16900 -H 18100 -c 0.30 --endcaps --nice-plots")
        print("  python3 py.py --help  (for all options)")
        print()

        main(R, H, coverage, top_bot_grid, plot_nicer_plots, run_batch)
