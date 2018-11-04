FROM python:3

RUN apt-get update
RUN apt-get install -y aria2
COPY aria2.conf /root/.aria2/

WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

CMD aria2c && gunicorn --workers=2 -b 0.0.0.0:8000 --reload index:app
