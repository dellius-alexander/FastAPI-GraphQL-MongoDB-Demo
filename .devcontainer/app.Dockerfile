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

# Update pip and Install dependencies
RUN python3 -m pip install --no-cache-dir --upgrade -r /tmp/requirements.txt pip

# Tell system to use this venv as default
RUN mkdir -p /entrypoint

COPY .devcontainer/entrypoint/entrypoint.sh* /entrypoint/entrypoint.sh
# Start the app
#ENTRYPOINT ["python3", "-m", "uvicorn", "main:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "8000", "--reload"]
ENTRYPOINT ["/bin/bash", "/entrypoint/entrypoint.sh"]