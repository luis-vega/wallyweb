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











### de aqui para abajo es la ayuda con edmondo

# @app.get("/files/")
# async def create_file(file: bytes = File(description="A file read as bytes")):
#     return {"file_size": len(file)}


# @app.get("/uploadfile/")
# async def create_upload_file(
#     file: UploadFile = File(description="A file read as UploadFile"),
# ):
#     return {"filename": file.filename}
## hasta aqui
#############



#####
### Esto es lo del hindu
#####
# @app.get('/')
# def root_endpoint():
#     return {'working': True}

# @app.post('/predict')
# def predict(img_file:UploadFile = File(...)):
#     input_image = Image.open(img_file.file)
#     return {'image': img_file}
#     # model.run_from_filepath


# @app.post("/files/")
# async def create_file(file: bytes = File()):
#     return {"file_size": len(file)}


# @app.post("/uploadfile/")
# async def create_upload_file(file: UploadFile):
#     return {"filename": file.filename}
# @app.post("/files/")
# async def create_file(file: bytes = File()):
#     return {"file_size": len(file)}


# @app.post("/uploadfile/")
# async def create_upload_file(file: UploadFile):
#     return {"filename": file.filename}

####
# Hasta aca
####








# def load_model():
#     return f'some model'

# @app.get('/predict')
# def predict():

#     model = load_model()
#     y_pred = model + 'and something else'

#     return {'prediction':y_pred}


#####
## de aqui para abajo estoy replazando la anterior funcion para hacerla encajar con el modelo
#####


# @app.get('/predict')
# def predict():
#     model = load_model()
#     y_pred = model.predict(X_s)

#     return {'This is where waldo is':y_pred[0]}


#######
###  try #2
#######


# import os

# from fastapi import FastAPI
# from fastapi.responses import FileResponse

# app = FastAPI()

# path = "/path/to/files"

# @app.get("/wally_image", responses={200: {"wally_image": "A whole picture of wally.",
#                                           "content" : {"image/jpeg" :
#                                               {"example" : "No example available. Just imagine a picture of a vector image."}}}})
# def image_endpoint():
#     file_path = os.path.join(path, "files/vector_image.jpg")
#     if os.path.exists(file_path):
#         return FileResponse(file_path, media_type="image/jpeg", filename="vector_image_for_you.jpg")
#     return {"error" : "File not found!"}


# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: Union[str, None] = None):
#     return {"item_id": item_id, "q": q}
