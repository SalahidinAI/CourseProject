FROM python:3.12

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt /app/ # меняем на req.txt если надо
RUN pip install gunicorn # от aws lesson 2 not our (это нужно если раньше не скачал gunicorn)
RUN pip install setuptools # от aws lesson 2 not our (желательно)
RUN pip install --upgrade pip && \
    pip install -r requirements.txt # меняем на req.txt если надо

COPY nginx/nginx.conf /etc/nginx/conf.d/

COPY . /app/
