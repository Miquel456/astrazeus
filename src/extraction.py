import streamlit as st
import src.database as db
import src.description as des
import src.format as fmt
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import astropy.units as u
import requests
import http.client, urllib.parse
import json
import re
import itertools
from skyfield.api import load
from astropy.coordinates import AltAz, SkyCoord, EarthLocation
from datetime import datetime, timezone, timedelta
from astropy.time import Time
from astropy.visualization import astropy_mpl_style, quantity_support
from streamlit_js_eval import get_geolocation
from time import sleep
from PIL import Image
from openai import OpenAI
from itertools import chain
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import StandardScaler

def get_time(u_time, year, month, day, hour=0, minute=0):
    """
    Return time as datetime type. Inputs:
    u_time: universal time delay, like +2 UTC.
    year, month, day, hour and minute with the same meaning. Hour and minute are 0 as default.
    """
    tz = timezone(timedelta(hours=u_time))
    dt = datetime(year, month, day, hour, minute, tzinfo=tz)
    return dt

def planet_visible(name, location, u_time=0, length=24, multi=False):
    """
    From the file de440s.bsp, the function returns lists of altitude and azimuth coordinates
    for every planet in the Solar System from Earth Location.
    name: planet name.
    location: local location coordinates.
    u_time: universal time delay, like +2 UTC.
    lenght: hours quantity (24 == 1 day)
    multi: single query/object if False.
    """
    planets = load('src/de440s.bsp')
    valid_planets = {
        'mercury': 'mercury barycenter',
        'venus': 'venus barycenter',
        'mars': 'mars barycenter',
        'jupiter': 'jupiter barycenter',
        'saturn': 'saturn barycenter',
        'uranus': 'uranus barycenter',
        'neptune': 'neptune barycenter',
    }
    planet_key = valid_planets.get(name.lower())
    if not planet_key:
        raise ValueError(f"'{name}' is not a recognized planet name.")
    time_zone = timezone(timedelta(hours=u_time))
    if multi == False:
        ts = load.timescale()
        t = ts.from_datetime(datetime.now(time_zone))
        earth = planets['earth']
        observer = planets[planet_key]
        astrometric = earth.at(t).observe(observer)
        ra = str(astrometric.radec()[0]).replace(' ', '')
        dec = str(astrometric.radec()[1]).replace(' ', '').replace('deg', 'd').replace("'", 'm').replace('"', 's')
        coord = SkyCoord(ra=ra, dec=dec, frame='icrs')
        now = Time(datetime.now(time_zone))
        altaz_frame = AltAz(obstime=now, location=location)
        coord_altaz = coord.transform_to(altaz_frame)
        altitude = round(coord_altaz.alt.deg, 2)
        azimuth = round(coord_altaz.az.deg, 2)
    else:
        full_hours = []
        altitude = []
        azimuth = []
        ts = load.timescale()
        data = st.session_state.meteo_data
        begin_day = str(data['time'][0])
        dt = datetime.strptime(begin_day, "%Y-%m-%d %H:%M:%S")
        year = dt.year
        month = dt.month
        day = dt.day
        hour = dt.hour
        step = 24 / length
        for i in range(0, length, 1):
            hour_decimal = (hour + i * step) % 24
            h = int(hour_decimal)                 
            m = int((hour_decimal - h) * 60)      
            time = get_time(u_time, year, month, day, hour=h, minute=m)
            full_hours.append(time)
        for j in range(len(full_hours)):
            k = full_hours[j]
            t = ts.from_datetime(k)
            earth = planets['earth']
            observer = planets[planet_key]
            astrometric = earth.at(t).observe(observer)
            ra = str(astrometric.radec()[0]).replace(' ', '')
            dec = str(astrometric.radec()[1]).replace(' ', '').replace('deg', 'd').replace("'", 'm').replace('"', 's')
            coord = SkyCoord(ra=ra, dec=dec, frame='icrs')
            time = Time(k)
            altaz_frame = AltAz(obstime=time, location=location)
            coord_altaz = coord.transform_to(altaz_frame)
            altitude.append(round(coord_altaz.alt.deg, 2))
            azimuth.append(round(coord_altaz.az.deg, 2))

    return altitude, azimuth


def object_visible(name, location, u_time=0, multi=False):
    """
    Function that returns lists of altitude and azimuth coordinates that are not planets.
    name: object name.
    location: local location coordinates.
    u_time: universal time delay, like +2 UTC.
    multi: single query/object if False.
    """
    if multi == False:
        time_zone = timezone(timedelta(hours=u_time))
        time = Time(datetime.now(time_zone))
        res = SkyCoord.from_name(name)
        resaltaz = res.transform_to(AltAz(obstime=time, location=location))
        altitude = round(resaltaz.alt.deg,2)
        azimut = round(resaltaz.az.deg,2)
    else:
        full_hours = []
        altitude = []
        azimut = []
        data = st.session_state.meteo_data
        begin_day = str(data['time'][0])
        dt = datetime.strptime(begin_day, "%Y-%m-%d %H:%M:%S")
        year = dt.year
        month = dt.month
        day = dt.day
        hour = dt.hour
        for i in range(0,24,1):
            time = get_time(u_time, year, month, day, hour=(hour+i))
            full_hours.append(time)
        for j in range(len(full_hours)):
            k = full_hours[j]
            time = Time(k)
            res = SkyCoord.from_name(name)
            resaltaz = res.transform_to(AltAz(obstime=time, location=location))
            altitude.append(round(resaltaz.alt.deg,2))
            azimut.append(round(resaltaz.az.deg,2))

    return altitude, azimut

