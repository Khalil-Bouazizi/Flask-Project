FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade setuptools==70.0.0

RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
