# Generate WiFi QR Cards
This package generates a PDF document with WiFi login cards, including
a QR Code to automate login

Run this repo in a VSCode devcontainer to execute `generate_wifi_qr_card.py`.
Alternatively, can execute the following docker command

```sh
docker container run --rm -v ${PWD}:/app -it python:3.12-bookworm \
    bash -c "apt update && \
    apt install -y texlive-latex-recommended \texlive-pictures && \
    pip install -q -U pip segno pillow pylatex && cd /app && /bin/bash"
```