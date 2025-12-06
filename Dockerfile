FROM python:3.11.13-bookworm

WORKDIR /prod

RUN pip install --upgrade pip setuptools wheel

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY x_rays x_rays

CMD uvicorn x_rays.api.fast:app --host 0.0.0.0 --port $PORT