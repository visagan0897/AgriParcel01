from pathlib import Path

import geopandas as gpd
from shapely.geometry import box


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
    / "candidate_aoi.geojson"
)


# Candidate rectangle in geographic coordinates.
# This is only a search candidate.
MIN_LON = 77.38
MAX_LON = 77.48
MIN_LAT = 8.62
MAX_LAT = 8.72


def main() -> None:
    print("Loading verified taluk boundaries...")

    taluks = gpd.read_file(INPUT_FILE)

    # Work in a metric CRS for all area calculations.
    taluks_m = taluks.to_crs("EPSG:32644")

    # Combine Ambasamudram + Cheranmahadevi.
    study_region = taluks_m.geometry.union_all()

    print("Creating candidate rectangle...")

    candidate_wgs84 = box(
        MIN_LON,
        MIN_LAT,
        MAX_LON,
        MAX_LAT,
    )

    candidate = gpd.GeoDataFrame(
        {
            "name": ["Candidate AOI"],
        },
        geometry=[candidate_wgs84],
        crs="EPSG:4326",
    ).to_crs("EPSG:32644")

    # Keep only the portion inside the verified study region.
    aoi_geometry = candidate.geometry.iloc[0].intersection(
        study_region
    )

    area_km2 = aoi_geometry.area / 1_000_000

    print(f"\nCandidate AOI area: {area_km2:.2f} km²")

    if area_km2 < 20:
        print("RESULT: FAIL — below official 20 km² minimum.")
        return

    print("RESULT: PASS — satisfies the 20 km² minimum.")

    # Convert back to WGS84 for GeoJSON.
    output = gpd.GeoDataFrame(
        {
            "name": ["Candidate AOI"],
            "area_km2": [area_km2],
        },
        geometry=[aoi_geometry],
        crs="EPSG:32644",
    ).to_crs("EPSG:4326")

    output.to_file(
        OUTPUT_FILE,
        driver="GeoJSON",
    )

    print("\nSaved candidate AOI:")
    print(OUTPUT_FILE)


if __name__ == "__main__":
    main()