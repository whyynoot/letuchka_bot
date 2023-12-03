FROM python:3.9
WORKDIR /usr/app

COPY . .
RUN pip3 install --upgrade pip
# RUN pip3 install -r requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt
CMD python3 main.py
