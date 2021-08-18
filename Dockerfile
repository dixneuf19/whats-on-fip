FROM python:3.9-buster

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY whatsonfip whatsonfip

EXPOSE 80

CMD ["uvicorn", "whatsonfip.main:app" , "--host", "0.0.0.0", "--port", "80"]
