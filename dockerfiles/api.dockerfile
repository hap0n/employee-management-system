FROM python:3.8.10 AS app

COPY requirements.txt app/
RUN pip install -r app/requirements.txt
COPY . app/
WORKDIR app
RUN pip install -e .
EXPOSE 8080

FROM app AS app-dev
RUN pip install -r requirements.dev.txt
ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.5.1/wait /docker-compose-wait
RUN chmod +x /docker-compose-wait
