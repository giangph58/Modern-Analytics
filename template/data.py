import numpy as np
import pandas as pd

# Generate dummy map_data_oecd
countries = [
    {"Entity": "United States", "lat": 39.8283, "lon": -98.5795},
    {"Entity": "Germany", "lat": 51.1657, "lon": 10.4515},
    {"Entity": "France", "lat": 46.2276, "lon": 2.2137},
    {"Entity": "United Kingdom", "lat": 55.3781, "lon": -3.4360},
    {"Entity": "Japan", "lat": 36.2048, "lon": 138.2529},
    {"Entity": "Canada", "lat": 56.1304, "lon": -106.3468},
    {"Entity": "Australia", "lat": -25.2744, "lon": 133.7751},
    {"Entity": "Italy", "lat": 41.8719, "lon": 12.5674},
    {"Entity": "Spain", "lat": 40.4637, "lon": -3.7492},
    {"Entity": "Netherlands", "lat": 52.1326, "lon": 5.2913},
]

years = list(range(1990, 2018))
map_data_rows = []
plot_data_rows = []

np.random.seed(42)

# Generate map data
for country in countries:
    for year in years:
        base_death_rate = np.random.uniform(20, 80)
        year_trend = (year - 1990) * np.random.uniform(-0.5, 0.2)
        death_rate = max(10, base_death_rate + year_trend + np.random.normal(0, 5))

        base_pm25 = np.random.uniform(8, 25)
        pm25_trend = (year - 1990) * np.random.uniform(-0.1, 0.3)
        pm25 = max(5, base_pm25 + pm25_trend + np.random.normal(0, 2))

        map_data_rows.append(
            {
                "Entity": country["Entity"],
                "Year": year,
                "Death.Rate": round(death_rate, 1),
                "PM2.5": round(pm25, 1),
                "latitude": country["lat"],
                "longitude": country["lon"],
            }
        )

# Generate plot data (including "World")
plot_countries = [country["Entity"] for country in countries] + ["World"]

np.random.seed(42)
for country in plot_countries:
    for year in years:
        if country == "World":
            death_rate = np.random.uniform(35, 55) + (year - 1990) * np.random.uniform(
                -0.3, 0.1
            )
            pm25 = np.random.uniform(12, 18) + (year - 1990) * np.random.uniform(0, 0.2)
        else:
            base_death_rate = np.random.uniform(20, 80)
            year_trend = (year - 1990) * np.random.uniform(-0.5, 0.2)
            death_rate = max(10, base_death_rate + year_trend + np.random.normal(0, 5))

            base_pm25 = np.random.uniform(8, 25)
            pm25_trend = (year - 1990) * np.random.uniform(-0.1, 0.3)
            pm25 = max(5, base_pm25 + pm25_trend + np.random.normal(0, 2))

        plot_data_rows.append(
            {
                "Entity": country,
                "Year": year,
                "Death.Rate": round(death_rate, 1),
                "PM2.5": round(pm25, 1),
            }
        )

# Create DataFrames
map_data_oecd = pd.DataFrame(map_data_rows)
plot_data_oecd = pd.DataFrame(plot_data_rows)

# Create dummy polygon data for choropleth maps
polygon_data = pd.DataFrame(
    {
        "Entity": [country["Entity"] for country in countries],
        "geometry": [
            f"POLYGON(({country['lon'] - 2} {country['lat'] - 2}, {country['lon'] + 2} {country['lat'] - 2}, {country['lon'] + 2} {country['lat'] + 2}, {country['lon'] - 2} {country['lat'] + 2}, {country['lon'] - 2} {country['lat'] - 2}))"
            for country in countries
        ],
    }
)

# Legacy variables (in case the original code references these)
map_data_world_bank = map_data_oecd.copy()  # Same data for compatibility
plot_data_world_bank = plot_data_oecd.copy()  # Same data for compatibility
