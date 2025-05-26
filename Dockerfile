FROM ubuntu:24.04

WORKDIR /workspace

RUN apt-get update && apt-get install -y \
    python3.12 python3.12-pip python3.12-venv \
    build-essential gcc g++ cmake gfortran pkg-config \
    libopenblas-dev liblapack-dev \
    software-properties-common \
    libbz2-dev libdb-dev \
    libreadline-dev libffi-dev libgdbm-dev liblzma-dev \
    libncursesw5-dev libsqlite3-dev libssl-dev \
    zlib1g-dev uuid-dev

RUN python3 -m venv /venv

RUN /venv/bin/python3 -m pip install \
    matplotlib numpy \
    gensim==4.3.3 \
    wordcloud

ENV PATH="/venv/bin:$PATH"
ENV VIRTUAL_ENV="/venv"

CMD ["/venv/bin/python3", "main.py"]