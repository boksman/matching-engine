FROM python:3.7.4

WORKDIR /app
CMD ["python"]

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python"]
