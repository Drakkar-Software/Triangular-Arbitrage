FROM python:3.10-slim-buster AS base

WORKDIR /app

# requires git to install requirements with git+https
RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential git gcc binutils

COPY . .

RUN pip3 install --no-cache-dir -U setuptools wheel pip \
    && pip3 install --no-cache-dir -r requirements.txt -r dev_requirements.txt \
    && python3 setup.py install

ENTRYPOINT ["python3", "server.py"]
