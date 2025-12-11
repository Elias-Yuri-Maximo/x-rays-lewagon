import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import utils
import requests
import os

# with open("images/hero-image.png", "rb") as f:
#     data = base64.b64encode(f.read()).decode()

def print_tree(path, prefix=""):
    items = sorted(os.listdir(path))
    for index, item in enumerate(items):
        full_path = os.path.join(path, item)
        connector = "└── " if index == len(items) - 1 else "├── "
        st.write(prefix + connector + item)
        if os.path.isdir(full_path):
            new_prefix = prefix + ("    " if index == len(items) - 1 else "│   ")
            print_tree(full_path, new_prefix)

st.write("Root folder:", os.getcwd())
print_tree(os.getcwd())

def request_prediction(uri, uploaded_file):

    # The file you want to send
    # file_path = r"C:\Users\elias\Desktop\CODE_PROJS\LeWagon\X-RAYS\x-rays-lewagon\x_rays\streamlit_frontend\test_image.png"
    files = {
        "received_image": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)
    }

    response = requests.post(uri, files=files)

    # print("Status code:", response.status_code)
    # print("Response:", response.text)

    return response
    
st.markdown(
    """
    <style>
        /* APP BACKGROUND */
        .stApp {
            background-color: #0A1A33; /* deep medical navy blue */
        }



        /* BUTTONS */
        .stButton>button {
            background-color: #1E3A66;   /* steel blue */
            color: white;
            border-radius: 8px;
            padding: 0.6rem 1.2rem;
            border: 1px solid #284B8A;
            font-family: 'Georgia', serif;
        }
        .stButton>button:hover {
            background-color: #284B8A;
        }


    </style>

    """,
    unsafe_allow_html=True
)



st.image( "home/elias-yuri-maximo/x_rays/streamlit_frontend/images/hero-image.png")


# --- Header ---
st.title("X-RAY COVID Detector")
st.write("Please upload the image of the X-Ray you want to classify")


uploaded_file = st.file_uploader("Upload an X-Ray image to evaluate with a Convolutional Neural Network", type=["png", "jpg", "jpeg"])
if uploaded_file: 
    # print("uploaded_file_cnn")



    response = request_prediction("https://xrays-555583252134.europe-west1.run.app/do_you_have_covid",
                                  uploaded_file)
    
    if response.status_code == 200:
        if response.json()["result"] < 0.35:
            
            st.success(f"You are healthy! According to our AI model.")
        else: 
            st.error(f"""You are likely sick! 
                     We strongly advise you to have a doctor's appointment soon.""")
            st.markdown("""
            <ul>
                <li>Rest and avoid heavy activity.</li>
                <li>Drink plenty of fluids and eat lightly.</li>
                <li>Take fever or pain medicine if needed.</li>
                <li>Isolate from others, keep your room ventilated, and wear a mask if you must be around people.</li>
                <li>Monitor your symptoms, especially breathing and fever.</li>
                <li>Seek medical care if your symptoms worsen or you have trouble breathing.</li>
                <li>Contact a doctor early if you’re in a higher-risk group.</li>
            </ul>
            """, unsafe_allow_html=True)

    else:
        st.error(f"Error {response.status_code}")
        st.write(response.text)

    st.image(uploaded_file, caption="My Image", use_container_width=True)

# uploaded_file_dense_net = st.file_uploader("Upload an X-Ray image to evaluate with a Dense Net Model", type=["png", "jpg", "jpeg"])
# if uploaded_file_dense_net: 
#     print("uploaded_file_dense_net")

# uploaded_pca = st.file_uploader("Upload an X-Ray image to evaluate with a PCA model", type=["png", "jpg", "jpeg"])
# if uploaded_pca: 
#     print("uploaded_pca")
