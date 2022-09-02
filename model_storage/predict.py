from email.mime import image
from PIL import Image
from io import BytesIO
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.applications.imagenet_utils import decode_predictions
import numpy as np


input_shape = (224,224,3)


def load_model():
    model = MobileNetV2(input_shape)
    return model

start_model = load_model()

def read_image(image_encoded):
    pil_image = Image.open(BytesIO(image_encoded))
    return pil_image

def preprocess(Image: Image.Image):
    image = image.resize(input_shape)
    image = np.asfarray(image)
    image = image / 127.5 - 1.0
    image = np.expand_dims(image,0)
    return image



def prediction(image: np.ndarray):
    predictions = start_model.predict(image)
    predictions = decode_predictions(predictions)[0][0][1]
    return predictions
