import streamlit as st
import src.format as fmt
import src.database as db
import src.extraction as ext

fmt.get_session_state_format(n_page=2)

fmt.text_writing("""
                 
            # :telescope: Library :book:
            """)
fmt.text_writing("""
                 
            ### Welcome :wave:
            
            This is the **_Library_**, a place to satisfy curiosity and expand your knowledge about 
            the little lights that inhabit the sky.
            """)

with st.expander("RECOMMENDATIONS FOR YOU",False):
    st.info("Working on clustering!")
with st.expander("RECCOMENDATIONS FROM OTHER USERS"):
    st.info("Working on KNN!")

categories = [i for i in db.data_conn()['ob_type'].unique()]
category = st.segmented_control("Choose a category:", categories, selection_mode='single')
planets = ['Venus','Jupiter','Saturn','Mars','Mercury']
objects = []
if category:
    for i, ob_type in zip(db.data_conn()['name'], db.data_conn()['ob_type']):
        if ob_type == category:
            objects.append(i)
    name = st.pills("Choose an object:", objects, selection_mode='single')
    if name:
        try:
            text,image = db.astro_object_description(name)
            if image != "":
                fmt.text_writing(text,True)
                if name in planets:
                    with st.spinner("Creating 3D map..."):
                        ext.create_3d_planet(name)
                st.image(image, caption=f"{name} from ESA/Hubble")
            else:
                fmt.text_writing(text,True)
                if name in planets:
                    with st.spinner("Creating 3D map..."):
                        ext.create_3d_planet(name)

        except Exception as e:
            st.error(f"Error: {e}")
