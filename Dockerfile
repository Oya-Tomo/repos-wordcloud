FROM ubuntu:25.10

WORKDIR /workspace

RUN apt-get update && apt-get install -y \
    python3 python3-pip python3-venv \
    build-essential gcc g++ cmake gfortran pkg-config \
    libopenblas-dev liblapack-dev

RUN python3 -m venv /venv

RUN /venv/bin/python3 -m pip install \
    matplotlib numpy \
    gensim wordcloud

ENV PATH="/venv/bin:$PATH"
ENV VIRTUAL_ENV="/venv"

CMD ["/venv/bin/python3", "main.py"]