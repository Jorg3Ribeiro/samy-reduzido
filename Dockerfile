FROM python:3.9

WORKDIR /app

COPY requirements.txt .
COPY . .

EXPOSE 8888

RUN pip install --upgrade pip
RUN pip install --upgrade lxml_html_clean
RUN pip install -r requirements.txt

CMD ["python", "app.py"]
