from branca.colormap import linear
from ipyleaflet import Choropleth, CircleMarker, LayerGroup
from ipywidgets import HTML
from numpy import isnan
from pandas import DataFrame, merge


def determine_circle_radius(num: float) -> int:
    """Circles are scaled differently in ipyleaflet compared to R/Leaflet,
    hence different coefficients.
    """
    if isnan(num):
        return 5

    num = int(num)

    bins = [range(10), range(10, 20), range(20, 25)]
    coefficients = [1.1, 0.8, 0.75]
    final_coef = 0.2

    for bin, coef in zip(bins, coefficients):
        if num in bin:
            return int(num * coef)
    return int(num * final_coef)


def determine_circle_color(num: float) -> str:
    if isnan(num):
        return "#D2D2D2"
    num = int(num)

    bins = [
        range(1),
        range(1, 2),
        range(2, 5),
        range(5, 10),
        range(10, 20),
        range(20, 50),
        range(50, 100),
    ]
    colors = [
        "#F7FCF0",
        "#E0F3DB",
        "#CCEBC5",
        "#A8DDB5",
        "#7BCCC4",
        "#4EB3D3",
        "#2B8CBE",
    ]
    final_color = "#08589E"

    for bin, color in zip(bins, colors):
        if num in bin:
            return color
    return final_color


def add_circles(geodata: DataFrame, circle_layer: LayerGroup) -> None:
    """Layer data is updated by reference, hence None return"""
    circle_layer.clear_layers()
    circle_markers = []
    for _, row in geodata.iterrows():
        popup = HTML(f"<b>{row.Entity}:</b></br>" + str(round(row["Death.Rate"], 2)))
        circle_marker = CircleMarker(
            location=[
                row["latitude"],
                row["longitude"],
            ],  # Updated to match dummy data columns
            radius=determine_circle_radius(row["Death.Rate"]),
            weight=1,
            color="white",
            opacity=0.7,
            fill_color=determine_circle_color(row["PM2.5"]),
            fill_opacity=0.5,
            popup=popup,
        )
        circle_markers.append(circle_marker)
    points = LayerGroup(layers=circle_markers)
    circle_layer.add_layer(points)


def add_polygons(
    polygon_data: DataFrame,
    points_data: DataFrame,
    polygons_layer: LayerGroup,
) -> None:
    """Add choropleth polygons to the map"""
    polygons_layer.clear_layers()

    # For dummy data, we'll create a simple choropleth
    # In a real app, you'd merge with actual polygon geometries
    try:
        combined_data = merge(
            polygon_data, points_data, left_on="Entity", right_on="Entity", how="inner"
        )
        if len(combined_data) > 0:
            # Create a simple choropleth layer
            # Note: This is simplified for dummy data
            geo_data = dataframe_to_geojson(combined_data)
            choro_data = dict(zip(combined_data["Entity"], combined_data["Death.Rate"]))

            choropleth_layer = Choropleth(
                geo_data=geo_data,
                choro_data=choro_data,
                colormap=linear.GnBu_09,
                value_min=0,
                value_max=70,
                style={
                    "weight": 2,
                    "opacity": 1,
                    "fillOpacity": 0.5,
                    "color": "white",
                    "dashArray": "3",
                },
                hover_style={
                    "weight": 1,
                    "color": "#FFF",
                    "dashArray": "",
                    "fillOpacity": 0.8,
                    "bringToFront": False,
                },
            )
            polygons_layer.add_layer(choropleth_layer)
    except Exception as e:
        # If polygon rendering fails, just skip it for now
        print(f"Polygon rendering skipped: {e}")


def filter_data(data: DataFrame, year: int) -> DataFrame:
    """Filter data by year"""
    return data[data["Year"] == year]


def dataframe_to_geojson(df: DataFrame) -> dict:
    """Convert DataFrame to GeoJSON format"""
    geojson = {"type": "FeatureCollection", "features": []}

    for _, row in df.iterrows():
        # Create simple polygon around each country point for dummy data
        lat = row.get("latitude", 0)
        lon = row.get("longitude", 0)

        feature = {
            "type": "Feature",
            "id": row["Entity"],
            "properties": {"name": row["Entity"]},
            "geometry": {
                "type": "Polygon",
                "coordinates": [
                    [
                        [lon - 2, lat - 2],
                        [lon + 2, lat - 2],
                        [lon + 2, lat + 2],
                        [lon - 2, lat + 2],
                        [lon - 2, lat - 2],
                    ]
                ],
            },
        }
        geojson["features"].append(feature)

    return geojson
