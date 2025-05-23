# 🌌 Astrazeus: Interactive Astronomy with Streamlit

An interactive application developed as part of the Master's Thesis in Data Science & Artificial Intelligence. This tool allows users to explore the visibility of astronomical objects based on their location, time, and weather conditions.

## 🚀 Features

- 🌍 Customizable location: Users can input latitude, longitude, and altitude to determine what celestial objects are visible from their position.

- 🕒 Hourly visibility calculation: Divide the day into time intervals to evaluate the visibility of an astronomical object hour by hour.

- ☁️ Real weather integration: Includes parameters such as cloud cover and sunlight to refine predictions.

- 💐 Celestial plots: Polar plots showing altitude and azimuth of celestial objects throughout the day.

## 🧑‍💻 Technologies Used

- `Python 3.10+`

- `Streamlit` for the interactive web interface

- `Astropy` for astronomical calculations

- `Matplotlib` for sky visualizations

- `pandas`, `numpy` for data processing

- `requests` for accessing external weather and visibility APIs

## 🧠 Motivation

This project aims to make amateur astronomy more accessible by combining astronomical and meteorological data to help users plan their stargazing sessions more effectively.

## 📦 Installation

1. Clone this repository:

<pre>git clone https://github.com/Miquel456/astrazeus.git
cd astrazeus </pre>

2. Install the required packages:

<pre>pip install -r requirements.txt </pre>

3. Run the app:

<pre>streamlit run Home.py </pre>

## 📷 Screenshots

Ex: 
- Weather
  
![Vega_Weather](images/example/vega_example_results_1.webp)

- Visual forecast
  
![Vega_Visibility](images/example/vega_example_results_2.webp)

- Sky Chart Position
  
![Vega Position](images/example/vega_example_results_3.webp)

## 📌 Project Status

✅ Functional🛠️ Possible improvements: multilingual support, push notifications, 3D planet visualization, favorites 

## 👨‍🏫 Author

Project developed by Miquel Pujol Reina as part of the Master in Data Science & Artificial Intelligence (2025).