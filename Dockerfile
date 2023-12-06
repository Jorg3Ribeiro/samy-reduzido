FROM python:3.9

WORKDIR /app

COPY requirements.txt .
COPY . .

EXPOSE 8888

RUN pip install -r requirements.txt

CMD ["python", "app.py"]
