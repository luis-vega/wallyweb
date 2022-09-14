from fastapi import FastAPI, File, UploadFile
from json import dumps
from numpy import fromstring, uint8
import cv2
import io

# import matplotlib.pyplot as plt
from PIL import Image

from fastapi import FastAPI, File, UploadFile
from keras.models import Sequential
from keras.layers import Dropout, Lambda,Conv2D, MaxPooling2D

app = FastAPI()

def get_conv(input_shape=(64, 64, 3), filename=None):
    model = Sequential()
    model.add(Lambda(lambda x: x / 127.5 - 1., input_shape=input_shape, output_shape=input_shape))
    model.add(Conv2D(32, (3, 3), activation='relu', name='conv1', input_shape=input_shape, padding="same"))
    model.add(Conv2D(64, (3, 3), activation='relu', name='conv2', padding="same"))
    model.add(MaxPooling2D(pool_size=(3, 3)))
    model.add(Dropout(0.25))
    model.add(Conv2D(128, (8, 8), activation="relu", name="dense1"))
    model.add(Dropout(0.5))
    model.add(Conv2D(1, (14, 14), name="dense2", activation="sigmoid"))

    if filename:
        model.load_weights(filename)
    return model

heatmodel = get_conv(input_shape=(None, None, 3), filename="model_storage/localize7.h5")
def locate(img):
    data = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    heatmap = heatmodel.predict(data.reshape(1, data.shape[0], data.shape[1], data.shape[2]))
    return heatmap

@app.get("/")
def index():
    return {"status": "ok"}

@app.post('/upload_image')
async def receive_image(img: UploadFile=File(...)):
    contents = await img.read()
    nparr = fromstring(contents, uint8)
    cv2_img = cv2.imdecode(nparr, cv2.IMREAD_COLOR) # type(cv2_img) => numpy.ndarray
    heatmap = locate(cv2_img)
    return dumps(heatmap.tolist())