def location_coord():
    """
    Function that returns values such as acc (accuracy), lat (latitude) and lon (longitude)
    extracted from local location.
    """
    loc = get_geolocation()
    if loc:
        acc = loc['coords']['accuracy']
        lat = loc['coords']['latitude']
        lon = loc['coords']['longitude']
        return acc,lat,lon
    else:
        st.error("Geolocation data could not be retrieved." /
                 " Please ensure location permissions are enabled.")
    return

def visibility_df(choice,lat,lon,h=0,delta_time=0,display=False):
    """
    Returns a list of objects and determine if they are visible or not.
    choice = list of any type of objects.
    lat = latitude coordinate.
    lon = longitude coordinate.
    h = height. 0 as default.
    delta_time = universal time delay, like +2 UTC. +0 as default.
    display = display DataFrame of objects, with visibility or no, if True.
    """
    location = EarthLocation(lat=lat * u.deg, lon=lon * u.deg, height=h * u.m)
    name1 = db.data_conn()['name']
    name2 = db.data_conn()['name_2']
    obtype = db.data_conn()['ob_type']
    result_data = []
    for i, j, k in zip(name1, name2, obtype):
        if k in choice or i in choice:
            try: 
                alt, _ = planet_visible(i, location, u_time=delta_time)
            except Exception:
                try:
                    alt, _ = object_visible(i, location, u_time=delta_time)
                except Exception:
                    alt, _ = object_visible(j, location, u_time=delta_time)
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
            for i in df['Name']:
                lst_obj_vis.append(i)
            if display == True:
                st.dataframe(styled_df)
    except:
        st.info("No object/s found for the filters selected!")
    return lst_obj_vis

def weather_content(lat,lon,height=0):
    """
    Function that queries Meteoblue API and generates DataFrame saved into st.session_state.
    lat = latitude coordinate.
    lon = longitude coordinate.
    height = height. 0 as default.
    """
    api_key = st.secrets['meteo']['meteo_api_key']
    if not st.session_state.get("meteo_api_weather", False):
            params = {
                    "apikey": api_key,
                    "lat": lat,
                    "lon": lon,
                    "asl": height,
                    "format": "json"
            }
            response = requests.get("https://my.meteoblue.com/packages/basic-1h", params=params)
            if response.status_code == 200:
                data = response.json()
                try:
                    hourly_data = data["data_1h"]
                    df_data = pd.DataFrame(hourly_data)
                    df_units = pd.DataFrame(list(data["units"].items()), columns=["Parameter", "Unit"])
                    df_utcoffset = float(data["metadata"]["utc_timeoffset"])
                    df_data["time"] = pd.to_datetime(df_data["time"])
                    if not df_data.empty:
                        st.session_state.meteo_api_weather = True
                        st.session_state.meteo_data = df_data
                        st.session_state.meteo_units = df_units
                        st.session_state.meteo_utcoffset = df_utcoffset
                        return
                    else:
                        st.warning("The DataFrame is empty. Please check the data source.")
                except:
                    st.error("Something went wrong!")
            else:
                st.error(f"Petition error: {response.status_code}")
    else:
        return
        
def obj_results_visible(list,lat,lon,height,delta_time=0):
    """
    Function that returns the results of the objects selected in the 'list'.
    list: list of objects selected.
    lat = latitude coordinate.
    lon = longitude coordinate.
    height = height value.
    delta_time = universal time delay, like +2 UTC. +0 as default.
    """
    if not list:
        st.info("No object/s found for the selected method!")
    else:
        if st.button("Explore!", type="primary"):
            if len(list) == 0:
                st.warning("No object selected!")
            elif len(list) <= 3:
                for k in list:
                    for i, obj in enumerate(st.session_state.data):
                        if obj['name'] == k:
                            st.session_state.data[i]['interest'] += 1
                            if st.session_state.data[i]['interest'] >= 2:
                                st.session_state.data[i]['active'] = True
                with st.spinner(f"Charging the results..."):
                    weather_content(lat,lon,height)
                    meteo_image(lat,lon,height)
                    try:
                        data = st.session_state.meteo_data 
                        meteo_units = st.session_state.meteo_units
                        params, units = meteo_content_edit(data,meteo_units)               
                    except Exception as e:
                        st.error(f"Error: {e}")
                    for i in list:
                        with st.spinner(f"Getting results for {i}"):
                            for k, l in zip(db.data_conn()['name'], db.data_conn()['ob_type']):
                                if k and l:
                                    if k == i and l == 'Planet':   
                                        fmt.text_writing(f"""
                                         
            ## :ringed_planet: {i} 
            """)                         
                                    elif k == i:
                                        fmt.text_writing(f"""
                                         
            ## :dizzy: {i}
            """)
                                else:
                                    st.warning(f"Invalid data for object: Name={k}, Type={l}")
                            sleep(1)
                            full_visualization_ai(i,params,units,lat, lon, height=0, hours=24)
                            fmt.text_writing(f"""
                                         
            #### :calendar: Celestial map showing the positions of {i} throughout today's day
            """)
                            graph_position(i, lat, lon, height, u_time=delta_time,multi=True)
            else:
                st.warning("Only 3 objects at the same time!")
    return

