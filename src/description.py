import streamlit as st

def des_what():
    # st.header("🌌 Welcome to the NightSky&Weather App!")
    # st.write('This is an interactive App where you can find the visibility of an astronomical object in our database. Choose an option ' \
    #      'to start with, using external, manual location:pushpin: or your local, current location:round_pushpin:.')
    # st.write('After that choice, decide if you are searching for categories, i.e. Galaxy :milky_way:, Star:stars: or '\
    #          'Planet:earth_africa:; or searching by its name, i.e. Andromeda:milky_way:, Sirius:star2: or Saturn:ringed_planet:.')
    # st.write('If \'Category\' is selected, the program will tell you how many objects are visible at the moment. '\
    #         'Choose up to five objects to analyze with weather conditions:night_with_stars:.')
    # st.write('If \'Individual\' is selected, write the popular name of the object and know if it is visible or not '\
    #          'with weather conditions:night_with_stars:.')
    # st.write('Go to the left sidebar to explore:telescope:!')
    # st.write("This is an interactive app where you can explore the visibility of astronomical objects from our database.")
    # st.write("Start by choosing your location method: either enter coordinates manually :pushpin: or use your current location :round_pushpin:.")
    # st.write("Next, decide if you'd like to search by *category* — for example, Galaxy :milky_way:, Star :stars:, or Planet :earth_africa: — or by *name*, such as Andromeda :milky_way:, Sirius :star2:, or Saturn :ringed_planet:.")
    # st.write("If you select 'Category', the app will show how many objects are currently visible. Choose up to five to analyze with real-time weather conditions :night_with_stars:.")
    # st.write("If you select 'Individual', simply enter the object's popular name to check its visibility along with weather conditions :night_with_stars:.")
    # st.write("Ready to explore? Head to the sidebar and start your journey :telescope:!")
    st.markdown("""
            This is an interactive app where you can check the visibility of astronomical objects from our database. Here's how it works:

            ➡️ **Step 1: Choose your location**
            - Enter an **external/manual location** :pushpin: or
            - Use your **current location** :round_pushpin:

            ➡️ **Step 2: Select your search mode**
            - **By Category** (e.g. Galaxy :milky_way:, Star :stars:, Planet :earth_africa:)  
            - **By Name** (e.g. Andromeda :milky_way:, Sirius :star2:, Saturn :ringed_planet:)

            ➡️ **If you choose 'Category':**
            - The app will tell you **how many objects are currently visible**
            - You can **select up to 5 objects** to analyze in more detail, including **weather conditions** :night_with_stars:

            ➡️ **If you choose 'Individual':**
            - Simply **type the name of the object** and discover its current visibility, including weather data :night_with_stars:

            ---
            🛰️ Head to the **left sidebar** to begin exploring! :telescope:
            """)
def des_credits():
    st.write("Credits for:")

def des_coord():
    # st.write("Latitude and Longitude are geographic coordinates used to specify any location on Earth:globe_with_meridians:.")
    # st.markdown("-> Latitude measures how far north or south a location is from the equator (ranging from -90° to +90°).")
    # st.markdown("-> Longitude measures how far east or west a location is from the Prime Meridian (ranging from -180° to +180°).")
    # st.write("These values are expressed in decimal degrees. Positive latitude values are in the Northern Hemisphere, "\
    #          "and positive longitude values are in the Eastern Hemisphere.")
    # st.write("📍 For instance, the coordinates for Barcelona, Spain are:")
    # st.markdown("* Latitude: 41.38879")
    # st.markdown("* Longitude: 2.15899")
    # st.write("This means Barcelona is 41.39° north of the equator and 2.16° east of the Prime Meridian.")
    # st.image("https://bam.files.bbci.co.uk/bam/live/content/z74msbk/large", use_container_width=True)
    # st.markdown("""
    #         <div style='text-align: right; font-size: 0.9em; color: #aaa;'>
    #             Image from 
    #             <a href='https://bam.files.bbci.co.uk/bam/live/content/z74msbk/large' target='_blank' style='color: #aaa;'>BBC</a>
    #             's files
    #         </div>
    #         """, unsafe_allow_html=True)
    st.markdown("""
        ### 🌍 Latitude and Longitude

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

        This means Barcelona is **41.39° north** of the equator and **2.16° east** of the Prime Meridian.

        """)

    st.image("https://bam.files.bbci.co.uk/bam/live/content/z74msbk/large", use_container_width=True)

    st.markdown("""
        <div style='text-align: right; font-size: 0.9em; color: #aaa;'>
            Image from 
            <a href='https://bam.files.bbci.co.uk/bam/live/content/z74msbk/large' target='_blank' style='color: #aaa;'>BBC</a>'s files
        </div>
        """, unsafe_allow_html=True)
