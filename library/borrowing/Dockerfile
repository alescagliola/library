FROM python:3.6-slim-buster

WORKDIR /app

COPY borrowing/requirements.txt ./

RUN pip install -r requirements.txt

COPY borrowing/ . 

EXPOSE 5001

CMD [ "flask", "run", "--host=0.0.0.0", "--port=5001"]
ENV FLASK_APP=borrowingapp.py