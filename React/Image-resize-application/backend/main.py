from fastapi import FastAPI, UploadFile, File
from fastapi.staticfiles import StaticFiles 
from PIL import Image
from io import BytesIO
import os
import tweepy
from config import API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_SECRET

app = FastAPI()
UPLOAD_DIR = "uploads"
RESIZED_DIR = "resized"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(RESIZED_DIR, exist_ok=True)
SIZES = [(300, 250), (728, 90), (160, 600), (300, 600)]

auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
twitter_api = tweepy.API(auth)

def resize_image(image, size, filename):
    resized_image = image.resize(size)
    file_path = os.path.join(RESIZED_DIR, filename)
    resized_image.save(file_path, format="JPEG")
    return file_path

@app.post("/upload/")
async def upload_image(file: UploadFile = File(...)):
    image_bytes = await file.read()
    image = Image.open(BytesIO(image_bytes)).convert("RGB")
    
    resized_paths = []
    for i, size in enumerate(SIZES):
        resized_path = resize_image(image, size, f"resized_{i}.jpg")
        resized_paths.append(f"http://localhost:8000/resized/resized_{i}.jpg")
    
    return {"message": "Images resized", "urls": resized_paths}

@app.post("/publish/")
async def publish_images():
    images = [os.path.join(RESIZED_DIR, f"resized_{i}.jpg") for i in range(4)]
    media_ids = [twitter_api.media_upload(img).media_id for img in images]
    twitter_api.update_status(status="Here are the resized images!", media_ids=media_ids)
    return {"message": "Images posted to Twitter"}

app.mount("/resized", StaticFiles(directory="resized"), name="resized")
