import os
import logging
from dotenv import load_dotenv
import sys

from app.common.error import InternalError


load_dotenv()


class Config:
    version = "0.1.0"
    title = "releads"
    _is_pytest = 'pytest' in sys.modules

    if _is_pytest:
        db_name = os.environ.get('TEST_MONGO_DB', 'test_db')
        mongodb_url = f"{os.environ.get('TEST_MONGO_URL', 'mongodb://localhost:27017')}/{db_name}"
        db_username = os.environ.get('TEST_MONGO_USER', '')
        db_password = os.environ.get('TEST_MONGO_PASSWORD', '')
    else:
        db_name = os.environ['MONGO_DB']
        mongodb_url = f"{os.environ['MONGO_URL']}/{db_name}"
        db_username = os.environ['MONGO_USER']
        db_password = os.environ['MONGO_PASSWORD']

    app_settings = {
        'db_name': db_name,
        'mongodb_url': mongodb_url,
        'db_username': db_username,
        'db_password': db_password,
        'max_db_conn_count': os.environ['MAX_CONNECTIONS_COUNT'],
        'min_db_conn_count': os.environ['MIN_CONNECTIONS_COUNT'],
    }

    @classmethod
    def check_app_settings_on_none(cls):
        for k, v in cls.app_settings.items():
            if v is None:
                logging.error(f'Config variable error. {k} cannot be None')
                raise InternalError([{"message": "Server configure error"}])
            else:
                logging.info(f'Config variable {k} is {v}')
