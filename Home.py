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

fmt.page_format()

st.header("🌌 Welcome to the NightSky&Weather App!")
tab1, tab2 = st.tabs(["What is it?","Credits"])
with tab1:
    des.des_what()
with tab2:
    des.des_credits()