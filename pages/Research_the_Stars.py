import src.format as fmt
import streamlit as st
import plotly.graph_objects as go
import numpy as np

fmt.page_format()



phi, theta = np.mgrid[0:np.pi:100j, 0:2*np.pi:100j]
x = np.sin(phi) * np.cos(theta)
y = np.sin(phi) * np.sin(theta)
z = np.cos(phi)

fig = go.Figure(data=[go.Surface(x=x, y=y, z=z, colorscale='Blues')])
fig.update_layout(title='3D Planet', margin=dict(l=0, r=0, b=0, t=30))

st.plotly_chart(fig, use_container_width=True)