from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData, create_engine
#from sqlalchemy import create_engine
#from sqlalchemy.orm import sessionmaker
from utils.log import *

import config
logger = init_logger(__name__, testing_mode=config.DEBUG_MODE)

convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)
db = SQLAlchemy(metadata=metadata)


# def reset_database():
#     #from database.models import AWSPrices, AWSInstance, AWSInstancePrice, AWSInstanceWorkLoad, AWSLowSummary
#     db.drop_all()
#     db.create_all()
