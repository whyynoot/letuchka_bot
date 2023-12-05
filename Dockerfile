FROM python:3.9-slim-buster
WORKDIR /usr/app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
# RUN pip3 install --upgrade pip
# RUN pip3 install -r requirements.txt
CMD python3 main.py
