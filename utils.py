import streamlit as st
import toml
from PIL import Image
from datetime import datetime


@st.cache_data(ttl=300)
def load_config(config_readme_path: str):
    """Loads information files"""
    config_readme = toml.load(config_readme_path)
    return dict(config_readme)


@st.cache_data(ttl=300)
def load_image(image_path: str):
    """Loads an image"""
    return Image.open(image_path)


from typing import Any, Dict, List
import streamlit as st


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
