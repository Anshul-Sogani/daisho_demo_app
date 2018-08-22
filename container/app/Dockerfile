FROM python:3.6

EXPOSE 5000

COPY . /opt/app
WORKDIR /opt/app


RUN pip install -r requirements.txt

CMD python app.py