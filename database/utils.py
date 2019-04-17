from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.sql import func

from utils import init_logger
import config
logger = init_logger(__name__, testing_mode=config.DEBUG_MODE)


def check_if_exist(conn, object_name, query):
    exists = False
    try:
        exist_instance = conn.session.query(object_name).filter_by(**query).scalar() is not None
        if exist_instance:
            exists = True
    except NoResultFound:
        logger.debug("something NoResultFound wrong here {}".format(NoResultFound))
    except Exception as e:
        logger.debug("something gona wrong here {}".format(e))
    return exists


def simple_query(conn, object_name, query):
    data = None
    try:
        data = conn.session.query(object_name).filter_by(**query).first()
    except NoResultFound:
        logger.debug("something NoResultFound wrong here {}".format(NoResultFound))
    except Exception as e:
        logger.debug("something gona wrong here {}".format(e))
    return data


def simple_query_count(conn, object_name, query):
    data = None
    try:
        data = conn.session.query(func.count(object_name)).filter_by(**query).scalar()
    except NoResultFound:
        logger.debug("something NoResultFound wrong here {}".format(NoResultFound))
    except Exception as e:
        logger.debug("something gona wrong here {}".format(e))
    return data


def simple_sum(conn, object_name, query):
    data = None
    try:
        data = conn.session.query(func.sum(object_name).filter_by(**query)).scalar()
    except NoResultFound:
        logger.debug("something NoResultFound wrong here {}".format(NoResultFound))
    except Exception as e:
        logger.debug("something gona wrong here {}".format(e))
    return data
