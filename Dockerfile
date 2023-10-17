FROM python:3.11-slim

WORKDIR /usr/src/ygt

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .
RUN tailwindcss -i ./static/src/main.css -o ./static/dist/main.css --minify

CMD ["python", "app.py"]