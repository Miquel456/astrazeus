import streamlit as st
import src.format as fmt
import src.description as des

fmt.get_session_state_format(n_page=0)

fmt.text_writing("""
                 
            ## 🌌 Welcome to the Astrazeus App!
            """)
tab1, tab2, tab3 = st.tabs(["What is it?", "Customize", "Credits"])

with tab1:
    des.des_what()
with tab2:
    des.des_custom()
with tab3:
    des.des_credits()