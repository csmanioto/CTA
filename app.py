# external api and libs
from flask import Flask, Blueprint
# from flask import Blueprint
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy_utils import database_exists, create_database, drop_database
#from flask_login import LoginManager, current_user, login_user
#import os

# APP includes
import config
from utils.log import *
from business.aws.ec2 import EC2
#from api.restplus import api

logger = init_logger(__name__, testing_mode=config.DEBUG_MODE)

app = Flask(__name__)
app.config['SERVER_NAME'] = "{}:{}".format(config.API_INTERFACE, config.API_TCP_PORT)
app.config['SQLALCHEMY_DATABASE_URI'] = config.DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = config.DATABASE_TRACK_MODIFICATIONS
app.config['SWAGGER_UI_DOC_EXPANSION'] = 'list'
app.config['RESTPLUS_VALIDATE'] = True
app.config['RESTPLUS_MASK_SWAGGER'] = False
app.config['ERROR_404_HELP'] = False

convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)
db = SQLAlchemy(app, metadata=metadata)

# def get_env_variable(name):
#     try:
#         return os.environ[name]
#     except KeyError:
#         message = "Expected environment variable '{}' not set.".format(name)
#         raise Exception(message)

@app.cli.command('resetdb')
def resetdb_command():
    from database.models import AWSPrices, AWSInstance, AWSInstancePrice, AWSInstanceWorkLoad, AWSSummary
    """Destroys and creates the database + tables."""

    if database_exists(config.DATABASE_URI):
        print('Deleting database.')
        drop_database(config.DATABASE_URI)
    if not database_exists(config.DATABASE_URI):
        print('Creating database.')
        create_database(config.DATABASE_URI)

    print('Creating tables.')
    db.create_all()
    db.session.commit()
    print('Shiny!')


# def initialize_app (flask_app):
#
#     blueprint = Blueprint('api', __name__, url_prefix='/api')
#     api.init_app(blueprint)
#     #pi.add_namespace(lowuser_get_instances)
#     #api.add_namespace(loweuser_get_top_3)
#     flask_app.register_blueprint(blueprint)
#     db.init_app(flask_app)


def main():
    #  initialize_app(app)
    logger.info('>>>>> Starting at http://{}/api/ <<<<<'.format(app.config['SERVER_NAME']))
    app.run(debug=config.DEBUG_MODE)


@app.cli.command('scan_aws')
def scan():
    for scan_profile in config.AWS_CREDENTIAL_CONFIG:
        if scan_profile['enable']:
            logger.info("Stating scan process to credital/enviroment {}".format(scan_profile['credential']))
            ec2 = EC2(scan_profile)
            #details = ec2.get_ec2_details(instance_id="i-0e350f0bcebbc4238", aws_region='us-east-2', db_conn=db)
            #details = ec2.get_ec2_details(instance_id="i-def11255", aws_region='eu-west-1', db_conn=db)
            #details = ec2.get_ec2_details(instance_id=""i-047870d8f758e7894", aws_region='us-east-2', db_conn=db)
            details = ec2.get_ec2_details(db_conn=db)
            if not details[0]:
                print("No details for instance")
            else:
                print(details[0])


if __name__ == "__main__":
    # main()
    scan()
    print("running...")