def selection(lat,lon,height=0):
    """
    After passing the coordinates selection format, this function sums up the interaction by selecting multiple
    objects or individual objects.
    lat = latitude coordinate.
    lon = longitude coordinate.
    h = height. 0 as default.
    """
    selection = st.sidebar.pills(label="Select search format:", options=["Multiple","Individual"],selection_mode="single")
    try:
        if selection == "Multiple":
            category_choice = st.sidebar.multiselect("CATEGORY:", db.data_conn()['ob_type'].unique(),
                                                     placeholder="Name of the category")
            if category_choice:
                try:
                    objects_selected = []
                    if st.session_state.meteo_utcoffset == "":
                        utc_delta = st.slider("UTC Time Zone:", min_value=-12, max_value=+12, value=0)
                    else:
                        utc_delta = st.session_state.meteo_utcoffset
                    for i in range(len(category_choice)):
                        with st.expander(f"{category_choice[i].upper()}"):
                            filtered_df = db.data_conn()[db.data_conn()['ob_type'] == category_choice[i]]
                            choosen = st.pills(f"",
                                        [j for j in filtered_df['name']],
                                        selection_mode="multi")
                            if choosen:
                                objects_selected.append(choosen)
                    objects_selected = list(chain.from_iterable(objects_selected))
                    if len(objects_selected) <= 3:
                        try:
                            fmt.text_writing(f"""
                                         
            ##### :telescope: Current visibility UTC: {utc_delta}h :eye:
            """)
                            table = visibility_df(objects_selected, lat, lon, height,delta_time=utc_delta, display=True)
                            obj_results_visible(table, lat, lon, height,delta_time=utc_delta)
                        except Exception as e:
                            st.warning(f"No data available for the selected filters! {e}")
                    else:
                        st.warning("Up to 3 objects can be selected!")           
                except Exception as e:
                    st.info(f"Select category object. {e}")
        if selection == "Individual":
            one_choice = st.sidebar.selectbox("INDIVIDUAL OBJECT:", db.data_conn()['name'],
                                              placeholder="Name of the object", index = None)
            if one_choice:
                one_choice = [one_choice]
                if st.session_state.meteo_utcoffset == "":
                    utc_delta = st.slider("UTC Time Zone:", min_value=-12, max_value=+12, value=0)
                else:
                    utc_delta = st.session_state.meteo_utcoffset
                try:
                    fmt.text_writing(f"""
                                         
            ##### :telescope: Current visibility UTC: {utc_delta}h :eye:
            """)
                    table = visibility_df(one_choice, lat, lon, height,delta_time=utc_delta, display=True)
                    obj_results_visible(table, lat, lon, height,delta_time=utc_delta)
                except Exception as e:
                    st.warning(f"No data available for the selected filters! Error: {e}")
                except:
                    st.info(f"Write name object.")                
    except:
        st.info("Choose a category to analyze!")
    return

def graph_position(name, lat, lon, h=0, u_time=0, multi=False):
    """
    Generate a polar graph and plot the position for an object after collecting azimuth and altitude 
    coordinates of the object.
    name = name of the object or planet.
    lat = latitude coordinate.
    lon = longitude coordinate.
    h = height. 0 as default.
    u_time = universal time delay, like +2 UTC. +0 as default.
    multi = only plot a single object if False.
    """
    location = EarthLocation(lat=lat*u.deg, lon=lon*u.deg, height=h*u.m)
    az_list = []
    alt_list = []
    try:
        for i, j in zip(db.data_conn()['name'], db.data_conn()['ob_type']):
            if i == name:
                if multi == True:
                    if j.lower() == 'planet':
                        alt, az = planet_visible(i, location, u_time=u_time, multi=True)
                    else:
                        alt, az = object_visible(i, location, u_time=u_time, multi=True)
                    title_type = "Today Trajectory 24h"
                    for i, j in zip(alt, az):
                        az_list.append(np.radians(j))
                        alt_list.append(90 - i)
                else:
                    if j.lower() == 'planet':
                        alt, az = planet_visible(i, location, u_time=u_time, multi=False)
                    else:
                        alt, az = object_visible(i, location, u_time=u_time,multi=False)
                    title_type = "Now"
                    az_list.append(np.radians(az))
                    alt_list.append(90 - alt)
    except Exception as e:
        st.warning(f"Could not retrieve position for {name}: {e}")
        return
    fig = plt.figure(figsize=(6, 6))
    ax = fig.add_subplot(111, polar=True)
    ax.set_theta_zero_location("N")
    ax.set_theta_direction(-1)
    ax.set_xticks(np.radians([0, 90, 180, 270]))
    ax.set_xticklabels(['North\n0°', 'East\n90°', 'South\n180°', 'West\n270°'])
    ax.set_yticks(np.arange(0, 91, 10))
    ax.set_yticklabels(['Zenith'] + ['']*8 + ['Horizon'])
    ax.set_rlim(0, 90)
    ax.plot(az_list, alt_list, '*', mew=1.5, label=name)
    if len(az_list) > 24:
        for i in range(len(az_list)):
            ax.annotate(f"{i}h", xy=(az_list[i+12], alt_list[i+12]), xytext=(5, 5),
                    textcoords='offset points', fontsize=9)
    else:
        for i in range(len(az_list)):
            ax.annotate(f"{i}h", xy=(az_list[i], alt_list[i]), xytext=(5, 5),
                    textcoords='offset points', fontsize=9)
    ax.set_title(f"Sky Chart - {title_type}", va='bottom', fontsize=14)
    ax.legend(loc="lower left", fontsize=8)
    st.pyplot(fig)
    return

