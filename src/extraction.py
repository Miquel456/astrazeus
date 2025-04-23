from skyfield.api import load
from astropy.coordinates import AltAz, SkyCoord, EarthLocation
import astropy.units as u
from datetime import datetime, timezone
from astropy.time import Time
import src.database as db
import pandas as pd
import streamlit as st
import src.format as fmt
from streamlit_js_eval import get_geolocation
import matplotlib.pyplot as plt
import numpy as np
from time import sleep
import src.description as des

def planet_visible(name, location):
    # Carreguem efemèrides i temps actual
    planets = load('de440s.bsp')
    ts = load.timescale()
    t = ts.from_datetime(datetime.now(timezone.utc))

    # Diccionari amb noms vàlids de planetes
    valid_planets = {
        'mercury': 'mercury barycenter',
        'venus': 'venus barycenter',
        'mars': 'mars barycenter',
        'jupiter': 'jupiter barycenter',
        'saturn': 'saturn barycenter',
        'uranus': 'uranus barycenter',
        'neptune': 'neptune barycenter',
    }

    # Comprovem si el nom és vàlid
    planet_key = valid_planets.get(name.lower())
    if not planet_key:
        raise ValueError(f"'{name}' is not a recognized planet name.")

    # Observador des de la Terra cap al planeta
    earth = planets['earth']
    observer = planets[planet_key]
    astrometric = earth.at(t).observe(observer)

    # Transformem a coordenades celestes
    ra = str(astrometric.radec()[0]).replace(' ', '')
    dec = str(astrometric.radec()[1]).replace(' ', '').replace('deg', 'd').replace("'", 'm').replace('"', 's')
    coord = SkyCoord(ra=ra, dec=dec, frame='icrs')

    # Temps i marc de coordenades AltAz
    now = Time(datetime.now(timezone.utc))
    altaz_frame = AltAz(obstime=now, location=location)

    # Transformació a AltAz
    coord_altaz = coord.transform_to(altaz_frame)
    altitude = round(coord_altaz.alt.deg, 2)
    azimuth = round(coord_altaz.az.deg, 2)

    return altitude, azimuth


def object_visible(name, location):
    now = Time(datetime.now(timezone.utc))
    res = SkyCoord.from_name(name)
    resaltaz = res.transform_to(AltAz(obstime=now, location=location))
    altitude = round(resaltaz.alt.deg,2)
    azimut = round(resaltaz.az.deg,2)
    return altitude, azimut

def location_coord():
    loc = get_geolocation()
    if loc:
        acc = loc['coords']['accuracy']
        lat = loc['coords']['latitude']
        lon = loc['coords']['longitude']
        time = Time(datetime.now(timezone.utc))
        return acc,lat,lon,time
    else:
        st.error("Geolocation data could not be retrieved. Please ensure location permissions are enabled.")

def visibility_df(choice,lat,lon,h=0,display=False):
    location = EarthLocation(lat=lat * u.deg, lon=lon * u.deg, height=h * u.m)

    name1 = db.data_conn()['name']
    name2 = db.data_conn()['name_2']
    obtype = db.data_conn()['ob_type']

    # Inicialitzar una llista per guardar les dades
    result_data = []

    for i, j, k in zip(name1, name2, obtype):
        if k in choice or i in choice:
            try: 
                alt, _ = planet_visible(i, location)
            except Exception:
                try:
                    alt, _ = object_visible(i, location)
                except Exception:
                    alt, _ = object_visible(j, location)

            result_data.append({
                "Name": i,
                "Type": k,
                "Altitude": alt,
                "Visibility": fmt.get_altitude_icon(alt)
            })

    df = pd.DataFrame(result_data)
    lst_obj_vis = []
    try:
        if not df.empty:
            styled_df = df.style.format({'Altitude': '{:.2f}'})
            visibles = df[df['Altitude'] > 0]
            for i in visibles['Name']:
                lst_obj_vis.append(i)
            if display == True:
                st.dataframe(styled_df)
    except:
        st.info("No object/s found for the filters selected!")
    return lst_obj_vis

def obj_results_visible(list,lat,lon,height):
    selected = st.segmented_control(label="Visible objects:", options=list, selection_mode="multi")
    if not list:
        st.info("No objects found for the selected categories!")
    else:
        if st.button("Explore!", type="primary"):
            if len(selected) == 0:
                st.warning("No object selected!")
            elif len(selected) <= 5:
                for i in selected:
                    with st.spinner("Charging the results..."):
                        sleep(2)
                        st.subheader(i)
                        graph_position(i,lat,lon,height)
            else:
                st.warning("Only 5 objects at the same time!")

