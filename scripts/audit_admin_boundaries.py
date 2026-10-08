from pathlib import Path

import geopandas as gpd


PROJECT_ROOT = Path(__file__).resolve().parents[1]

BOUNDARY_FILE = (
    PROJECT_ROOT
    / "data"
    / "reference"
    / "india_adm3_simplified.geojson"
)

OUTPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "reference"
    / "target_taluks.geojson"
)


TARGET_NAMES = [
    "Ambasamudram",
    "Cheranmahadevi",
]


def main() -> None:
    print("Reading India ADM3 boundary dataset...")

    gdf = gpd.read_file(BOUNDARY_FILE)

    print(f"Total features: {len(gdf)}")
    print(f"CRS: {gdf.crs}")

    # Exact names confirmed from the dataset.
    targets = gdf[
        gdf["shapeName"].isin(TARGET_NAMES)
    ].copy()

    print("\nTarget features found:")

    if targets.empty:
        print("ERROR: No target features found.")
        return

    print(
        targets[
            [
                "shapeName",
                "shapeISO",
                "shapeID",
                "shapeGroup",
                "shapeType",
            ]
        ].to_string(index=False)
    )

    print("\nCalculating approximate areas...")

    # Reproject to a metric CRS for area calculation.
    # EPSG:32644 = WGS84 / UTM zone 44N,
    # appropriate for the Tirunelveli region.
    projected = targets.to_crs("EPSG:32644")

    targets["area_km2"] = projected.geometry.area / 1_000_000

    print(
        targets[
            ["shapeName", "area_km2"]
        ].to_string(index=False)
    )

    total_area = targets["area_km2"].sum()

    print(f"\nCombined area: {total_area:.2f} km²")

    # Save extracted taluk boundaries.
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    targets.to_file(
        OUTPUT_FILE,
        driver="GeoJSON",
    )

    print("\nSaved:")
    print(OUTPUT_FILE)


if __name__ == "__main__":
    main()