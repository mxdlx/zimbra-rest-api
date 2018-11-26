FROM python:2.7.15-stretch
MAINTAINER aaraujo@protonmail.ch

WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . ./

CMD ["python", "./main.py"]
