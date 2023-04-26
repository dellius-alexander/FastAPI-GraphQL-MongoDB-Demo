FROM python:3.9-rc
WORKDIR /app
COPY requirements.txt /tmp
RUN apt-get update -y && \
    apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev
RUN python3 -m pip install -r /tmp/requirements.txt --upgrade pip
ENTRYPOINT ["python", "-m", "uvicorn"]
CMD ["main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
