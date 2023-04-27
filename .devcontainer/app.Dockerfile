FROM python:3.9
WORKDIR /app

# Install dependencies
RUN apt-get update -y && \
    apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    git build-essential libsndfile1-dev \
    tesseract-ocr espeak-ng python3 \
    python3-pip ffmpeg git-lfs cmake

# Copy requirements.txt to the image
COPY requirements.txt* /tmp/requirements.txt

# Install virtual environment
RUN python3 -m venv /app/venv
RUN cd /app && \
    . /app/venv/bin/activate

# Update pip and Install dependencies
RUN python3 -m pip install --upgrade pip && \
    python3 -m pip install -r /tmp/requirements.txt

# Tell system to use this venv as default
ENV PATH="/app/venv/bin:$PATH"
ENV RUN_PORT=8000

# Start the app
ENTRYPOINT ["python3", "-m", "uvicorn"]
CMD ["main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
