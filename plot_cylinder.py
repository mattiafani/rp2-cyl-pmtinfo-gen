import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from utils import create_plots_dir


def plot_cylinder(
    R, H, r, pmt_positions, is_nice_pointer, plot_title=None, save_file=None, file_name=None, run_batch=False
):
    plots_directory = create_plots_dir(R, H)

    # Generate points for the cylinder surface
    theta = np.linspace(0, 2 * np.pi, 100)
    x = R * np.cos(theta)
    y = R * np.sin(theta)

    # Create a figure and 3D axis
    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")

    # Plot cylinder surface
    ax.plot(x, y, zs=-H / 2, zdir="z", linewidth=2, color="lightblue")
    ax.plot(x, y, zs=H / 2, zdir="z", linewidth=2, color="lightblue")

    # Plot PMT positions
    pmt_positions = np.array(pmt_positions)
    ax.scatter(pmt_positions[:, 0], pmt_positions[:, 1], pmt_positions[:, 2], c="blue", marker="o")

    # Plot PMTs as circles with uniform radius
    if is_nice_pointer == True:
        for x, y, z in pmt_positions:
            u = np.linspace(0, 2 * np.pi, 100)
            v = np.linspace(0, np.pi, 100)
            cx = r * np.outer(np.cos(u), np.sin(v)) + x
            cy = r * np.outer(np.sin(u), np.sin(v)) + y
            cz = r * np.outer(np.ones(np.size(u)), np.cos(v)) + z
            ax.plot_surface(cx, cy, cz, color="blue", alpha=0.5)

    ax.set_title(f"{plot_title}", fontsize=12)
    # ax.legend()

    # Set plot limits and labels
    ax.set_xlim([-R, R])
    ax.set_ylim([-R, R])
    ax.set_zlim([-H / 2, H / 2])
    ax.set_xlabel("X [mm]")
    ax.set_ylabel("Y [mm]")
    ax.set_zlabel("Z [mm]")

    ax.set_box_aspect([R / R, R / R, H / (2 * R)])

    # Plot

    if save_file:
        plt.savefig(f"{plots_directory}/{file_name}.pdf", format="pdf")
        print(f"Plot saved as {plots_directory}/{file_name}.pdf")

    if not run_batch:
        plt.show()

    plt.close()

    fig.clear()
