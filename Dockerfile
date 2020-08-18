FROM python:3.8

COPY requirements.txt /requirements.txt
RUN pip install --upgrade pip && pip install -r /requirements.txt

WORKDIR /app

COPY app.py load.py models.py data.csv /app/

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
