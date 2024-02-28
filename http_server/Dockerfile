FROM python:3.9-slim

WORKDIR /home/neo/Desktop/Project/http_server

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY http-server.py .

EXPOSE 5000

CMD ["python", "http-server.py"]
