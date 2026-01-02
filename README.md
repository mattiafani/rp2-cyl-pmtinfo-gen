# rp2-cyl-pmtinfo-gen

A Python tool for generating RAT-PAC 2 PMTINFO files for cylindrical detectors with optimized PMT configurations.

## Overview

This tool automates the generation of geometry configuration files for cylindrical detector designs used in neutrino physics experiments. It calculates optimal PMT placement on cylindrical surfaces and endcaps based on requested detector coverage, ensuring no PMT overlap while maximizing coverage efficiency. Endcap PMTs can be placed in two different layouts: circular and grid-like.

## Key Features

- **Coverage-based PMT placement**: Automatically determines the number and position of PMTs per surface, based on requested detector coverage
- **Overlap prevention**: Ensures PMTs do not overlap while maintaining optimal spacing
- **Cylindrical geometry support**: Handles both cylindrical barrel surfaces and endcap configurations
- **Visual verification**: Generates plots for visual inspection of PMT layouts
- **RAT-PAC 2 compatibility**: Outputs PMTINFO files in RAT-PAC 2 format
- **Batch processing**: Supports generating multiple configurations efficiently

## How It Works

1. **Input**: Specify detector dimensions (radius, height) and coverage requirements
2. **Calculation**: The tool computes optimal PMT positions ensuring:
   - Desired coverage percentage is achieved
   - PMTs are evenly distributed across surfaces
   - No physical overlap between PMTs
3. **Output**: Generates geometry files and visualization plots for verification
4. **Validation**: Review generated plots to confirm the PMT layout meets requirements

## Requirements

- Python 3.x
- NumPy
- Matplotlib (for visualization)

## Installation

```bash
git clone https://github.com/mattiafani/rp2-cyl-pmtinfo-gen.git
cd rp2-cyl-pmtinfo-gen
```

## Usage

### Basic Usage

Run the main script with the following parameters:

```bash
python3 py.py <R[mm]> <H[mm]> <bool_endcaps_pmt_grid> <bool_nicer_plots> <bool_run_batch>
```

**Parameters:**
- `R[mm]`: Radius of the cylindrical detector in millimeters
- `H[mm]`: Height of the cylindrical detector in millimeters
- `bool_endcaps_pmt_grid`: Enable/disable PMT grid on endcaps (`True`/`False`)
- `bool_nicer_plots`: Enable enhanced visualization (`True`/`False`)
- `bool_run_batch`: Enable batch processing mode (`True`/`False`)

### Example

```bash
python3 py.py 16900 18100 True False True
```

This generates geometry files for a detector with:
- Radius: 16.9 meters
- Height: 18.1 meters
- PMT grid on endcaps enabled
- Standard plotting
- Batch mode enabled

The tool will automatically:
- Calculate the number of PMTs needed for the requested coverage
- Position PMTs to avoid overlap
- Generate visualization plots for verification
- Output RAT-PAC 2 compatible geometry files

## File Structure

- `py.py`: Main script for geometry generation
- `generate_pmt_positions.py`: Core logic for calculating PMT positions with overlap prevention
- `utils.py`: Utility functions for geometry calculations
- `store_info.py`: Data storage and output file generation
- `plot_all.py`: Comprehensive visualization of detector geometry
- `plot_cylinder.py`: Cylindrical surface visualization
- `plot_open.py`: Open detector view visualization
- `plot_rectangle.py`: Flat projection visualization

## Output

The tool generates:
- **Geometry files**: RAT-PAC 2 compatible configuration files with PMT positions
- **PMT coordinates**: Complete list of PMT positions and orientations
- **Visualization plots**: Multiple views for visual verification of PMT layout
  - 3D detector view
  - Cylindrical surface unwrapping
  - Endcap layouts
  - PMT distribution analysis

## Visualization and Verification

After running the tool, review the generated plots to verify:
- PMTs are evenly distributed across the detector surface
- No PMT overlap occurs
- Coverage meets your requirements
- Endcap PMT arrangements (if enabled)

## PMT Placement Algorithm

The tool uses an intelligent placement algorithm that:
1. Calculates required PMT density based on coverage requirements
2. Distributes PMTs uniformly across cylindrical and endcap surfaces
3. Checks for and prevents any PMT overlap
4. Optimizes spacing for maximum coverage efficiency

## License

This project is licensed under the GNU General Public License v2.0 - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## Contact

For questions or support, please open an issue on the [GitHub repository](https://github.com/mattiafani/rp2-cyl-pmtinfo-gen).

## Acknowledgments

This tool is designed for use with RAT-PAC 2 (Reactor Analysis Tool - Physics Analysis in C++), a simulation framework used in neutrino detector experiments.