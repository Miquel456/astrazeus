import streamlit as st
import src.format as fmt

fmt.get_session_state_format(n_page=3)
fmt.text_writing("""
                
        # :mailbox_with_mail: Let know your opinion! :pencil: 
        """)
st.link_button("To the survey!", 
        url='https://docs.google.com/forms/d/e/1FAIpQLScJ9MMkNIfjNO_fNHxP0rKsMiaAXnq-C8wCnEpYlZT9LaxrWA/viewform?usp=header')