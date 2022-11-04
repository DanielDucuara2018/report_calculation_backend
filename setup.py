from setuptools import find_packages, setup

VERSION = "0.1"

INSTALL_REQUIRES = [
    "python-binance==1.0.16",
    "apischema==0.15.6",
    "python-telegram-bot==20.0a2",
    "SQLAlchemy==1.4.37",
    "psycopg2==2.9.1",
    "configparser==5.3.0",
]

setup(
    name="report-calculation",
    version=VERSION,
    python_requires=">=3.9.0",
    packages=find_packages(exclude=["tests"]),
    # url="http://www.report_calulation.com",
    author="Daniel Ducuara",
    author_email="daniel14015@gmail.com",
    description="Get a report of my porfolio",
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "report-calculation = report_calulation.main:main",
            # "console = report_calulation.main:console",
        ]
    },
    install_requires=INSTALL_REQUIRES,
    extras_require={
        "test": [
            "pytest==6.2.4",
            "pytest-mock==3.6.1",
            "pytest-cov==2.12.1",
            "pytest-asyncio==0.15.1",
        ]
    },
)
