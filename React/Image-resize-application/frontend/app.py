import streamlit as st
import requests
import os

st.title("Image Resizer & Twitter Publisher")

backend_url = "http://127.0.0.1:8000"

uploaded_file = st.file_uploader("Upload an Image", type=["jpg", "png", "jpeg"])

if uploaded_file:
    files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
    
    try:
        response = requests.post(f"{backend_url}/upload/", files=files)
        response.raise_for_status()

        if response.status_code == 200:
            st.success("Image uploaded and resized successfully!")
            resized_urls = response.json().get("urls", [])
            for url in resized_urls:
                st.image(url, caption=os.path.basename(url), use_container_width=True)
        else:
            st.error("Image upload failed.")
    
    except requests.exceptions.RequestException as e:
        st.error(f"Connection error: {e}")

if st.button("Post to Twitter"):
    try:
        response = requests.post(f"{backend_url}/publish/")
        response.raise_for_status()

        if response.status_code == 200:
            st.success("Images posted to Twitter!")
        else:
            st.error("Failed to post images.")
    
    except requests.exceptions.RequestException as e:
        st.error(f"Connection error: {e}")
