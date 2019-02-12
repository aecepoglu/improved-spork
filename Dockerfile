FROM python:3-slim

WORKDIR /app

ENV FLASK_APP "hello"
ENV FLASK_RUN_PORT "5000"

EXPOSE ${FLASK_RUN_PORT}

COPY ./requirements.txt /app/
RUN pip install -r requirements.txt

COPY ./hello.py /app/
COPY ./db.py /app/

CMD ["flask", "run", "--host=0.0.0.0"]
