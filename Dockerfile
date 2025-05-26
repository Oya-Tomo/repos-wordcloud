FROM ubuntu:24.04

WORKDIR /workspace

RUN apt-get update && apt-get install -y \
    python3 python3-pip python3-venv \
    libopenblas-dev git

RUN python3 -m venv /venv

RUN /venv/bin/python3 -m pip install \
    matplotlib numpy \
    gensim==4.3.3 \
    wordcloud

ENV PATH="/venv/bin:$PATH"
ENV VIRTUAL_ENV="/venv"

CMD ["/venv/bin/python3", "main.py"]