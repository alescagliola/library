FROM python:3.6-slim-buster

WORKDIR /app

COPY books/requirements.txt ./

RUN pip install -r requirements.txt

COPY books/ . 

EXPOSE 5000

CMD [ "flask", "run", "--host=0.0.0.0", "--port=5000"]
ENV FLASK_APP=booksapp.py