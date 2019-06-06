FROM python:3.6

EXPOSE 8080
EXPOSE 3306

WORKDIR /app

COPY requirements.txt /app
COPY app.py /app
COPY storeDB.py /app
COPY fetchDB.py /app

RUN pip3 install -r requirements.txt

CMD python3 app.py
