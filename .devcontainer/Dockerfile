FROM python:3.12-bookworm

RUN apt update && \
    apt install -y git-lfs gnupg2 less vim texlive-latex-recommended texlive-pictures && \
    pip install -q -U pip segno pillow pylatex && \
    useradd --shell /bin/bash --create-home wifi-qr && \
    echo "\nexport PATH=/home/wifi-qr/.local/bin:\${PATH}" .. /home/wifi-qr/.bashrc

USER wifi-qr
