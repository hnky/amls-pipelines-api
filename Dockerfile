FROM python:3.6
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
RUN chmod 644 app.py
ENTRYPOINT ["python"]
CMD ["app.py"]
