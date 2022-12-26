import configparser
import os
from dataclasses import dataclass

from apischema import deserialize
from sqlalchemy.engine import create_engine
from sqlalchemy.orm import Session, sessionmaker

from report_calculation.model.base import mapper_registry

root_folder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

import logging

logger = logging.getLogger(__name__)


@dataclass
class Database:
    database: str
    host: str
    password: str
    port: str
    user: str


def load_database_info() -> Database:
    logger.info("loading postgres configuration from file")
    Config = configparser.ConfigParser()
    Config.read(os.path.join(root_folder, "report_calculation.ini"))
    return deserialize(Database, Config._sections["database"])


def init() -> sessionmaker:
    logger.info("Initialising postgres connection")
    db = load_database_info()
    engine = create_engine(
        f"postgresql://{db.user}:{db.password}@{db.host}:{db.port}/{db.database}"
    )
    mapper_registry.metadata.create_all(bind=engine)
    return sessionmaker(bind=engine)


def open_session(
    session_factory: sessionmaker,
) -> Session:
    return session_factory()


session = open_session(init())
