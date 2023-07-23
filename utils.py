import streamlit as st
import toml
from PIL import Image
from datetime import datetime


@st.cache_data(ttl=3600)
def load_config(config_readme_path: str):
    """Loads information files"""
    config_readme = toml.load(config_readme_path)
    return dict(config_readme)


@st.cache_data(ttl=3600)
def load_image(image_path: str):
    """Loads an image"""
    return Image.open(image_path)


def display_links(repo_link, other_link) -> None:
    """Displays a repository and other link"""
    col1, col2 = st.sidebar.columns(2)
    col1.markdown(
        f"<a style='display: block; text-align: center;' href={repo_link}>Source code</a>",
        unsafe_allow_html=True,
    )
    col2.markdown(
        f"<a style='display: block; text-align: center;' href={other_link}>App introduction</a>",
        unsafe_allow_html=True,
    )


def is_daytime():
    # Get the current local time
    now = datetime.now()
    # Set the hours during which it's considered daytime (e.g., 6 AM to 6 PM)
    daytime_start = now.replace(hour=6, minute=0, second=0)
    daytime_end = now.replace(hour=18, minute=0, second=0)
    # Check if the current time is within the daytime range
    return daytime_start <= now <= daytime_end


general_parameters = [
    "um025",
    "humidity",
    "pressure",
    "um050",
    "temperature",
    "um003",
    "um005",
    "pm1",
    "pm10",
    "um100",
    "pm25",
    "um010",
    "voc",
    "pm4",
    "no",
    "no2",
    "o3",
    "so2",
    "co",
]

custom_markers = {
    "humidity": "&#x1F4A7;",  # Humidity - Raindrop Emoji
    "others": "&#x25B2;",
}

custom_css = """
    <style>
    .card {
        padding: 20px;
        border: 1px solid #ccc;
        border-radius: 10px;
        box-shadow: 5px 5px 10px rgba(0, 0, 0, 0.1);
    }
    .card-title {
        font-size: 24px;
        font-weight: bold;
        margin-bottom: 10px;
    }
    .card-content {
        font-size: 16px;
        color: white;
    }
    </style>
    """


def create_custom_markdown_card(text):
    # Apply custom CSS styles to the card
    st.markdown(custom_css, unsafe_allow_html=True)
    # Create the card
    st.markdown(
        """
        <div class="card">
            <div class="card-title">Information</div>
            <div class="card-content">
            """
        + text
        + """
        
        </div>
            """,
        unsafe_allow_html=True,
    )
    st.write("")
    st.write("")
    st.write("")