def create_3d_planet(planet):
    """
    Function that generates 3D interactive plot map with greyscales texture for planets.
    planet: name of the planet.
    """
    texture = Image.open(f"images/planet_texture/{planet.lower()}map.jpg").convert("L")
    texture_array = np.asarray(texture)
    h, w = texture_array.shape
    theta = np.linspace(0, 2 * np.pi, w)
    phi = np.linspace(0, np.pi, h)
    theta, phi = np.meshgrid(theta, phi)
    r = 1
    x = r * np.sin(phi) * np.cos(theta)
    y = r * np.sin(phi) * np.sin(theta)
    z = r * np.cos(phi)
    fig = go.Figure(data=[go.Surface(
        x=x, y=y, z=z,
        surfacecolor=texture,
        colorscale="greys",
        cmin=0,
        cmax=255,
        showscale=False
    )])
    fig.update_layout(
        title=f"🌐 {planet.title()} in 3D with greys colorscale",
        scene=dict(
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            zaxis=dict(visible=False),
            aspectmode='data'
        ),
        margin=dict(l=0, r=0, t=30, b=0)
    )
    st.plotly_chart(fig, use_container_width=True)
    return

def coordinates_location():
    """
    Interactive function that sums up the selection for 'External Location' and 'Coordinates' method.
    """
    help = st.expander("What are Latitude and Longitude?",False)
    with help:
        des.des_coord()
    col1, col2, col3 = st.columns(3)
    with col1:
        try:
            lat = st.number_input(label="Latitude (°)", value=None, step=0.00001,
                                format="%0.5f", placeholder="e.g. 41.38879")
            lat_res = fmt.limits(lat, -90.0, 90.0, name="Latitude")
        except:
            pass
    with col2:
        try:
            lon = st.number_input(label="Longitude (°)", value=None, step=0.00001,
                                format="%0.5f", placeholder="e.g. 2.15899")
            lon_res = fmt.limits(lon, -180.0, 180.0, name="Longitude")
        except:
            pass
    with col3:
        try:
            height = st.number_input(label="Height (m)", value=None, step=0.10,
                                    format="%0.2f", placeholder="e.g. 50.00")
            h_res = fmt.limits(height, 0.0, 9000.0, name="Height")
        except:
            pass
    try:
        if lat_res and lon_res and h_res:
                selection(lat,lon,height)
    except:
        st.info("Need all the coordinates!")
    return

def geocode_location():
    """
    Interactive function that queries Geocode API to get latitude and longitude coordinates.
    """
    st.sidebar.warning("⚠️ This method does not calculate the height!")
    locate_input = st.text_input("Enter a location:", placeholder="e.g. 27 Carretera de l'Observatori Fabra, 08035 Barcelona, Espanya")

    if locate_input:
        if st.session_state.geocode_done == False or st.session_state.locate_input != locate_input:
            st.session_state.locate_input = locate_input
            try:
                with st.spinner("Looking for coordinates..."):
                    conn = http.client.HTTPConnection('geocode.xyz')
                    params = urllib.parse.urlencode({
                        'locate': locate_input,
                        'json': 1
                    })
                    conn.request('GET', '/?{}'.format(params))
                    res = conn.getresponse()
                    data = res.read()
                    parsed_data = json.loads(data.decode('utf-8'))
                    standard = parsed_data.get('standard', {})
                    confidence = float(standard.get('confidence', 0))
                    if confidence >= 0.5:
                        st.session_state.geocode_done = True
                        st.session_state.latitude_geo = parsed_data['latt']
                        st.session_state.longitude_geo = parsed_data['longt']
                    else:
                        st.warning("""⚠️ Low confidence in the location. Please check the input.
                        Valid address format: \n
                        (Street number) + Street name, Postal code + City, (Province), Country
                        """)
                        st.session_state.geocode_done = False
            except:
                st.error("❌ Error with the API or address input.")
                st.session_state.geocode_done = False
    else:
        if st.session_state.get("geocode_done", True):
            st.sidebar.warning(f"⚠️ Using the previous location: {st.session_state.locate_input}")
        else:
            st.info("Write a location to get the coordinates.")
    return

def ext_location():
    """
    Interactive function that is used for 'External Location' choice.
    """
    fmt.text_writing("""
                     
        ### :stars: Astronomical objects with proposed location :pushpin:     
        """)
    decision = st.segmented_control(label="Select a method:", options=["Coordinates", "Address"], selection_mode="single")
    if decision == "Coordinates":
        coordinates_location()  
    elif decision == "Address":
        geocode_location()
        if st.session_state.get("geocode_done", False):
            lat_geo = float(st.session_state.latitude_geo)
            lon_geo = float(st.session_state.longitude_geo)
            selection(lat_geo, lon_geo)
    return

def local_location():
    """
    Interactive function that is used for 'Local Location' choice.
    """
    fmt.text_writing("""
                
            ### :stars: Astronomical objects with current location 📍
            """)
    act_loc = st.sidebar.toggle("Location")
    if act_loc:
        loc = location_coord()
        if loc:
            acc = loc[0]
            lat = loc[1]
            lon = loc[2]
            if acc > 35:
                st.warning("The precision is too low. Please refresh the page or check your network.")
                st.write(acc)
            else:
                selection(lat,lon)
    else:
        st.info("Enable first the access to your location on the left sidebar!")

