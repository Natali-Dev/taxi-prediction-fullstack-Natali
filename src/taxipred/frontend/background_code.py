import streamlit as st
import base64
from taxipred.utils.constants import ASSET_PATH

def add_background():
    # Funktion som omvandlar en bild till base64 så vi kan bädda in den i CSS
    def get_base64_of_bin_file(bin_file):
        with open(bin_file, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()

    img_path = ASSET_PATH / "funny_taxi.png"   # relativ sökväg till bilden
    img_base64 = get_base64_of_bin_file(img_path)

    # CSS för att lägga bilden som bakgrund och göra den lite "immig"
    page_bg = f"""
    <style>
    .stApp {{
      background-image: url("data:image/png;base64,{img_base64}");
      background-size: cover;
      background-position: center;
    }}
    .stApp::before {{
      content: "";
      position: absolute;
      top: 0;
      bottom: 0;
      right: 25%;
      left: 25%;
      background: rgba(0,0,0,0.9);  /* ändra alpha för mer/mindre dimma */
      
      z-index: 0;
    }}
    </style>
    """

    return st.markdown(page_bg, unsafe_allow_html=True)

