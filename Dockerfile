FROM python:3.5

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

ENTRYPOINT [ "python", "magictune.py" ]

CMD [ "--help" ]