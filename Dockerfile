FROM python:3.10.0-alpine
WORKDIR /home

COPY . .
RUN pip install -r requirements.txt
ENTRYPOINT ["python", "main.py"]