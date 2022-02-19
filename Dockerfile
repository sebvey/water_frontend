FROM python:3.8.12-buster

COPY requirements.txt requirements.txt
COPY water_frontend water_frontend
COPY data data
COPY .streamlit .streamlit
COPY .env .env
COPY app.py app.py

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE $PORT

CMD streamlit run app.py --server.port $PORT

