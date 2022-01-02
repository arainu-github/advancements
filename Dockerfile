FROM python:3

WORKDIR /usr/src/app
RUN pip install flask mysql-connector-python waitress flask_cors

COPY . .

CMD ["waitress-serve", "--port", "5000", "main:app"]