def open_ai(content, temp, max_tokens=400, model="gpt-3.5-turbo", mode="astro_meteo"):
    """
    Funtcion that queries OpenAI API with different modes and models. It returns a JSON and a text.
    content: prompt content to ask AI.
    temp: temperature of the content. It ranges from 0 to 1, the lower more formal is.
    max_tokens: lenght of the total output. 400 as default.
    model: OpenAI model.
    mode: if 'astro_meteo' returns output with meteorological description. 
          If 'astro_des' returns output with astronomical object description.
    """
    openai_api_key = st.secrets["openai"]["openai_api_key"]
    client = OpenAI(api_key=openai_api_key)
    if mode == "astro_meteo":
        talk_form = (
            "You are a science communicator, expert in astronomy and meteorology. "
            "Given structured data, generate a public-friendly description and a JSON visibility evaluation. "
            "Be clear and engaging. End the text summary with these emojis: 🧑‍🚀🖖. "
            "Return the JSON in a separate block surrounded by triple backticks with 'json'."
        )
        try:
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": talk_form},
                    {"role": "user", "content": content}
                ],
                temperature=temp,
                max_tokens=max_tokens
            )
            full_response = response.choices[0].message.content
            json_match = re.search(r"(\[\s*{.*?}\s*\])", full_response, re.DOTALL)
            if json_match:
                try:
                    json_part = json.loads(json_match.group(1))
                except json.JSONDecodeError as err:
                    st.warning(f"⚠️ Error interpretant JSON: {err}")
                    json_part = []
            else:
                st.info("ℹ️ No s'ha trobat cap bloc JSON.")
                json_part = []
            text_part = full_response.replace(json_match.group(1), "").strip() if json_match else full_response
            text_part = text_part.replace(text_part[:13], "").strip()
            return json_part, text_part
        except Exception as e:
            st.error(f"❌ Error with API: {e}")
            return [], ""
    elif mode == "astro_des":
        talk_form = (
            "You are a science communicator, expert in astronomy. "
            "Given structured data, generate a public-friendly description. "
            "Be clear and engaging. End the text summary with these emojis: 🧑‍🚀🖖. "
        )
        try:
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": talk_form},
                    {"role": "user", "content": content}
                ],
                temperature=temp,
                max_tokens=max_tokens
            )
            full_response = response.choices[0].message.content
            return full_response
        except Exception as e:
            st.error(f"❌ Error with API: {e}")
            return

def astro_description(params):
    """
    Function that describes the prompt to generate a describtion of an object. Returns a text.
    params: dictionary with object parameters.
    """
    text = f"""
        🪐 Object Information:
        - Name: {params['name']}
        - Category: {params['category']}
        - Right Ascension (RA): {params['ra']} (in hms format)
        - Declination (DEC): {params['dec']} (in degrees, minutes, and seconds)
        - Apparent Magnitude: {params['app_mag']}
        - Absolute Magnitude: {params['abs_mag']}
        - Mass: {params['mass']}
        - Radius: {params['radius']}
        - Distance from Earth: {params['distance']} 

        📚 Using this data, write a captivating, easy-to-understand, and scientifically accurate description 
        of the object for a general audience.

        ➡️ If the category is **Star**, compare its apparent and absolute magnitudes to those of the Sun 
        (Apparent Magnitude: -26.74, Absolute Magnitude: 4.83).

        ➡️ If the category is **Planet**, compare its mass and radius to Earth's 
        (Mass: 5.97x10²⁴ kg, Radius: 6.37x10³ km).

        🎯 The tone should be **engaging, informative, and inspiring**, making the reader feel fascinated by astronomy.
    """
    return text

def build_weather_per_hour(params, units, hours):
    """
    Function that returns a dictionary with specific meteorological data.
    params: JSON with meteorological values.
    units: JSON meteorological units.
    hours: limit range to analize. (24 hours == 1 day)
    """
    times = params["time"]
    weather_list = []
    selected_indices = [i for i, _ in enumerate(params["time"]) if i <= hours]
    for i in selected_indices:
        weather_list.append({
            "time": times[i],
            "temperature": f"{params['temperature'][i]} {units['temperature'][0]}",
            "precipitation": f"{params['precipitation'][i]} {units['precipitation'][0]}",
            "precipitation_probability": f"{params['precipitation_probability'][i]} {units['precipitation_probability'][0]}",
            "sun": f"{params['sun'][i]} (0=night, 1=day)",
            "windspeed": f"{params['windspeed'][i]} {units['windspeed'][0]}",
            "winddirection": f"{params['winddirection'][i]} {units['winddirection'][0]}",
            "sealevelpressure": f"{params['sealevelpressure'][i]} {units['pressure'][0]}"
        })
    return weather_list

