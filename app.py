import streamlit as st
import plotly.graph_objects as go
from connection import OpenAQConnection
from utils import *


st.set_page_config(page_title="OpenAQ Connection", layout="wide")

conn = st.experimental_connection("openaq", type=OpenAQConnection)
readme = load_config("config_readme.toml")


def visualize_variable_on_map(data_dict, variable):
    is_day = is_daytime()
    mapbox_style = "carto-darkmatter" if not is_day else "open-street-map"

    # Initialize lists to store data for multiple locations
    latitudes = []
    longitudes = []
    values = []
    display_names = []
    last_updated = []

    # Loop through the results and extract relevant data for each location
    for result in data_dict.get("results", []):
        measurements = result.get("parameters", [])
        for measurement in measurements:
            if measurement["parameter"] == variable:
                value = measurement["lastValue"]
                display_name = measurement["displayName"]
                latitude = result["coordinates"]["latitude"]
                longitude = result["coordinates"]["longitude"]
                last_updated_value = result["lastUpdated"]

                latitudes.append(latitude)
                longitudes.append(longitude)
                values.append(value)
                display_names.append(display_name)
                last_updated.append(last_updated_value)

    if not latitudes or not longitudes or not values:
        print(f"{variable} data not found.")
        return create_custom_markdown_card(
            f"{variable} data not found for the selected country."
        )

    # Create the visualization
    fig = go.Figure()

    marker = [
        custom_markers["humidity"]
        if variable == "humidity"
        else custom_markers["others"]
    ]

    # Add a single scatter mapbox trace with all locations
    fig.add_trace(
        go.Scattermapbox(
            lat=latitudes,
            lon=longitudes,
            mode="markers+text",
            marker=dict(
                size=20,
                color=values,
                colorscale="Viridis",  # You can choose other color scales as well
                colorbar=dict(title=f"{variable.capitalize()}"),
            ),
            text=[
                f"{marker[0]} {display_name}: {values[i]}<br>Last Updated: {last_updated[i]}"
                for i, display_name in enumerate(display_names)
            ],
            hoverinfo="text",
        )
    )

    # Update map layout
    fig.update_layout(
        mapbox=dict(
            style=mapbox_style,  # Choose the desired map style
            zoom=5,  # Adjust the initial zoom level as needed
            center=dict(
                lat=sum(latitudes) / len(latitudes),
                lon=sum(longitudes) / len(longitudes),
            ),
        ),
        margin=dict(l=0, r=0, t=0, b=0),
    )
    create_custom_markdown_card(information)
    st.plotly_chart(fig, use_container_width=True)


# Info
st.title("Air quality data map")
with st.expander("What is this app?", expanded=False):
    st.write(readme["app"]["app_intro"])
    st.write("")
st.write("")
st.sidebar.image(load_image("logo.png"), use_column_width=True)
display_links(readme["links"]["repo"], readme["links"]["other_link"])

with st.spinner("Loading the available countries..."):
    # Countries exist in first 2 pages
    countries = []
    for page in [1, 2]:
        countries_request = conn.query_countries(page=page)["results"]
        countries = countries + countries_request

    transformed_countries = {
        country["name"]: {
            "code": country["code"],
            "parameters": country["parameters"],
            "locations": country["locations"],
            "lastUpdated": country["lastUpdated"],
        }
        for country in countries
    }

    # Add a global for default when the app is initialised
    transformed_countries["Global"] = {
        "code": None,
        "parameters": general_parameters,
        "locations": None,
        "lastUpdated": None,
    }

# Parameters
st.sidebar.title("Selections")
selected_country = st.sidebar.selectbox(
    "Select the desired country",
    transformed_countries,
    placeholder="Country",
    index=len(transformed_countries) - 1,  # Gets the last one "Global"
    help=readme["tooltips"]["country"],
)

selected_viariable = st.sidebar.selectbox(
    "Select the desired variable",
    transformed_countries[selected_country]["parameters"],
    placeholder="Variable",
    index=1,
    help=readme["tooltips"]["variable"],
)

total_locations = transformed_countries[selected_country]["locations"]
last_time = transformed_countries[selected_country]["lastUpdated"]
information = f"The selected country is {selected_country}. The total found locations are {total_locations} with last updates at {last_time}."

code = transformed_countries[selected_country]["code"]
get_locations_response = conn.query(code)
visualize_variable_on_map(get_locations_response, selected_viariable)
