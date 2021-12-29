FROM python:3

WORKDIR /usr/src/app
RUN pip install flask mysql-connector-python

COPY . .

CMD ["python","./main.py"]