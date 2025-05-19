import streamlit as st
import src.format as fmt
import src.extraction as ext
import requests
from openai import OpenAI
from time import sleep
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from astropy.visualization import astropy_mpl_style, quantity_support
import astropy.units as u
from astropy.coordinates import AltAz, EarthLocation, SkyCoord
from astropy.time import Time
from datetime import datetime, timezone, timedelta
import itertools

fmt.get_session_state_format(n_page=4)
fmt.text_writing("""
            
            # :robot_face: AI description 🪐
            """)

def astro_description(params):
    text = f"""
        🪐 Object Information:
        - Name: {params['name']}
        - Category: {params['category']}
        - Right Ascension (RA): {params['ra']} (in hms format)
        - Declination (DEC): {params['dec']} (in degrees, minutes, and seconds)
        - Apparent Magnitude: {params['app_mag']}
        - Absolute Magnitude: {params['abs_mag']}
        - Mass: {params['mass']}
        - Radius: {params['radius']}
        - Distance from Earth: {params['distance']} 

        📚 Using this data, write a captivating, easy-to-understand, and scientifically accurate description 
        of the object for a general audience.

        ➡️ If the category is **Star**, compare its apparent and absolute magnitudes to those of the Sun 
        (Apparent Magnitude: -26.74, Absolute Magnitude: 4.83).

        ➡️ If the category is **Planet**, compare its mass and radius to Earth's 
        (Mass: 5.97x10²⁴ kg, Radius: 6.37x10³ km).

        🎯 The tone should be **engaging, informative, and inspiring**, making the reader feel fascinated by astronomy.
    """
    return text

# content = astro_description(params)
# ia = st.button("description")
# if ia:
#       result = ext.open_ai(content, temp=0.6, max_tokens=400, model="gpt-3.5-turbo", mode="astro_des")
#       st.write(result)

st.warning("PROBLEMS WITH PLANET GRAPHIC ALTITUDE WITH FILLED AREA!")
