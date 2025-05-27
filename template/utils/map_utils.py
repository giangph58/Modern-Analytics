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

    # Find the min and max values for better scaling
    max_funds = geodata["TotalFunds"].max() if "TotalFunds" in geodata.columns else 0

    for _, row in geodata.iterrows():
        # Create more detailed popup information
        popup_html = f"""
        <div style='min-width: 150px'>
            <b>{row.Entity}</b><br>
            <b>Healthy Life Years:</b> {round(row.get("HealthyLifeYears", 0), 1)}<br>
            <b>GDP:</b> ${int(row.get("GDP", 0)):,}<br>
            <b>EU Funding:</b> ${int(row.get("TotalFunds", 0)):,}
        </div>
        """

        popup = HTML(popup_html)

        # Scale circle size based on funding amount
        funding = row.get("TotalFunds", 0)
        radius = 5
        if max_funds > 0:
            radius = max(5, min(20, (funding / max_funds) * 20))

        circle_marker = CircleMarker(
            location=[row["latitude"], row["longitude"]],
            radius=radius,
            weight=1,
            color="white",
            opacity=0.7,
            fill_color=determine_circle_color(row.get("HealthyLifeYears", 0)),
            fill_opacity=0.7,
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

    try:
        # Print diagnostic information
        print(f"Points data columns: {points_data.columns.tolist()}")
        print(f"Polygon data columns: {polygon_data.columns.tolist()}")

        combined_data = merge(
            polygon_data, points_data, left_on="Entity", right_on="Entity", how="inner"
        )

        print(f"Combined data size: {len(combined_data)}")

        if len(combined_data) > 0:
            # Create the GeoJSON data
            geo_data = dataframe_to_geojson(combined_data)

            # Use healthy life years as the choropleth data
            choro_data = dict(zip(combined_data["Entity"], combined_data["TotalFunds"]))

            choropleth_layer = Choropleth(
                geo_data=geo_data,
                choro_data=choro_data,
                colormap=linear.YlOrRd_09,  # Different color scheme for health data
                value_min=50,  # Adjust based on your health data range
                value_max=75,  # Adjust based on your health data range
                style={
                    "weight": 2,
                    "opacity": 1,
                    "fillOpacity": 0.7,
                    "color": "white",
                    "dashArray": "3",
                },
                hover_style={
                    "weight": 1,
                    "color": "#FFF",
                    "dashArray": "",
                    "fillOpacity": 0.8,
                    "bringToFront": True,
                },
            )

            # Add tooltips with funding information
            choropleth_layer.tooltip = HTML()

            polygons_layer.add_layer(choropleth_layer)
            print("Choropleth layer added successfully")
    except Exception as e:
        # Provide detailed error information
        print(f"Polygon rendering skipped: {e}")
        import traceback

        traceback.print_exc()


def filter_data(data: DataFrame, year: int) -> DataFrame:
    """Filter data by year"""
    return data[data["Year"] == year]


def dataframe_to_geojson(df: DataFrame) -> dict:
    """Convert DataFrame to GeoJSON format"""
    geojson = {"type": "FeatureCollection", "features": []}

    for _, row in df.iterrows():
        # Get coordinates from the merged data
        lat = row.get("latitude", 0)
        lon = row.get("longitude", 0)

        # Additional properties for tooltips
        properties = {
            "name": row["Entity"],
            "hly": row.get("HealthyLifeYears", 0),
            "gdp": row.get("GDP", 0),
            "funds": row.get("TotalFunds", 0),
        }

        # Create the GeoJSON feature
        feature = {
            "type": "Feature",
            "id": row["Entity"],
            "properties": properties,
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
