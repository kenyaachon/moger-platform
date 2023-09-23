FROM python:3.11.5-bullseye

USER root

RUN apt install curl
RUN curl -sL https://deb.nodesource.com/setup_18.x | bash
RUN apt update
RUN apt upgrade
RUN apt install nodejs
RUN npm install -g serverless
RUN curl -sSL https://install.python-poetry.org | POETRY_VERSION=1.6.1 python3 -


ENV PATH "/root/.local/bin:$PATH"

