import src.format as fmt
import src.extraction as ext
import streamlit as st

fmt.page_format()
st.title("📍Geolocation :pushpin::earth_americas:")

tab_names = ["Local Location", "External Location"]
active_tab = st.radio("Select a mode", tab_names, horizontal=True)

if active_tab == "Local Location":
    ext.local_location()
elif active_tab == "External Location":
    ext.ext_location()