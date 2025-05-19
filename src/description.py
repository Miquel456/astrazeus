import streamlit as st
import src.format as fmt

def des_what():
    fmt.text_writing("""
                     
            ### 🌌 What is Astrazeus?
                     
            🌌 This is an interactive app where you can check the visibility of astronomical objects from our database. Here's how it works:
                     
            ➡️ **Step 1: Choose your location**
            - Enter an **external/manual location** 📍 or
            - Use your **current location** 📍

            ➡️ **Step 2: Select your search mode**
            - **By Category** (e.g. Galaxy 🌌, Star 🌟, Planet 🌍)  
            - **By Name** (e.g. Andromeda 🌌, Sirius 🌟, Saturn 🪐)

            ➡️ **If you choose 'Category':**
            - The app will tell you **how many objects are currently visible**
            - You can **select up to 5 objects** to analyze in more detail, including **weather conditions** 🌃

            ➡️ **If you choose 'Individual':**
            - Simply **type the name of the object** and discover its current visibility, including weather data 🌃

            ---

            🛰️ Head to the **left sidebar** to begin exploring! 🔭
            """)
def des_credits():
    fmt.text_writing("""
                     
            ### :copyright: Credits
            
            Made by **Astrazeus** team :rocket:
                     
            - **Miquel Pujol**: Physicist and Data Scientist
            
            Powered by:
                     
            - **Streamlit**: Web app framework
            - **Python**: programming language
            
            Libraries and APIs:
            - **MeteoBlue**: Weather data
            - **Astropy**: Astronomy calculations
            - **Astroquery.Simbad**: Astronomy database queries
            - **Skyfield**: Astronomy calculations
            - **OpenAI**: ChatGPT API
            - **Geocode.xyz**: Geocoding API
            - **Streamlit geolocator**: Geolocation API
                     
            Images:
            - National Aeronautics and Space Administration (NASA): Astronomy Picture of the Day (APOD)
            """)
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.image("images/credits/streamlit_logo.webp", use_container_width=True)
    with col2:
        st.image("images/credits/astropy_project_logo.svg", use_container_width=True)
    with col3:
        st.image("images/credits/simbad_logo.svg", use_container_width=True)
    with col4:
        st.image("images/credits/skyfield_logo.webp", use_container_width=True)
    
    col5, col6, col7, col8 = st.columns(4)
    with col5:
        st.image("images/credits/python_logo.webp", use_container_width=True)
    with col6:
        st.image("images/credits/geocode_logo.webp", use_container_width=True)
    with col7:
        st.image("images/credits/OpenAI_logo.webp", use_container_width=True)
    with col8:
        st.image("images/credits/meteoblue_logo_2024.webp", use_container_width=True)

    col9, col10, col11, col12 = st.columns(4)
    with col9:
        st.image("images/credits/nasa_logo.webp", use_container_width=True)
    # with col10:
    #     st.image("images/credits/esa_logo.webp", use_container_width=True)

def des_coord():
    fmt.text_writing("""
                     
        ###  🌍 Latitude and Longitude

        Latitude and Longitude are geographic coordinates used to specify any location on Earth :globe_with_meridians:.

        ➡️ **Latitude** measures how far **north or south** a location is from the equator  
        • Range: **-90° to +90°**

        ➡️ **Longitude** measures how far **east or west** a location is from the Prime Meridian  
        • Range: **-180° to +180°**

        These values are expressed in **decimal degrees**:  
        - Positive **latitude** → **Northern Hemisphere**  
        - Positive **longitude** → **Eastern Hemisphere**

        📍 For example, the coordinates for **Barcelona, Spain** are:  
        - **Latitude**: 41.38879  
        - **Longitude**: 2.15899  

        :world_map: This means Barcelona is **41.39° north** of the equator and **2.16° east** of the Prime Meridian. 
        """)

    st.image("https://bam.files.bbci.co.uk/bam/live/content/z74msbk/large", use_container_width=True)

    fmt.text_writing("""
        <div style='text-align: right; font-size: 0.9em; color: #ffffff;'>
            Image from 
            <a href='https://bam.files.bbci.co.uk/bam/live/content/z74msbk/large' target='_blank' style='color: #ffffff;'>BBC</a>'s files
        </div>
        """, False)
