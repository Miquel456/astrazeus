import src.format as fmt
import src.extraction as ext
import streamlit as st

fmt.get_session_state_format(n_page=1)
fmt.text_writing("""
                 
            ## 📍Geolocation :pushpin::earth_americas:
            """)
tab_names = ["Local Location", "External Location"]
active_tab = st.radio("Select a mode:", tab_names, horizontal=True)
if active_tab == "Local Location":
    ext.local_location()
elif active_tab == "External Location":
    ext.ext_location()