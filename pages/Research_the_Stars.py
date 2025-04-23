import streamlit as st
import numpy as np
import src.format as fmt
from PIL import Image
import plotly.graph_objects as go


import matplotlib.pyplot as plt
from PIL import Image
fmt.page_format()
def show_texture_preview(image_path):
    texture = Image.open(image_path).convert("L")  # Escala de grisos
    texture_array = np.asarray(texture)
    st.image(texture_array, caption="Previsualització de la textura", use_container_width=True)
    return texture_array

def create_3d_planet(texture):
    h, w = texture.shape

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
        colorscale="YlOrRd",  # Pots provar també 'Viridis', 'Earth', etc.
        cmin=0,
        cmax=255,
        showscale=False
    )])

    fig.update_layout(
        title="🌍 Planeta 3D amb textura (escalat de grisos)",
        scene=dict(
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            zaxis=dict(visible=False),
            aspectmode='data'
        ),
        margin=dict(l=0, r=0, t=30, b=0)
    )

    st.plotly_chart(fig, use_container_width=True)

# Ruta de la textura
texture_path = "images/marsmap1k.jpg"
texture = show_texture_preview(texture_path)
create_3d_planet(texture)




# def mars_3d_plot(texture_path):
#     # Carrega la textura
#     img = Image.open(texture_path).resize((360, 180))
#     texture = np.asarray(img)

#     # Coordenades esfera
#     phi = np.linspace(0, np.pi, 180)
#     theta = np.linspace(0, 2 * np.pi, 360)
#     phi, theta = np.meshgrid(phi, theta)

#     x = np.sin(phi) * np.cos(theta)
#     y = np.sin(phi) * np.sin(theta)
#     z = np.cos(phi)

#     # Normalitzar textura per aplicar com a color
#     texture_colors = texture / 255.0
#     surfacecolor = np.flipud(texture_colors[:, :, 0])  # només un canal, per colormap
#     # grayscale = np.mean(texture_colors, axis=2)
#     # surfacecolor = np.flipud(grayscale)
#     # texture_colors
#     # plt.imshow(texture_colors)
#     # plt.title("Visualització de la textura")
#     # plt.axis("off")
#     # fig = plt.show()

#     # Figura plotly
#     fig = go.Figure(data=[go.Surface(
#         x=x, y=y, z=z,
#         surfacecolor=surfacecolor,
#         # colorscale='YlOrBr',
#         colorscale=[[0, 'brown'], [1, 'orange']],
#         cmin=0,
#         cmax=1,
#         showscale=False,
#         lighting=dict(ambient=0.5, diffuse=0.9)
#     )])

#     fig.update_layout(
#         title="Mars 3D (interactive)",
#         scene=dict(
#             xaxis=dict(visible=False),
#             yaxis=dict(visible=False),
#             zaxis=dict(visible=False),
#             aspectmode='data'
#         ),
#         margin=dict(l=0, r=0, t=30, b=0)
#     )
#     return fig

# # Streamlit interface
# st.title("🔴 Mars 3D Visualization (Interactive)")
# st.write("Use your mouse or touch to rotate the planet!")

# # texture_path = "images/marsmap1k.jpg"
# texture_path = "images\mars_1k_color.jpg"
# fig = mars_3d_plot(texture_path)

# st.plotly_chart(fig, use_container_width=True)

# st.image('images/marsmap1k.jpg')