def selection(lat,lon,height=0):
    selection = st.sidebar.pills(label="Select format search:", options=["Category","Individual"],selection_mode="single")
    try:
        if selection == "Category":
            category_choice = st.sidebar.multiselect("CATEGORY:", db.data_conn()['ob_type'].unique(),placeholder="Name of the category")
            if category_choice:
                try:
                    if st.checkbox("Show table", False):
                        table = visibility_df(category_choice, lat, lon,height,display=True)
                        try:
                            obj_results_visible(table,lat,lon,height)
                        except:
                            st.warning("No data available for the selected filters!")
                    else:
                        table = visibility_df(category_choice, lat, lon,height,display=False)
                        if table is None:
                            st.warning("No data available for the selected filters!")
                        obj_results_visible(table,lat,lon,height)
                except:
                    st.info("Select category object.")
        if selection == "Individual":
            one_choice = st.sidebar.selectbox("INDIVIDUAL OBJECT:", db.data_conn()['name'],placeholder="Name of the object", index = None)
            if one_choice:
                one_choice = [one_choice]
                try:
                    if st.checkbox("Show table", False):
                        table = visibility_df(one_choice, lat, lon,height,display=True)
                        try:
                            obj_results_visible(table,lat,lon,height)
                        except:
                            st.warning("No data available for the selected filters!")
                    else:
                        table = visibility_df(one_choice, lat, lon,height,display=False)
                        if table is None:
                            st.warning("No data available for the selected filters!")
                        obj_results_visible(table,lat,lon,height)
                except:
                    st.info("Write name object.")                
    except:
        st.info("Choose a category to analyze!")

def graph_position(name, lat, lon, h=0):
    location = EarthLocation(lat=lat*u.deg, lon=lon*u.deg, height=h*u.m)
    
    fig = plt.figure(figsize=(6, 6))
    ax = fig.add_subplot(111, polar=True)

    ax.set_theta_zero_location("N")  # Nord a dalt
    ax.set_theta_direction(-1)       # Sentit horari

    ax.set_xticks(np.radians([0, 90, 180, 270]))
    ax.set_xticklabels(['North\n0°', 'East\n90°', 'South\n180°', 'West\n270°'])

    ax.set_yticks(np.arange(0, 91, 10))
    ax.set_yticklabels(['Zenith'] + ['']*8 + ['Horizon'])
    ax.set_rlim(0, 90)

    # colors = plt.cm.tab10.colors  # paleta per a múltiples objectes
    #  color=colors[idx % len(colors)]

    # for idx, obj in enumerate(name_list):
    try:
        for i, j in zip(db.data_conn()['name'], db.data_conn()['ob_type']):
            if i == name:
                if j.lower() == 'planet':
                    alt, az = planet_visible(i, location)
                else:
                    alt, az = object_visible(i, location)

        alt = 90 - alt  # pas a distància zenital
        ax.plot(np.radians(az), alt, '*', mew=1.5)
        ax.annotate(name, xy=(np.radians(az), alt), xytext=(5, 5),
                    textcoords='offset points', fontsize=9)
    except Exception as e:
        st.warning(f"Could not retrieve position for {name}: {e}")

    ax.set_title("Sky Chart", va='bottom', fontsize=14)
    ax.legend(loc="lower left", fontsize=8)

    st.pyplot(fig)

def ext_location():
    st.subheader(":stars: Astronomical objects with proposed location :pushpin:")
    help = st.expander("What are Latitude and Longitude?",False)
    with help:
        des.des_coord()

    # col1, col2, col3 = st.columns(3)

    # with col1:
    try:
        lat = st.sidebar.number_input(label="Latitude (°)", value=None, step=0.00001,
                            format="%0.5f", placeholder="e.g. 41.38879")
        lat_res = fmt.limits(lat, -90.0, 90.0)
    except:
        pass
    # with col2:
    try:
        lon = st.sidebar.number_input(label="Longitude (°)", value=None, step=0.00001,
                            format="%0.5f", placeholder="e.g. 2.15899")
        lon_res = fmt.limits(lon, -180.0, 180.0)
    except:
        pass

    # with col3:
    try:
        height = st.sidebar.number_input(label="Height (m)", value=None, step=0.10,
                                format="%0.2f", placeholder="e.g. 50.00")
        h_res = fmt.limits(height, 0.0, 9000.0)
    except:
        pass

    try:
        if lat_res and lon_res and h_res:
            selection(lat_res,lon_res,h_res)
    except:
        st.sidebar.info("Need all coordinates!")

def local_location():
    st.subheader(":stars: Astronomical objects with your current location 📍")
    act_loc = st.sidebar.toggle("Location")
    if act_loc:
        loc = location_coord()
        if loc:
            acc = loc[0]
            lat = loc[1]
            lon = loc[2]
            now = loc[3]

            if acc > 35:
                st.warning("The precision is too low. Please refresh the page or check your network.")
                st.write(acc)
            else:
                selection(lat,lon)
    else:
        st.info("Enable first the access to your location")