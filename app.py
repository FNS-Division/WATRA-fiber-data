import streamlit as st
from streamlit_folium import st_folium
import geopandas as gpd
import folium

st.title("Fiber networks in WATRA countries")

# Load your datasets
gdf_lines = gpd.read_file("lines/combined_lines.geojson")
gdf_nodes = gpd.read_file("nodes/combined_nodes.geojson")
gdf_submarine_cables = gpd.read_file("submarine/cables.geojson")
gdf_submarine_points = gpd.read_file("submarine/points.geojson")
gdf_ixps = gpd.read_file("IXP/ixp.geojson")

# Get center of map
center = gdf_lines.geometry.unary_union.centroid
m = folium.Map(location=[center.y, center.x], zoom_start=6)

# Create popup fields for each dataset
def create_popup_fields(gdf, fields):
    """Create popup fields for folium GeoJson"""
    popup_fields = []
    aliases = []
    for field in fields:
        if field in gdf.columns:
            popup_fields.append(field)
            # Create nice aliases for display
            alias = field.replace('_', ' ').title()
            aliases.append(alias)
    return popup_fields, aliases

# Add fiber lines (exclude capacity_Tbps and region)
line_fields = ['line_id', 'status', 'operator_name', 'from', 'to', 'distance', 
               'data_source', 'data_source_year', 'country']
popup_fields, aliases = create_popup_fields(gdf_lines, line_fields)

folium.GeoJson(
    gdf_lines,
    name="Fiber Lines",
    popup=folium.GeoJsonPopup(fields=popup_fields, aliases=aliases),
    style_function=lambda x: {
        'color': 'blue',
        'weight': 1,
        'opacity': 0.8
    }
).add_to(m)

# Add nodes (all fields)
node_fields = ['node_id', 'country', 'longitude', 'latitude', 'infrastructure_type', 
               'operator_name', 'node_status', 'type_infr', 'data_source', 'data_source_year']
popup_fields, aliases = create_popup_fields(gdf_nodes, node_fields)

folium.GeoJson(
    gdf_nodes,
    name="Nodes",
    popup=folium.GeoJsonPopup(fields=popup_fields, aliases=aliases),
    marker=folium.CircleMarker(radius=2, color='blue', fill=False, fillOpacity=0, weight=2)
).add_to(m)

# Add submarine cables
cable_fields = ['name', 'capacity_Tbps', 'year_service', 'length_km']
popup_fields, aliases = create_popup_fields(gdf_submarine_cables, cable_fields)

folium.GeoJson(
    gdf_submarine_cables,
    name="Submarine Cables",
    popup=folium.GeoJsonPopup(fields=popup_fields, aliases=aliases),
    style_function=lambda x: {
        'color': 'green',
        'weight': 2,
        'opacity': 0.7,
        'dashArray': '5, 5'
    }
).add_to(m)

# Add submarine landing points
point_fields = ['name', 'cables_count', 'first_cable_name']
popup_fields, aliases = create_popup_fields(gdf_submarine_points, point_fields)

folium.GeoJson(
    gdf_submarine_points,
    name="Submarine Landing Points",
    popup=folium.GeoJsonPopup(fields=popup_fields, aliases=aliases),
    marker=folium.CircleMarker(radius=4, color='green', fill=True, fillColor='lightgreen', fillOpacity=0.8)
).add_to(m)

# Add IXPs
ixp_fields = ['country', 'name']
popup_fields, aliases = create_popup_fields(gdf_ixps, ixp_fields)

folium.GeoJson(
    gdf_ixps,
    name="IXPs",
    popup=folium.GeoJsonPopup(fields=popup_fields, aliases=aliases),
    marker=folium.CircleMarker(radius=6, color='purple', fill=True, fillColor='purple', fillOpacity=0.8)
).add_to(m)

# Add layer control
folium.LayerControl().add_to(m)

# Add legend using folium's traditional approach
legend_html = '''
<div style="position: absolute; 
            top: 10px; right: 10px; width: 200px; 
            background-color: white; border:2px solid grey; z-index:9999; 
            font-size:12px; padding: 10px; box-shadow: 2px 2px 6px rgba(0,0,0,0.3);">
<p style="margin-top: 0; margin-bottom: 8px; font-weight: bold;">Fibre Infrastructure</p>
<p style="margin: 4px 0;"><span style="display: inline-block; width: 20px; height: 2px; background-color: blue; margin-right: 8px; vertical-align: middle;"></span>Fiber Lines</p>
<p style="margin: 4px 0;"><span style="display: inline-block; width: 8px; height: 8px; border: 2px solid blue; border-radius: 50%; margin-right: 8px; vertical-align: middle; background: white;"></span>Fiber Nodes</p>
<p style="margin: 4px 0;"><span style="display: inline-block; width: 20px; height: 1px; border-top: 2px dashed green; margin-right: 8px; vertical-align: middle;"></span>Submarine Cables</p>
<p style="margin: 4px 0;"><span style="display: inline-block; width: 8px; height: 8px; background-color: lightgreen; border-radius: 50%; margin-right: 8px; vertical-align: middle;"></span>Landing Points</p>
<p style="margin: 4px 0;"><span style="display: inline-block; width: 8px; height: 8px; background-color: purple; border-radius: 50%; margin-right: 8px; vertical-align: middle;"></span>IXPs</p>
</div>
'''

# Use a child HTML element for better positioning
legend_element = folium.Element(legend_html)
m.get_root().html.add_child(legend_element)

# Render in Streamlit
st_folium(m, width=800, height=800)