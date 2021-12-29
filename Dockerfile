FROM python:3

WORKDIR /usr/src/app
RUN pip install flask mysql-connector-python

COPY . .

CMD ["waitress-serve", "--port", "5000", "main:app"]