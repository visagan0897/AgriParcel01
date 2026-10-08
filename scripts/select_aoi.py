from pathlib import Path

import geopandas as gpd
from shapely.geometry import box


PROJECT_ROOT = Path(__file__).resolve().parents[1]

BOUNDARY_FILE = (
    PROJECT_ROOT
    / "data"
    / "reference"
    / "target_taluks.geojson"
)

OUTPUT_FILE = (
    PROJECT_ROOT
    / "config"
    / "aoi.geojson"
)

TARGET_MIN_KM2 = 25.0
TARGET_MAX_KM2 = 40.0

# Candidate window dimensions in degrees.
# Roughly 5 km x 5 km at this latitude.
WINDOW_WIDTH = 0.055
WINDOW_HEIGHT = 0.055

STEP = 0.01


def main() -> None:
    print("Loading verified taluk boundaries...")

    taluks = gpd.read_file(BOUNDARY_FILE)

    # Use a metric CRS for geometry and area calculations.
    taluks_m = taluks.to_crs("EPSG:32644")

    study_region = taluks_m.geometry.union_all()

    # Search in WGS84 because the candidate grid is generated
    # from longitude/latitude coordinates.
    study_region_wgs84 = taluks.to_crs("EPSG:4326").geometry.union_all()

    minx, miny, maxx, maxy = study_region_wgs84.bounds

    print("\nStudy-region bounds:")
    print(f"  Longitude: {minx:.6f} → {maxx:.6f}")
    print(f"  Latitude : {miny:.6f} → {maxy:.6f}")

    candidates = []

    lon = minx

    while lon + WINDOW_WIDTH <= maxx:
        lat = miny

        while lat + WINDOW_HEIGHT <= maxy:
            rectangle = box(
                lon,
                lat,
                lon + WINDOW_WIDTH,
                lat + WINDOW_HEIGHT,
            )

            # Candidate must be completely inside the verified
            # Ambasamudram/Cheranmahadevi study region.
            if study_region_wgs84.contains(rectangle):
                candidate = gpd.GeoSeries(
                    [rectangle],
                    crs="EPSG:4326",
                ).to_crs("EPSG:32644").iloc[0]

                area_km2 = candidate.area / 1_000_000

                if TARGET_MIN_KM2 <= area_km2 <= TARGET_MAX_KM2:
                    candidates.append(
                        {
                            "geometry": rectangle,
                            "area_km2": area_km2,
                            "center_lon": lon + WINDOW_WIDTH / 2,
                            "center_lat": lat + WINDOW_HEIGHT / 2,
                        }
                    )

            lat += STEP

        lon += STEP

    print(f"\nSuitable candidates found: {len(candidates)}")

    if not candidates:
        print("No candidate AOI found.")
        print("We will adjust the search window in the next step.")
        return

    # Choose the candidate closest to 30 km².
    selected = min(
        candidates,
        key=lambda item: abs(item["area_km2"] - 30.0),
    )

    output = gpd.GeoDataFrame(
        {
            "name": ["AgriParcel01 AOI"],
            "area_km2": [selected["area_km2"]],
            "selection": ["Grid search inside verified taluk boundaries"],
        },
        geometry=[selected["geometry"]],
        crs="EPSG:4326",
    )

    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    output.to_file(
        OUTPUT_FILE,
        driver="GeoJSON",
    )

    print("\nSELECTED AOI")
    print("------------------------------")
    print(f"Area       : {selected['area_km2']:.2f} km²")
    print(f"Center     : {selected['center_lat']:.6f}, "
          f"{selected['center_lon']:.6f}")
    print("------------------------------")

    print("\nSaved:")
    print(OUTPUT_FILE)


if __name__ == "__main__":
    main()