import streamlit as st
import src.format as fmt

def des_what():
    fmt.text_writing("""
                     
            ### 🌌 What is Astrazeus?
                     
            🌌 This is an interactive app where you can check the visibility of astronomical objects from our database. Here's how it works:
            
            ➡️ **Step 0: Customize your experience**
            - On top of this page, a section named **_Customize_** where you can change the background wallpaper 
                for a better experience :lower_left_paintbrush:
                     
            ➡️ **Step 1: Navigate through the app**
            - On your left sidebar there are app pages: **_Home_**, **_Geolocation_**, **_Library_** and **_Summit Feedback_** 
            """)
    _, col2, _ = st.columns(3)
    with col2:
        st.image("images/example/sidebar_pages.webp",use_container_width=False)    

    fmt.text_writing("""      
                                    
            ➡️ **Step 2: Choose your location (_Geolocation_ page)**
            - Enter an **external/manual location** 📍 or
            - Use your **current location** 📍
            
            ➡️ If _Local Location_ is chosen, on left sidebar there will be a slide option to enable permission to access your
                current location:
            """)
    col1, col2 = st.columns(2)
    with col1:
        st.image("images/example/local_location.webp",use_container_width=False)
    with col2:
        st.image("images/example/enable_local_location.webp",use_container_width=True)   

    fmt.text_writing("""      
                                    
            ➡️ If _External Location_ is chosen, it will appear two options: **_Coordinates_** and **_Address_**:
            - For _Coordinates_ option, the correct input are numbers corresponding to **Latitude**, **Longitude** and **Height**,
                as the example shows. To know more, expand _What are Latitude and Longitude?_
            - For _Address_ option, the correct input is with the format:\n
                     
                _(Street number) + Street name, Postal code + City, (Province), Country_
                as the example shows.
            """)
    _, col2, _ = st.columns(3)
    with col2:
        st.image("images/example/external_location.webp",use_container_width=False)
    col1, col2 = st.columns(2)
    with col1:
        st.image("images/example/external_location_coordinates.webp",use_container_width=False)
    with col2:
        st.image("images/example/external_location_address.webp",use_container_width=False)  

    fmt.text_writing("""     

            ➡️ **Step 3: Select your search mode**
                     
            On your left sidebar there are two modes:
            - Selecting **Multiple** stellar objects
            - Selecting **Individual** objects

            ➡️ **On 'Multiple':**
            - The app will tell you **how many categories there are** (e.g. Galaxy 🌌, Star 🌟, Planet 🌍)
            - Afterwards, you can **select up to 3 objects** from categories chosen to analyze in more detail, including 
                **current visibility** and **weather conditions** 🌃

            ➡️ **If you choose 'Individual':**
            - Simply **type the name of the object** (e.g. Andromeda 🌌, Sirius 🌟, Saturn 🪐)
                and discover its current visibility, including weather data 🌃
                     
            ➡️ After selecting the targets, **it is time to _Explore_**!:telescope:
            """)
    _, col2, col3, _ = st.columns(4)
    with col2:
        st.image("images/example/selection_multiple_format.webp",use_container_width=False)
    with col3:
        st.image("images/example/selection_individual_format.webp",use_container_width=False) 
    
    fmt.text_writing(""" 

        :exclamation::exclamation: AND THERE IS MORE :exclamation::exclamation:

        ➡️**Discover new data and images of each astronomical object in the _Library_!:books:**      
                      
        ➡️**Do not forget to summit your feedback!**

        🛰️ Head to the **left sidebar** to begin exploring! 🔭
        """)

    fmt.text_writing(""" 
                     
            ---
            ### :stars: **Example of results**
                     
            Next, it is displayed an example of results using _External Location_, _Coordinates_ option 
            for **Vega** star selected from _Individual_ search:
            
            ➡️ First, writing Barcelona coordinates at _Height = 50.00m_, it is seen that **Vega** in not
                currently visible
            """)
    st.image("images/example/vega_example_visibility.webp",use_container_width=False)
    fmt.text_writing(""" 
                     
            ➡️ Secondly, clicking on **_Explore_** different graphs appear giving information about:
            """)
    fmt.text_writing(""" 
                     
            ##### -> **Wheater**
            """)
    st.image("images/example/vega_example_results_1.webp",use_container_width=False)
    fmt.text_writing(""" 
                     
            ##### -> **Visibility over time**
            """)
    st.image("images/example/vega_example_results_2.webp",use_container_width=False)
    fmt.text_writing(""" 
                     
            ##### -> **Position over time**
            """)
    st.image("images/example/vega_example_results_3.webp",use_container_width=False)

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
            - European Space Agency (ESA): Hubble Space Telescope
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

    _, col9, col10, _ = st.columns(4)
    with col9:
        st.image("images/credits/nasa_logo.webp", use_container_width=True)
    with col10:
        st.image("images/credits/esa_logo.webp", use_container_width=True)

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
