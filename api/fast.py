from fastapi import FastAPI, File, UploadFile
from starlette.responses import Response
# from model_storage.predict import read_image, prediction
import numpy as np
import cv2
import io




from fastapi import FastAPI, File, UploadFile

app = FastAPI()

@app.get("/")
def index():
    return {"status": "ok"}

@app.post('/upload_image')
async def receive_image(img: UploadFile=File(...)):
    ### Receiving image
    contents = await img.read()

    nparr = np.fromstring(contents, np.uint8)
    cv2_img = cv2.imdecode(nparr, cv2.IMREAD_COLOR) # type(cv2_img) => numpy.ndarray

    ### Do cool stuff with your image.... For example face detection
    #annotated_img = annotate_face(cv2_img)

    ### Encoding and responding with the image
    im = cv2.imencode('.png', cv2_img)[1] # extension depends on which format is sent from Streamlit
    return Response(content=im.tobytes(), media_type="image/png")









# from fastapi import FastAPI, File, UploadFile
# from starlette.responses import Response
# from pydantic import BaseModel
# from model import asd
# import numpy as np
# import pickle
# import cv2
# import io

# app = FastAPI()

# #class params(BaseModel):
# #    pass
# #    img : 

# @app.get("/")
# def index():
#     return {"status": "ok"}


# #with open("/model.pkl", "rb") as f:
# #
# #   model = pickle.load(f)


# @app.post('/prediction')
# async def predict_image(img: UploadFile=File(...)):
#     ### Receiving image
#     contents = await img.read()
#     nparr = np.fromstring(contents, np.uint8)
#     cv2_img = cv2.imdecode(nparr, cv2.IMREAD_COLOR) 

#     #pred_img = model.predict([img]).tolist()[0]
#     pred_img = asd(cv2_img)

#     img = cv2.imencode('.png', pred_img)[1] 
#     return Response(content=img.tobytes(), media_type="image/png")














