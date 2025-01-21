FROM python:3.8

WORKDIR /app

COPY . /app

COPY .env /app/.env

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

RUN chmod +x init.sh

CMD ["./init.sh"]
