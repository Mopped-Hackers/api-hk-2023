FROM python:3.8

WORKDIR /app
RUN /usr/local/bin/python -m pip install --upgrade pip
COPY .env .env
COPY requirements.txt requirements.txt
RUN pip3 install pip
RUN pip3 install -r requirements.txt
RUN pip3 install sqlalchemy
RUN pip3 install psycopg2-binary

COPY . .
CMD ["uvicorn", "manage:app", "--host", "0.0.0.0", "--port", "8000"]