def meteo_description(params, units, hours, u_time = 0):
    """
    Function that returns a prompt with meteorogical data.
    params: JSON with meteorological values.
    units: JSON meteorological units.
    hours: limit range to analize. (24 hours == 1 day)
    u_time = universal time delay, like +2 UTC. +0 as default.
    """
    time_zone = timezone(timedelta(hours=u_time))
    time_now = datetime.now(time_zone)
    weather_data = build_weather_per_hour(params, units, hours)
    content = f"""
            You are an astronomy and meteorology expert helping the public understand observation conditions.

            Here is a list of hourly weather conditions:

            ```json
            {json.dumps(weather_data, indent=2, default=str)}
            ```
            Based on this:

            1. With the purpose of observing astronomical objects,
            return a list of JSON objects with visibility evaluations for every hourly weather conditions like this:
            [
                {{
                    "time": "...",
                    "visibility": "🟢/🟡/🔴",
                    "reason": "..."
                }},
                ...
            ]
            Instructions:
                - If the field `"sun"` equals 0, it is nighttime and **preferred** for observing stars or faint astronomical objects.
                - If `"sun"` is 1, it is daytime and **less ideal** for observing stars, unless the object is the Sun or a bright planet.
                - Other parameters to consider: cloud coverage, wind speed, and precipitation.
                - Use 🟢 for ideal conditions, 🟡 for acceptable but suboptimal, 🔴 for poor visibility.

            2. Then, provide a short and captivating summary for the public:

                - Mention the best hours (🟢).
                - Recommend the best closest hour to {time_now}.
                - End with these emojis: 🧑‍🚀🖖.

            Only return the JSON block and the summary. Do not include explanations.
            """
    return content

def meteo_image(lat,lon,height = 0):
    """
    Function that queries Meteoblue API to get meteorological image, saved to st.session_state.
    lat = latitude coordinate.
    lon = longitude coordinate.
    height = height. 0 as default.
    """
    if not st.session_state.get("meteo_api_image", None):
        api_key = st.secrets['meteo']['meteo_api_key']
        params = {
                "apikey": api_key,
                "lat": lat,
                "lon": lon,
                "asl": height,
                "format": "png"
                }
        url = "https://my.meteoblue.com/images/meteogram_one"
        response = requests.get(url, params=params)
        if response.status_code == 200:
            st.session_state.meteo_api_image = response.content
            return  
        else:
            st.error(f"Error downloading image: {response.status_code}")
            st.write(response.text)
    else:
        return

def meteo_content_edit(data,meteo_units):
    """
    From Meteoblue API data requests, it modifies to collect specific data.
    Returns list of weather parameters and units.
    data: JSON with weather data.
    meteo_units: meteorological units.
    """
    params = data[['precipitation', 'windspeed', 'precipitation_probability', 'relativehumidity', 
                    'temperature', 'time', 'sealevelpressure', 'winddirection']]
    units = {i: [] for i in meteo_units["Parameter"]}
    for j, index in zip(units.keys(), meteo_units.index):
            units[j].append(meteo_units["Unit"][index])
    params['sun'] = data['isdaylight'] 
    return params, units

def meteo_df_edition(dataframe):
    """
    Function that modifies a DataFrame to add rows for time, changing range from 1 hour to every 5 minutes.
    Returns modified DataFrame.
    dataframe: DataFrame to modify.
    """
    df = dataframe.drop(columns=['reason'])
    emoji_map = {
            "🟠": "🟡",
            }
    df['visibility'] = df['visibility'].replace(emoji_map)
    df_final = df
    for i in range(0,len(df)-1):
        for j in range(1,12):
            if j == 1:
                new_row = pd.DataFrame({
                                "time": [f"{df.loc[i, 'time'][:13]}:05:00"],
                                "visibility": [df.loc[i, 'visibility']]
                                })
            else:
                new_row = pd.DataFrame({
                        "time": [f"{df.loc[i, 'time'][:13]}:{str(10+(5*(j-2)))}:00"],
                        "visibility": [df.loc[i, 'visibility']]
                        })
            insert_at = j+12*i
            df_top = df_final.iloc[:insert_at]
            df_bottom = df_final.iloc[insert_at:]
            df_final = pd.concat([df_top, new_row, df_bottom], ignore_index=True)
    return df_final

def fill_visibility_areas(ax, times, altitudes, visibilities):
    """
    Function that fills the area between the axis with green, yellow and red.
    ax: axis.
    times: time list.
    altitudes: altitude coordinates.
    visibilities: list of visibility (green, yellow, red)
    """
    colors = {"🟢": "green", "🟡": "yellow", "🔴": "red"}
    labels_map = {"🟢": "Good visibility", "🟡": "Partial visibility", "🔴": "Poor visibility"}
    already_labeled = set()
    for vis, group in itertools.groupby(zip(times, altitudes, visibilities), key=lambda x: x[2]):
        group = list(group)
        if len(group) < 2:
            continue
        x_vals = [g[0] for g in group]
        y_vals = [g[1] for g in group]
        label = labels_map[vis] if vis not in already_labeled else None
        already_labeled.add(vis)
        ax.fill_between(x_vals, y_vals, 0, color=colors[vis], alpha=0.3, label=label)
    return

