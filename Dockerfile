FROM python:3.12.6

WORKDIR /app

COPY ./Pipfile /app/Pipfile
COPY ./Pipfile.lock /app/Pipfile.lock

RUN pip install pipenv
RUN cd /app
RUN pipenv install

COPY ./ ./