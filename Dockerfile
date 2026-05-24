FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    IMAGEEZ_CONFIG=pyproject.toml \
    IMAGEEZ_HOST=0.0.0.0 \
    IMAGEEZ_PORT=7865

WORKDIR /app

COPY pyproject.toml README.md app.py requirements.txt runtime.txt ./
COPY src ./src
COPY assets ./assets

RUN python -m pip install --upgrade pip \
    && python -m pip install -e ".[app,mesh]"

EXPOSE 7865

CMD ["python", "app.py"]
