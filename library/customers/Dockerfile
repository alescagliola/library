FROM python:3.6-slim-buster

WORKDIR /app

COPY customers/requirements.txt ./

RUN pip install -r requirements.txt

COPY customers/ . 

EXPOSE 4000

CMD [ "flask", "run", "--host=0.0.0.0", "--port=4000"]
ENV FLASK_APP=customersapp.py