import os

import pandas as pd


def load_real_data():
    """Load real data from CSV file and prepare it for mapping"""
    # Path to the real data file
    data_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "data/processed/FundsGDPhealth_export.csv",
    )

    # Read the CSV file
    df = pd.read_csv(data_path)

    # Add country coordinates for mapping (a lookup dictionary)
    country_coords = {
        "Germany": {"lat": 51.1657, "lon": 10.4515},
        "France": {"lat": 46.2276, "lon": 2.2137},
        "Netherlands": {"lat": 52.1326, "lon": 5.2913},
        "Spain": {"lat": 40.4637, "lon": -3.7492},
        "Italy": {"lat": 41.8719, "lon": 12.5674},
        "Belgium": {"lat": 50.8503, "lon": 4.3517},
        "Norway": {"lat": 60.4720, "lon": 8.4689},
        "Sweden": {"lat": 60.1282, "lon": 18.6435},
        "Denmark": {"lat": 56.2639, "lon": 9.5018},
        "Austria": {"lat": 47.5162, "lon": 14.5501},
        "Portugal": {"lat": 39.3999, "lon": -8.2245},
        "Finland": {"lat": 61.9241, "lon": 25.7482},
        "Ireland": {"lat": 53.1424, "lon": -7.6921},
        "Poland": {"lat": 51.9194, "lon": 19.1451},
        "Czechia": {"lat": 49.8175, "lon": 15.4730},
        "Slovenia": {"lat": 46.1512, "lon": 14.9955},
        "Luxembourg": {"lat": 49.8153, "lon": 6.1296},
        "Hungary": {"lat": 47.1625, "lon": 19.5033},
        "Romania": {"lat": 45.9432, "lon": 24.9668},
        "Turkey": {"lat": 38.9637, "lon": 35.2433},
        "Estonia": {"lat": 58.5953, "lon": 25.0136},
        "Switzerland": {"lat": 46.8182, "lon": 8.2275},
        "Cyprus": {"lat": 35.1264, "lon": 33.4299},
        "Lithuania": {"lat": 55.1694, "lon": 23.8813},
        "Latvia": {"lat": 56.8796, "lon": 24.6032},
        "Croatia": {"lat": 45.1000, "lon": 15.2000},
        "Serbia": {"lat": 44.0165, "lon": 21.0059},
        "Slovakia": {"lat": 48.6690, "lon": 19.6990},
        "Bulgaria": {"lat": 42.7339, "lon": 25.4858},
        "Iceland": {"lat": 64.9631, "lon": -19.0208},
        "Malta": {"lat": 35.9375, "lon": 14.3754},
        # "Ukraine": {"lat": 48.3794, "lon": 31.1656},
        "Albania": {"lat": 41.1533, "lon": 20.1683},
        "North Macedonia": {"lat": 41.6086, "lon": 21.7453},
        "Montenegro": {"lat": 42.7087, "lon": 19.3744},
        # "Bosnia and Herzegovina": {"lat": 43.9159, "lon": 17.6791},
    }

    # Create a new map-ready DataFrame
    map_data = []
    years = range(2013, 2025)

    for _, row in df.iterrows():
        country_name = row["TIME"]  # 'TIME' column contains country names
        country_code = row["country"]

        if country_name in country_coords:
            for year in years:
                gdp_col = f"GDP{year}"
                health_col = f"HLY{year}"

                # Skip if data is missing
                if pd.notna(row.get(gdp_col)) and pd.notna(row.get(health_col, None)):
                    map_data.append(
                        {
                            "Entity": country_name,
                            "CountryCode": country_code,
                            "Year": year,
                            "GDP": row[gdp_col],
                            "HealthyLifeYears": row[health_col],
                            "latitude": country_coords[country_name]["lat"],
                            "longitude": country_coords[country_name]["lon"],
                            "TotalFunds": row["TotalFundsPerCountry"],
                        }
                    )

    # Convert to DataFrame
    map_data_df = pd.DataFrame(map_data)

    # Create polygon data
    polygon_data_df = pd.DataFrame(
        {
            "Entity": list(country_coords.keys()),
            "geometry": [
                f"POLYGON(({coords['lon'] - 2} {coords['lat'] - 2}, {coords['lon'] + 2} {coords['lat'] - 2}, "
                + f"{coords['lon'] + 2} {coords['lat'] + 2}, {coords['lon'] - 2} {coords['lat'] + 2}, "
                + f"{coords['lon'] - 2} {coords['lat'] - 2}))"
                for coords in country_coords.values()
            ],
        }
    )

    return map_data_df, polygon_data_df


# Load the real data
map_data, polygon_data = load_real_data()
plot_data = map_data.copy()


def load_topic_data():
    """Load topic data from CSV file"""
    # Path to the real data file
    data_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "data/processed/topic_df.csv",
    )
    # Read the CSV file
    topic_df = pd.read_csv(data_path)
    return topic_df


topic_data = load_topic_data()
