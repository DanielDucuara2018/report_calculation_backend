# report_calculation

Report about my investments

## pre-commit

```bash
pip install --user pre-commit
pre-commit install
pre-commit run --all-files
```

## pytho venv

```bash
python3.9 -m venv venv
```

## generate docker containers

```bash
docker-compose up -d --build
```

## forwarding ports

Create a host name for report-calculation application:

```bash
sudo nano /etc/hosts
169.254.6.2 report-calculation
```

Forward port in host machine:

```bash
ssh -L 127.0.0.1:3201:report-calculation:3201 username@ip_address
```
