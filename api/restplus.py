import logging
import traceback

from flask_restplus import Api
import config
from sqlalchemy.orm.exc import NoResultFound

log = logging.getLogger(__name__)

api = Api(version='1.0', title='AWS Low Utilization Tracker',
          description='Scan in a AWS accountfor EC2 low utilization and others wast money in all VPCs')

@api.errorhandler
def default_error_handler(e):
    message = 'An unhandled exception occurred.'
    log.exception(message)

    if not config.DEBUG_MODE:
        return {'message': message}, 500


@api.errorhandler(NoResultFound)
def database_not_found_error_handler(e):
    log.warning(traceback.format_exc())
    return {'message': 'A database result was required but none was found.'}, 404