# report_calculation

Report about my investments

## pre-commit

```sh
pip install --user pre-commit
pre-commit install
```

## pytho venv

```sh
python3.9 -m venv venv
```

## generate docker containers

```sh
docker-compose up -d --build
```

## forwarding ports

```sh
ssh -L 127.0.0.1:3201:report-calculation:3201 username@ip_address
```