def plotting_meteo_data(object, dataframe, lat, lon, height=0, u_time=0, show_time=True):
    """
    Function that plots the meteorogical data.
    object: name of the object.
    dataframe: DataFrame.
    lat = latitude coordinate.
    lon = longitude coordinate.
    height = height. 0 as default.
    u_time = universal time delay, like +2 UTC. +0 as default.
    show_time = plots a vertical line to current time if True.
    """
    location = EarthLocation(lat=lat * u.deg, lon=lon * u.deg, height=height * u.m)
    init_time = Time(dataframe['time'][0])
    data_conn = db.data_conn()
    if object in data_conn['name'].values or object in data_conn['name_2'].values:
        object_type = data_conn.loc[data_conn['name'] == object, 'ob_type'].values
        if len(object_type) > 0 and object_type[0] == 'Planet':
            try:
                altitudes, _ = planet_visible(object, location, u_time=u_time, length=len(dataframe),multi=True)
            except Exception as e:
                st.error(f"Error: {e}")
            one_day = np.linspace(0, 24, len(dataframe)) * u.hour
            full_time = init_time + one_day
        else:
            try:
                name = SkyCoord.from_name(object)
            except Exception as e:
                st.error(f"Error: {e}")
                return
            one_day = np.linspace(0, 24, len(dataframe)) * u.hour
            full_time = init_time + one_day
            one_day_frame = AltAz(obstime=full_time, location=location)
            namealtaz = name.transform_to(one_day_frame)
            altitudes = namealtaz.alt
    plt.style.use(astropy_mpl_style)
    quantity_support()
    fig, ax = plt.subplots()
    ax.plot(one_day, altitudes, label=object, color="black", linewidth=1)
    fill_visibility_areas(ax, one_day, altitudes, dataframe['visibility'])
    fig.autofmt_xdate()
    ax.legend(loc="upper left")
    if show_time:
            time_zone = timezone(timedelta(hours=u_time))
            time_now = datetime.now(time_zone).hour + datetime.now(time_zone).minute / 60
            ax.axvline(x=time_now, color="black", linestyle="--", linewidth=1)
            if time_now < 23:
                    ax.text(time_now + 0.2, 10, "Current Time", rotation=90, verticalalignment='bottom', color="black")
            else:
                    ax.text(time_now - 0.7, 10, "Current Time", rotation=90, verticalalignment='bottom', color="black")
    ax.set_xlim(0, 24)
    ax.set_xticks(np.arange(0, 25, 1))
    ax.set_xlabel(f"Day {dataframe['time'][0][:10]} (24h)")
    ax.set_ylim(0, 90)
    ax.set_ylabel("Altitude [deg]")
    st.pyplot(fig)
    return

def full_visualization_ai(object,params,units,lat, lon, height=0, hours=24):
    """
    Function that sums up and plot all weather data and object position.
    object: name of the object.
    params: weather parameters.
    units: weather units.
    lat = latitude coordinate.
    lon = longitude coordinate.
    height = height. 0 as default.
    hours = limit range to plot (24 == 1 day as default)
    """
    with st.spinner("Weather forecasting with AI..."):
        if not st.session_state.get("openai_day_1", False):
            df_json = None
            try:
                utcoffset = st.session_state.meteo_utcoffset
                prompt = meteo_description(params=params, units=units, hours=hours, u_time=utcoffset)
                if not prompt:
                    st.error("Failed to generate prompt. Please check the input parameters.")
                    return
                json, text = open_ai(prompt, max_tokens=1500, temp=0.7)
                if not json or not text:
                    st.error("Failed to get a response from the AI API. Please check the API configuration.")
                    return             
                try:
                    fmt.text_writing(text, True, False)
                except Exception as e:
                    st.warning(f"Failed to format text: {e}")
                    st.write(text)
                df_json = pd.DataFrame(json)
                if df_json.empty:
                    st.error("The AI API returned an empty response. Please try again.")
                    return
                image = st.session_state.get("meteo_api_image", None)
                if image:
                    st.image(image, use_container_width=True)
                    fmt.text_writing("""
                        <div style='text-align: right; font-size: 0.9em; color: #ffffff;'>
                                Seven days prediction by Meteoblue
                        </div>
                        """, False)
                else:
                    st.warning("No image available from Meteoblue API.")
                df_meteo = meteo_df_edition(df_json)
                fmt.text_writing(f"""
                                         
            #### :chart_with_upwards_trend: Graph of {object}'s altitude as a function of time :chart_with_downwards_trend:
            """)
                plotting_meteo_data(object, df_meteo, lat, lon, height)
                st.session_state.openai_day_1 = True
                st.session_state.openai_json_1_day = df_json
                st.session_state.openai_text_1_day = text
                return
            except Exception as e:
                st.error(f"An error occurred: {e}")
                return
        else:
            text = st.session_state.openai_text_1_day
            df_json = st.session_state.openai_json_1_day
            try:
                fmt.text_writing(text,False,False)
            except:
                st.write(text)
            image = st.session_state.meteo_api_image
            st.image(image, use_container_width=True)
            fmt.text_writing("""
                        <div style='text-align: right; font-size: 0.9em; color: #ffffff;'>
                                Seven days prediction by Meteoblue
                        </div>
                        """, False)
            df_meteo = meteo_df_edition(df_json)
            utcoffset = st.session_state.meteo_utcoffset
            fmt.text_writing(f"""
                                         
            #### :chart_with_upwards_trend: Graph of {object}'s altitude as a function of time :chart_with_downwards_trend:
            """)
            plotting_meteo_data(object, df_meteo, lat, lon, height, utcoffset)
            return

