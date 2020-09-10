FROM python:3-alpine

WORKDIR /usr/src/app

COPY . ./
RUN pip install --no-cache-dir -r requirements.txt

CMD ["gunicorn", "-b 0.0.0.0:8000", "-w 4", "main:app"]
