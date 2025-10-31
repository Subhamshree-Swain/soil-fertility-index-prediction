import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import griddata

def fertility_map(data, resolution=100):
    points = data[["Latitude", "Longitude"]].values
    values = data["SFI"].values

    lat_min = data["Latitude"].min()
    lat_max = data["Latitude"].max()
    lon_min = data["Longitude"].min()
    lon_max = data["Longitude"].max()

    # padding
    lat_pad = (lat_max - lat_min) * 0.05
    lon_pad = (lon_max - lon_min) * 0.05

    lat_grid = np.linspace(lat_min - lat_pad, lat_max + lat_pad, resolution)
    lon_grid = np.linspace(lon_min - lon_pad, lon_max + lon_pad, resolution)
    lat_grid_mesh, lon_grid_mesh = np.meshgrid(lat_grid, lon_grid)

    # now interpolation
    sfi_grid = griddata(
        points, values,
        (lat_grid_mesh, lon_grid_mesh),
        method = "cubic",
        fill_value = np.nan
    )

    # Time for some visualization
    fig = plt.figure(figsize=(18, 7))

    # SFI map
    ax1 = plt.subplot(1, 3, 1)
    contour = ax1.contourf(lon_grid_mesh, lat_grid_mesh, sfi_grid,
                           levels=20, cmap="RdYlGn", alpha=0.9)
    plt.colorbar(contour, ax=ax1, label="SFI(0-100)")
    ax1.scatter(data["Longitude"], data["Latitude"], c="black", s=10, marker="x", alpha = 0.5, label="Sample Points")
    ax1.set_xlabel("Longitude")
    ax1.set_ylabel("Latitude")
    ax1.set_title("Soil Fertility Map")
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # SFI in terms low, medium and high
    ax2 = plt.subplot(1, 3, 2)
    sfi_class = np.digitize(sfi_grid,bins=[0, 40, 60, 80, 100])
    cmap_discrete = plt.cm.colors.ListedColormap(["#d73027", "#fee08b", "#d9ef8b", "#1a9850"])
    # the colors are - red, yellow, green, dark green in this order

    discrete_map = ax2.pcolormesh(lon_grid_mesh, lat_grid_mesh, sfi_class,
                   cmap = cmap_discrete, vmin=1, vmax=4, alpha=0.9)

    cbar = plt.colorbar(discrete_map, ax=ax2, ticks=[1.5, 2.5, 3.5, 4.5])
    cbar.ax.set_yticklabels(["Low\n(0-40)", "Low-Medium\n(40-60)", "Medium-High\n(60-80)", "High\n(80-100)"])
    ax2.scatter(data["Longitude"], data["Latitude"], c="black", s=10, marker="x", alpha=0.5)
    ax2.set_xlabel("Longitude")
    ax2.set_ylabel("Latitude")
    ax2.set_title("Fertility Classification Zones")
    ax2.grid(True, alpha=0.3)

    # Now time for 3D
    ax3 = plt.subplot(1, 3, 3, projection="3d")
    surface = ax3.plot_surface(lon_grid_mesh, lat_grid_mesh, sfi_grid, cmap = "RdYlGn", alpha = 0.9, linewidth=0)
    ax3.set_xlabel("Longitude")
    ax3.set_ylabel("Latitude")
    ax3.set_zlabel("SFI")
    ax3.set_title("3D Fertility Surface")
    plt.colorbar(surface, ax=ax3, shrink=0.5, label="SFI")
    plt.tight_layout()

    # Save the Files
    plt.savefig("sfi_map.png", dpi=300, bbox_inches="tight")
    plt.show()

    return lon_grid_mesh, lat_grid_mesh, sfi_grid

    
def analysis_window(data):
    fig = plt.figure(figsize=(16, 13))
    gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)

    # Histogram
    ax1 = fig.add_subplot(gs[0, :])
    ax1.hist(data["SFI"], bins=40, color="skyblue", edgecolor="black", alpha=0.7)
    ax1.axvline(data["SFI"].mean(), color="red", linestyle="--", linewidth=2, label=f"Mean: {data["SFI"].mean():.2f}")
    ax1.set_xlabel("Soil Fertility Index")
    ax1.set_ylabel("Frequency")
    ax1.set_title("Distribution of SFI")
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # Seperate parameter vs SFI
    params = [("N", "Nitrogen (kg/ha)", "blue"),
              ("P", "Phosphorus (kg/ha)", "orange"),
              ("K", "Potassium (kg/ha)", "green"),
              ("OC", "Organic Carbon (%)", "red"),
              ("ph", "pH", "purple")]

    for  index, (param, label, color) in enumerate(params):
        row = 1 + index // 3
        col = index % 3
        ax = fig.add_subplot(gs[row, col])

        ax.scatter(data[param], data["SFI"], alpha = 0.5, c=color, s=20)

        z = np.polyfit(data[param], data["SFI"], 2)
        p = np.poly1d(z)
        x_line = np.linspace(data[param].min(), data[param].max(), 100)
        ax.plot(x_line, p(x_line), "r--", alpha=0.8, linewidth=2)

        corr = data[[param, "SFI"]].corr().iloc[0, 1]
        ax.text(0.05, 0.95, f"Corr: {corr:.3f}",
                transform = ax.transAxes, verticalalignment="top",
                bbox=dict(boxstyle="round", facecolor="wheat", alpha=0.5))

        ax.set_xlabel(label)
        ax.set_ylabel("SFI")
        ax.set_title(f"{param} vs SFI")
        ax.grid(True, alpha=0.3)



    #Stats
    ax_stats = fig.add_subplot(gs[2, 2])
    ax_stats.axis("off")

    stats_text = f"""
    STATISTICS

    Total Samples: {len(data)}

    SFI Statistics:
        Mean: {data["SFI"].mean():.2f}
        Median: {data["SFI"].median():.2f}
        Std Dev: {data["SFI"].std():.2f}
        Range: {data["SFI"].min():.2f} - {data["SFI"].max():.2f}

    Nutrient Avgerages:
        N: {data["N"].mean():.1f} kg/ha
        P: {data["P"].mean():.1f} kg/ha
        K: {data["K"].mean():.1f} kg/ha
        OC: {data["OC"].mean():.1f} %
        pH: {data["ph"].mean():.1f} 
    """

    ax_stats.text(0.1, 0.5, stats_text, fontsize=10,
                  verticalalignment="center", family="monospace",
                  bbox=dict(boxstyle="round", facecolor="lightblue", alpha=0.3))
    plt.savefig("sfi_parameter.png", dpi = 300, bbox_inches="tight")
    plt.show()
