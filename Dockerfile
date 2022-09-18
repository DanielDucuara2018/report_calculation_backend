FROM python:3.9

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir --upgrade pip
RUN --mount=type=cache,target=/root/.cache pip install --editable .

ENTRYPOINT python /app/report_calculation/main.py