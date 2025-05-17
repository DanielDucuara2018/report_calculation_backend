# 📊 Report Calculation Backend

The **Report Calculation Backend** is a Python-based service designed to automate the generation of investment reports. It processes financial data, performs calculations, and delivers structured outputs to support investment analysis and decision-making.

---

## 🚀 Features

* **Automated Report Generation**: Processes financial data to generate comprehensive investment reports.
* **Dockerized Deployment**: Utilizes Docker and Docker Compose for consistent and scalable deployments.
* **Pre-commit Hooks**: Ensures code quality and consistency through automated checks before commits.
* **Configurable Settings**: Offers customizable configurations via `report_calculation.ini` and `supervisord.conf`.([GitHub][1])

---

## 🛠️ Getting Started

### Prerequisites

* Python 3.9
* Docker
* Docker Compose

### Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/DanielDucuara2018/report_calculation_backend.git
   cd report_calculation_backend
   ```
   
2. **Set Up Python Virtual Environment**

   ```bash
   python3.9 -m venv venv
   source venv/bin/activate
   ```
   
3. **Install Pre-commit Hooks**

   ```bash
   pip install --user pre-commit
   pre-commit install
   pre-commit run --all-files
   ```

4. **Build and Run Docker Containers**

   ```bash
   docker-compose up -d --build
   ```

5. **Configure Hostname and Port Forwarding**

   * **Add Hostname**

     ```bash
     sudo nano /etc/hosts
     # Add the following line:
     169.254.6.2 report-calculation
     ```

   * **Set Up Port Forwarding**

     ```bash
     ssh -L 127.0.0.1:3201:report-calculation:3201 username@ip_address
     ```

---

## 📁 Project Structure

```plaintext
├── alembic/                   # Database migrations
├── pgsql/init.d/              # PostgreSQL initialization scripts
├── report_calculation/        # Core application logic
├── .pre-commit-config.yaml    # Pre-commit hook configurations
├── Dockerfile                 # Docker image definition
├── docker-compose.yml         # Docker Compose configuration
├── pyproject.toml             # Project metadata and dependencies
├── report_calculation.ini     # Application configuration
├── setup.cfg                  # Setup configurations
├── setup.py                   # Installation script
└── supervisord.conf           # Process control configuration
```

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

[1]: https://github.com/DanielDucuara2018/report_calculation_backend?utm_source=chatgpt.com "DanielDucuara2018/report_calculation_backend - GitHub"
[2]: https://github.com/DanielDucuara2018/report_calculation_backend/security?utm_source=chatgpt.com "DanielDucuara2018/report_calculation_backend - GitHub"
