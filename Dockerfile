# FROM tensorflow/tensorflow
FROM python:3.8.6-buster
# COPY * /wallyweb
COPY api/fast.py fast.py
COPY model_storage /model_storage
COPY requirements.txt /requirements.txt
COPY setup.py /setup.py

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install .

# CMD uvicorn api.fast:app --host 0.0.0.0 --port $PORT
CMD uvicorn fast:app --host 0.0.0.0 --port $PORT
#CMD streamlit run app.py --host 0.0.0.0 --port $PORT
