import streamlit as st

def page_format():

    image1 = 'https://images.pexels.com/photos/7622345/pexels-photo-7622345.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2'
    image2 ='https://images.pexels.com/photos/861443/pexels-photo-861443.jpeg?auto=compress&cs=tinysrgb&w=600'

    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("{image1}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        .footer {{
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: rgba(250, 250, 250, 0.0);
        color: #ffffff;
        text-align: center;
        font-size: 0.8rem;
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
            background-image: url("{image2}");
            background-size: cover;
            background-repeat: no-repeat;
            background-position: center;
            }}
        
        </style>
        <div class="footer">
            Imatge taken by 
            <a href="https://www.pexels.com/photo/cel-nit-espai-vespre-2666598/" target="_blank" style="color: #aaa;">
                Adam Krypel</a>
                via Pexels
        </div>
        """,
        unsafe_allow_html=True
    )
    
    st.sidebar.markdown("""
            <div style="font-size: 0.8rem; color: black; margin-top: 2em;">
                Image taken by  
                <a href="https://www.pexels.com/photo/861443/" target="_blank" style="color: black;">
                    Alex Andrews</a> 
                     via Pexels
            </div>
            """, unsafe_allow_html=True)
    for _ in range(2):
        st.sidebar.markdown("<br>", unsafe_allow_html=True)

def highlight_altitude(row):
    color = 'background-color: lightgreen; color: black' if row['Altitude'] > 0 else 'background-color: lightcoral; color: black'
    return [color] * len(row)

def get_altitude_icon(alt):
    return "🟢" if alt > 0 else "🔴"

def limits(value, min, max):
    if not float(min) <= float(value) <= float(max):
        st.warning(f"Value must be between {min} and {max}!")
    else:
        return True

