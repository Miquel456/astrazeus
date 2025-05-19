import streamlit as st
from streamlit_js_eval import get_geolocation
import src.database as db
import astropy.units as u
from astropy.coordinates import AltAz, EarthLocation, SkyCoord
from astropy.time import Time
from datetime import datetime, timezone
from astroquery.simbad import Simbad
from time import sleep
import src.extraction as ext
import src.format as fmt
import pandas as pd
import src.description as des

fmt.get_session_state_format(n_page=0)

fmt.text_writing("""
                 
            ## 🌌 Welcome to the Astrazeus App!
            """)
tab1, tab2, tab3 = st.tabs(["What is it?", "Customize", "Credits"])

with tab1:
    des.des_what()

with tab2:
    fmt.text_writing("""
                
            ### Customize your experience :art:
            
            ➡️ **Select a background image**: Choose from a variety of stunning backgrounds to enhance your experience.
                     
            ➡️ **Select a sidebar**: Choose from a variety of breathtaking backgrounds for sidebar to enhance your experience.
            """)
    # BACKGROUND SELECTOR
    with st.container():
        st.write("---")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("< Previous background", key="back_bg"):
                st.session_state.bg_index = max(0, st.session_state.bg_index - 1)
        with col2:
            if st.button("Next background >", key="follow_bg"):
                st.session_state.bg_index = min(9, st.session_state.bg_index + 1)

    # SIDEBAR SELECTOR
    with st.container():
        st.write("---")
        col3, col4 = st.columns(2)
        with col3:
            if st.button("< Previous sidebar", key="prev_sb"):
                st.session_state.sb_index = max(0, st.session_state.sb_index - 1)
        with col4:
            if st.button("Next sidebar >", key="next_sb"):
                st.session_state.sb_index = min(12, st.session_state.sb_index + 1)
with tab3:
    des.des_credits()