def library():
    """
    Interactive function with objects decription and images or 3D interactive maps (if possible) for
    'Library'.
    """
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
            exploration = st.button("Explore!")
            if exploration:
                if name in objects:
                    for i, obj in enumerate(st.session_state.data):
                        if obj['name'] == name:
                            st.session_state.data[i]['interest'] += 1
                            if st.session_state.data[i]['interest'] >= 2:
                                st.session_state.data[i]['active'] = True
                try:
                    text,image = db.astro_object_description(name)
                    if image != "":
                        fmt.text_writing(text)
                        if name in planets:
                            with st.spinner("Creating 3D map..."):
                                create_3d_planet(name)
                        st.image(image, caption=f"{name} from ESA/Hubble")
                    else:
                        fmt.text_writing(text)
                        if name in planets:
                            with st.spinner("Creating 3D map..."):
                                create_3d_planet(name)
                except Exception as e:
                    st.error(f"Error: {e}")

def astro_recommendation_own_user():
    """
    Function that uses ML to return a list of objects to recommend if user activity is enough.
    Information is collected via st.session_state.
    """
    df = pd.DataFrame(st.session_state.data)
    try:
        num_cols = df.select_dtypes(include=['float', 'float64']).columns.tolist()
        cat_cols = df.select_dtypes(include=['object', 'string']).columns.tolist()
        if 'name' in cat_cols:
            cat_cols.remove('name')
        df_encoded = pd.get_dummies(df[num_cols + cat_cols])
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(df_encoded)
        df['scaled'] = list(X_scaled)
        active = df[df['active']]
        no_active = df[~df['active']]

        if not active.empty and not no_active.empty:
            nn = NearestNeighbors(n_neighbors=1)
            nn.fit(no_active['scaled'].tolist())
            _, indexos = nn.kneighbors(active['scaled'].tolist())
            fmt.text_writing(f"""
                             
            ### Similar Objects
            """)
            for i, (_, fila) in enumerate(active.iterrows()):
                idx_similar = indexos[i][0]
                nom_similar = no_active.iloc[idx_similar]['name']
                fmt.text_writing(f"""

            🔭 You are interested in **{fila['name']}**. Check for **{nom_similar}**! 
            """)
        else:
            st.info("Explore more objects to find similar ones.")
    except Exception as e:
        st.warning(f"No table available yet! {e}")
    return

def astro_recommendation_other_users():
    """
    Function that uses ML to return a list of objects to recommend from a random users activity.
    Information is collected via st.session_state.
    """
    try:
        np.random.seed(st.session_state.seed_num_random)
        df = pd.DataFrame(st.session_state.data)
        active = df[df['active']]
        active_current_user = active['name'].tolist()
        objects_available = df['name'].tolist()
        new_user_interest = {}
        n_users = 50
        for i in range(1, n_users + 1):
            user = f"User_{i}"
            n_objects = np.random.randint(1, min(7, len(objects_available) + 1))
            objectes_seleccionats = np.random.choice(objects_available, n_objects)
            interess = {obj: np.random.randint(1, 11) for obj in objectes_seleccionats}
            new_user_interest[user] = interess
        all_items = set()
        for ratings in new_user_interest.values():
            all_items.update(ratings.keys())
        all_items = sorted(all_items)
        all_users = sorted(new_user_interest.keys())
        item_user_matrix = pd.DataFrame(0, index=all_items, columns=all_users)
        for user, ratings in new_user_interest.items():
            for item, score in ratings.items():
                item_user_matrix.loc[item, user] = score
        model_knn = NearestNeighbors(metric='cosine', algorithm='brute')
        model_knn.fit(item_user_matrix.values)
        recomanations = {}
        for item in active_current_user:
            if item in item_user_matrix.index:
                item_vector = item_user_matrix.loc[item].values.reshape(1, -1)
                distances, indexs = model_knn.kneighbors(item_vector, n_neighbors=3 + 1)
                for dist, idx in zip(distances[0][1:], indexs[0][1:]):
                    similar_item = item_user_matrix.index[idx]
                    recomanations[similar_item] = recomanations.get(similar_item, 0) + 1 - dist
        sorted_recomanations = sorted(recomanations.items(), key=lambda x: -x[1])
        if sorted_recomanations:
            min_item = min(sorted_recomanations, key=lambda x: x[1])
            fmt.text_writing(f"""

            ### What other users observe
                                         
            :eyes: Other users will recommend -> **{min_item[0]}**!
            """)
        else:
            st.info("No recommendations available.")
    except Exception as e:
        st.error(f"Something went wrong with users recommendations! {e}")

##################################### 
# METEO API PRACTICE #
#####################################
def meteo_api(lat,lon,h=0):
    """
    Function to practice Meteoblue API response.
    """
    api_key = st.secrets['meteo']['meteo_api_key']
    params = {
        "apikey": api_key,
        "lat": lat,
        "lon": lon,
        "asl": h,
        "format": "json"
    }
    response = requests.get("https://my.meteoblue.com/packages/basic-1h", params=params)

    if response.status_code == 200:
        data = response.json()
        st.json(data)
        try:
            temps = data["data_1h"]["temperature"][0]
            st.write(f"🌡️ Current temperature: {temps} °C")
        except:
            st.warning("Could not read temperature.")
    else:
        st.error(f"Request error: {response.status_code}")

    params = {
        "apikey": api_key,
        "lat": lat,
        "lon": lon,
        "asl": h,
        "format": "png"
    }

    url = "https://my.meteoblue.com/images/meteogram_one"

    response = requests.get(url, params=params)

    if response.status_code == 200:
        st.image(response.content, caption="Meteogram All-in-One by Meteoblue", use_container_width=True)
    else:
        st.error(f"Error en descarregar la imatge: {response.status_code}")
        st.write(response.text)
    return
#######################################################