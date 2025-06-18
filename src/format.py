import streamlit as st
import base64
from pathlib import Path
from time import sleep
import numpy as np
import src.database as db

def get_base64_of_image(image_path):
    """
    Receive an image path to decode using base64.
    """
    with open(image_path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

def decode_image_from_folder(folder_path):
    """
    Select all images from path ending with ".webp" in order to decode every image.
    Used to generate optimized images for the page.
    Return a list of decoded images.
    """
    path = Path(folder_path)
    images = [img.name for img in sorted(path.glob("*.webp"))]
    return [get_base64_of_image(path / img) for img in images]

def page_format(bg_index,sb_index,n_page):
    """
    Format page for the whole app. It includes background images, sidebar images, text format and foot notes
    for every image.
    Inputs are bg_index (background index) and sb_index (sidebar index) using st.session_state respectively, also 
    n_page is used to determine page configuration.
    """
    image1 = decode_image_from_folder("images/background_picture")
    url1 = ["https://apod.nasa.gov/apod/ap230510.html",                 #1
            "https://apod.nasa.gov/apod/ap231201.html",                 #2
            "https://apod.nasa.gov/apod/ap240801.html",                 #3
            "https://apod.nasa.gov/apod/ap240529.html",                 #4
            "https://apod.nasa.gov/apod/ap231227.html",                 #5
            "https://apod.nasa.gov/apod/ap240429.html",                 #6
            "https://apod.nasa.gov/apod/ap240729.html",                 #7
            "https://apod.nasa.gov/apod/ap240131.html",                 #8
            "https://apod.nasa.gov/apod/ap240805.html",                 #9
            "https://apod.nasa.gov/apod/ap250209.html"]                 #10
    name1 = ["Amr Abdulwahab",                                          #1
             "José Rodrigues",                                          #2
             "Petr Horálek (Institute of Physics, Opava)",              #3
             "Marcin Rosadziński",                                      #4
             "Stefano Pellegrini",                                      #5
             "Juan Carlos Casado",                                      #6
             "Max Inwood",                                              #7
             "Marcin Ślipko",                                           #8
             "Makrem Larnaout",                                         #9
             "Michael Goh"]                                             #10
    color1 = ["#ffffff" for _ in range(len(image1))]
    source1 = ["APOD (NASA)" for _ in range(len(image1))]
    image2 = decode_image_from_folder("images/sidebar_picture")
    url2 = ["https://apod.nasa.gov/apod/ap240911.html",                 #1
            "https://apod.nasa.gov/apod/ap240812.html",                 #2
            "https://apod.nasa.gov/apod/ap230716.html",                 #3
            "https://apod.nasa.gov/apod/ap231117.html",                 #4
            "https://apod.nasa.gov/apod/ap231217.html",                 #5
            "https://apod.nasa.gov/apod/ap240221.html",                 #6
            "https://apod.nasa.gov/apod/ap230529.html",                 #7
            "https://apod.nasa.gov/apod/ap240827.html",                 #8
            "https://apod.nasa.gov/apod/ap241228.html",                 #9
            "https://apod.nasa.gov/apod/ap240729.html",                 #10
            "https://apod.nasa.gov/apod/ap241105.html",                 #11
            "https://apod.nasa.gov/apod/ap240309.html",                 #12
            "https://apod.nasa.gov/apod/ap230809.html"]                 #13
    name2 = ["Marcin Rosadziński",                                      #1
             "Josh Dury",                                               #2
             "Nicholas Roemmelt",                                       #3
             "Dennis Lehtonen",                                         #4
             "Hongyang Luo",                                            #5
             "Dheera Venkatraman",                                      #6
             "Petr Horálek (Institute of Physics, Opava)",              #7
             "Pau Montplet Sanz",                                       #8
             "Włodzimierz Bubak",                                       #9
             "Max Inwood",                                              #10
             "Josh Dury",                                               #11
             "Petr Horálek (Institute of Physics, Opava)",              #12
             "Petr Horálek (Institute of Physics, Opava)"]              #13
    color2 = ["#ffffff" for _ in range(len(image2))]
    source2 = ["APOD (NASA)" for _ in range(len(image2))]
    if n_page == 0:
        st.set_page_config(
            page_title="Home",
            page_icon=":house:",
            layout="centered",
            initial_sidebar_state="auto" 
            )
    elif n_page == 1:
        st.set_page_config(
            page_title="Geolocation",
            page_icon="📡", 
            layout="centered",
            initial_sidebar_state="auto"
            )
    elif n_page == 2:
        st.set_page_config(
            page_title="Library",
            page_icon=":mag:",
            layout="centered",
            initial_sidebar_state="auto"
            )
    elif n_page == 3:
        st.set_page_config(
            page_title="Feedback",
            page_icon=":memo:",
            layout="centered",
            initial_sidebar_state="auto"
            )
    elif n_page == 4:
        st.set_page_config(
            page_title="Extract",
            page_icon=":lock:",
            layout="centered",
            initial_sidebar_state="auto" 
            )
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/webp;base64,{image1[bg_index]}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        .highlight-box {{
            background-color: rgba(0, 0, 0, 0.7);
            padding: 1em;
            border-radius: 0.5em;
            font-family: 'Arial', sans-serif;
            font-size: 0.9rem;
            color: #ffffff;
            margin-bottom: 1em;
        }}
        .footer {{
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: rgba(0, 0, 0, 0.5);
        color: #ffffff;
        text-align: center;
        font-size: 1.0rem;
        padding: 10px;
        }}
        /* For all streamlit widgets and elements */
        html, body, [class^="css"] {{
            color: green !important;
            font-family: 'Arial', sans-serif;
        }}
        h1, h2, h3, h4, h5, h6{{
            color: white !important;
        }}
        p {{
            color: white !important;
        }}
        .stMarkdown {{
            color: white !important;
        }}
        section[data-testid="stSidebar"] {{
            background-image: url("data:image/webp;base64,{image2[sb_index]}");
            background-size: cover;
            background-repeat: no-repeat;
            background-position: center;
            }}
        </style>
        <div class="footer">
            Image taken by 
            <a href="{url1[bg_index]}" target="_blank" style="color: {color1[bg_index]};">
                {name1[bg_index]}</a>
                via {source1[bg_index]}
        </div>
        """,
        unsafe_allow_html=True
    )
    st.sidebar.markdown(f"""
            <div style="background-color: rgba(0, 0, 0, 0.6);font-size: 0.85rem; color: {color2[sb_index]}; margin-top: 0.1em;">
                Image taken by  
                <a href="{url2[sb_index]}" target="_blank" style="color: {color2[sb_index]};">
                    {name2[sb_index]}</a> 
                     via {source2[sb_index]}
            </div>
            """, unsafe_allow_html=True)
    for _ in range(2):
        st.sidebar.markdown("<br>", unsafe_allow_html=True)
    return

def get_session_state_format(n_page):
    """
    Function to initialize every concept of st.session_state.
    Only recive the integer number of the page as follows:
    - For 'Home' = 0
    - For 'Geolocation' = 1
    - For 'Library' = 2
    - For 'Summit Feedback' = 3
    """
    if "bg_index" not in st.session_state:
        st.session_state.bg_index = 0
    if "sb_index" not in st.session_state:
        st.session_state.sb_index = 0
    if "locate_input" not in st.session_state:
        st.session_state.locate_input = ""
    if "geocode_done" not in st.session_state:
        st.session_state.geocode_done = False
    if "meteo_api_weather" not in st.session_state:
        st.session_state.meteo_api_weather = False
    if "meteo_utcoffset" not in st.session_state:
        st.session_state.meteo_utcoffset = ""
    if "meteo_api_image" not in st.session_state:
        st.session_state.meteo_api_image = None
    if "openai_day_1" not in st.session_state:
        st.session_state.openai_day_1 = False
    if "idiom" not in st.session_state:
        st.session_state.idiom = "English"
    if 'seed_num_random' not in st.session_state:
        seed_num_random = np.random.randint(1, 100)
        st.session_state.seed_num_random = seed_num_random
    if 'data' not in st.session_state:
        st.session_state.data = db.astro_data_recommendation()
    page_format(st.session_state.bg_index, st.session_state.sb_index,n_page)
    # NAMES FOR ST.SESSION_STATE
    # bg_index = "Background image index"
    # sb_index = "Sidebar image index"
    # locate_input = "Address input"
    # geocode_done = "Geocode.xyz API TRUE/FALSE"
    # latitude_geo = "Geocode.xyz API latitude"
    # longitude_geo = "Geocode.xyz API longitude"
    # meteo_api_weather = "MeteoBlue API DONE/NOT DONE"
    # meteo_api_image = "MeteoBlue API Image DONE/NOT DONE"
    # openai_day_1 = "OpenAI API weather 1 day DONE/NOT DONE"
    # meteo_data = "MeteoBlue weather data in DataFrame"
    # meteo_units = "MeteoBlue weather data units in DataFrame"
    # meteo_utcoffset = "MeteoBlue UTC time offset data"
    # openai_json_1_day = "OpenAI API weather 1 day JSON"
    # idiom = "Language for App"
    # seed_num_random = "NumPy random number seed"
    # data = "JSON database for sk-learn"
    return

# def highlight_altitude(row):
#     """
#     Recive a data row 
#     """
#     color = 'background-color: lightgreen; color: black' if row['Altitude'] > 0 else 'background-color: lightcoral; color: black'
#     return [color] * len(row)

def get_altitude_icon(alt):
    """
    Recive a value and return a color emoji.
    """
    return "🟢" if alt > 0 else "🔴"

def limits(value, min, max,name):
    """
    Recive three string value inputs and convert them to float to set a limit range.
    Used to limit coordinates where the format selection is external location and 'Coordinates' mode.
    Return a warning if False, else True.
    """
    if not float(min) <= float(value) <= float(max):
        st.warning(f"{name} value must be between {min} and {max}!")
    else:
        return True

def text_writing(text, display=False, button=True, opacity=0.4):
    """
    This function permits to animate text like writing on real time. Reciving a text as input, there are two
    options to manipulate the animation. First, with display, if False there is no animation. Else, if True
    and button True too, a st.button is displayed to skip the animation and shows whole text. 
    A third input determines the opacity's area of the text.

    """
    placeholder = st.empty()
    style = f"""
            <div style='
                background-color: rgba(0, 0, 0, {opacity});
                padding: 1em;
                border-radius: 0.5em;
                font-family: 'Arial', sans-serif;
                font-size: 10px;
                color: #ffffff;
            '>{{}}</div>
            """
    if text:
        if display==True:
            if button==True:
                skip_button = st.button("Go to full text")
                try:
                    with st.spinner("Writing..."):
                        if skip_button:
                            placeholder.markdown(style.format(text), unsafe_allow_html=True)
                        else:
                            for i in range(1, len(text) + 1):
                                placeholder.markdown(style.format(text[:i]), unsafe_allow_html=True)
                                sleep(0.025)
                except:
                    st.write(text)
            else:
                for i in range(1, len(text) + 1):
                    placeholder.markdown(style.format(text[:i]), unsafe_allow_html=True)
                    sleep(0.025)
        else:
            placeholder.markdown(style.format(text), unsafe_allow_html=True)
    return