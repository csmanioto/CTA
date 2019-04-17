import boto3
#import logging.config
from utils.log import *
import config


class AWSInterface(object):
    logger = init_logger(__name__, testing_mode=config.DEBUG_MODE)
    settings_profile = None

    """
        AWSInterface class.
        Methods to get information and reports overs AWS.
    """
    aws_connection = None
    ec2_connection = None
    asg_connection = None
    aws_regions = {
        "us-east-1": "US East (N. Virginia)",
        "us-east-2": "US East (Ohio)",
        "us-west-1": "US West (N. California)",
        "us-west-2": "US West (Oregon)",
        "sa-east-1": "South America (Sao Paulo)",
        "ca-central-1": "Canada (Central)",
        "cn-north-1": "China (Beijing)",
        "cn-northwest-1": "China (Ningxia)",
        "ap-northeast-2": "Asia Pacific (Seoul)",
        "ap-south-1": "Asia Pacific (Mumbai)",
        "eu-central-1": "EU (Frankfurt)",
        "ap-southeast-2": "Asia Pacific (Sydney)",
        "eu-west-1": "EU (Ireland)",
        "ap-southeast-1": "Asia Pacific (Singapore)",
        "ap-northeast-1": "Asia Pacific (Tokyo)",
        "eu-west-2": "EU (London)",
        "eu-west-3": "EU (Paris)"
    }

    aws_regions_json_id = {
        "us-east-1": "us-east",
        "us-east-2": "us-east-2",
        "us-west-1": "us-west",
        "us-west-2": "us-west-2",
        "eu-west-1": "eu-ireland",
        "eu-central-1": "eu-central-1",
        "eu-west-2": "eu-west-2",
        "ap-southeast-1": "apac-sin",
        "ap-southeast-2": "apac-syd",
        "ap-northeast-1": "apac-tokyo",
        "ap-northeast-2": "apac-seoul",
        "sa-east-1": "sa-east-1",
        "us-gov-west-1": "us-gov-west-1",
        "ca-central-1": "ca-central-1",
        "ap-northeast-3": "apac-osaka",
        "eu-west-3": "eu-west-3"
    }

    # long / lat
    aws_regions_coordinates = {
        "eu-west-1": "53.350140, -6.266155",
        "eu-west-2": "51.509865, -0.118092",
        "us-west-2": "44.187126, -124.114609",
        "us-east-2": "40.367474, -82.996216",
    }

    def get_current_region(self):
        return self.aws_connection.get_credentials()

    def aws_regions_id_to_name(self, region_id):
        full_name = self.aws_regions[region_id]
        if full_name is None:
            full_name = "Region not found"
        return full_name

    def aws_get_regions_id(self):
        regions_id = self.aws_regions.keys()
        return regions_id

    def aws_get_geo_region(self, region_id):
        coordinates = self.aws_regions_coordinates[region_id]
        if coordinates is None:
            coordinates = "Region not found"
        return coordinates

    def aws_get_region_json_id(self, region_id):
        region_json = self.region_id[region_id]
        if region_json is None:
            region_json = "Region not found"
        return region_json

    def __init__(self, settings_profile=None, aws_access_key_id=None, aws_secret_access_key=None):
        # Have I a profile information ? or I should use aws_access details ?
        self.settings_profile = settings_profile
        try:
            if settings_profile is None:
                self.aws_connection = boto3.Session(aws_access_key_id=aws_access_key_id,
                                                    aws_secret_access_key=aws_secret_access_key)
            if settings_profile['credential'] is not None:
                self.credential = settings_profile['credential']
                self.aws_connection = boto3.Session(profile_name=self.credential)
            else:
                self.aws_connection = boto3.Session(aws_access_key_id=settings_profile['aws_access_key_id'],
                                                    aws_secret_access_key=settings_profile['aws_secret_access_key'])
        except Exception as e:
            self.logger.debug("I can't open a boto3 Session {}".format(e))
