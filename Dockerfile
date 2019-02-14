FROM python:3-slim

WORKDIR /app

ENV FLASK_APP "myapp"
ENV FLASK_RUN_PORT "5000"
ENV MONGO_URL "mongodb://mongo:27017/mydb"

EXPOSE ${FLASK_RUN_PORT}

COPY ./requirements.txt /app/
RUN pip install -r requirements.txt

COPY ./myapp /app/myapp

ENTRYPOINT ["flask"]

CMD ["run", "--host=0.0.0.0"]
