import streamlit as st
import src.format as fmt
import src.extraction as ext
import pandas as pd
import numpy as np
from sklearn.neighbors import NearestNeighbors

fmt.get_session_state_format(n_page=2)
fmt.text_writing("""
                
        # :telescope: Library :book:
        """)
fmt.text_writing("""
                
        ### Welcome :wave:
        
        This is the **_Library_**, a place to satisfy curiosity and expand your knowledge about 
        the little lights that inhabit the sky.
        """)
ext.library()
with st.expander("RECOMMENDATIONS FOR YOU",False):
        ext.astro_recommendation_own_user()
with st.expander("RECOMMENDATIONS FROM OTHER USERS",False):
        ext.astro_recommendation_other_users()