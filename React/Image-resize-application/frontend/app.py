import streamlit as st
import requests
import os

st.title("Image Resizer & Twitter Publisher")

uploaded_file = st.file_uploader("Upload an Image", type=["jpg", "png", "jpeg"])
backend_url = "http://127.0.0.1:8000"

if uploaded_file:
    files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
    response = requests.post(f"{backend_url}/upload/", files=files)

    if response.status_code == 200:
        st.success("Image uploaded and resized successfully!")
        resized_urls = response.json().get("urls", [])
        for url in resized_urls:
            st.image(url, caption=os.path.basename(url), use_container_width=True)

if st.button("Post to Twitter"):
    response = requests.post(f"{backend_url}/publish/")
    if response.status_code == 200:
        st.success("Images posted to Twitter!")
    else:
        st.error("Failed to post images.")