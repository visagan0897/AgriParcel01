from pathlib import Path

import geopandas as gpd
import matplotlib.pyplot as plt


PROJECT_ROOT = Path(__file__).resolve().parents[1]

INPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "reference"
    / "target_taluks.geojson"
)

OUTPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "reference"
    / "taluk_inspection.png"
)


def main() -> None:
    print("Loading target taluk boundaries...")

    gdf = gpd.read_file(INPUT_FILE)

    print(f"Features: {len(gdf)}")
    print(f"CRS: {gdf.crs}")

    # Project to metric coordinates for inspection.
    projected = gdf.to_crs("EPSG:32644")

    fig, ax = plt.subplots(figsize=(12, 10))

    projected.boundary.plot(
        ax=ax,
        linewidth=1.5,
    )

    projected.plot(
        ax=ax,
        alpha=0.15,
    )

    for _, row in projected.iterrows():
        point = row.geometry.representative_point()

        ax.annotate(
            row["shapeName"],
            (point.x, point.y),
            fontsize=12,
            ha="center",
        )

    ax.set_title(
        "Ambasamudram and Cheranmahadevi — AOI Inspection"
    )

    ax.set_xlabel("Easting (m)")
    ax.set_ylabel("Northing (m)")

    ax.set_aspect("equal")

    plt.tight_layout()

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    plt.savefig(
        OUTPUT_FILE,
        dpi=180,
        bbox_inches="tight",
    )

    plt.close()

    print("\nInspection map saved:")
    print(OUTPUT_FILE)


if __name__ == "__main__":
    main()