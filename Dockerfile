FROM python:3.10-slim

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    cmake \
    libssl-dev \
    wget \
    unzip \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

ENV LIBOQS_TAG="0.12.0"
ENV LIBOQS_PYTHON_TAG="0.12.0"
ENV LD_LIBRARY_PATH=/usr/local/lib:$LD_LIBRARY_PATH

# liboqs
RUN git clone https://github.com/open-quantum-safe/liboqs && \
    cd liboqs && \
    git checkout "tags/${LIBOQS_TAG}" -b "liboqs-${LIBOQS_TAG}" && \
    cmake -S . -B build -DBUILD_SHARED_LIBS=ON && \
    cmake --build build --parallel $(nproc) && \
    cmake --install build && \
    cd .. && rm -rf liboqs

# Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# liboqs-python wrapper
RUN git clone https://github.com/open-quantum-safe/liboqs-python && \
    cd liboqs-python && \
    git checkout "tags/${LIBOQS_PYTHON_TAG}" -b "liboqs-${LIBOQS_PYTHON_TAG}" && \
    pip install --no-cache-dir . && \
    cd .. && rm -rf liboqs-python

COPY . .

CMD ["python3", "main.py"]
