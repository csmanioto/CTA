from business.aws import *
import logging.config
from datetime import datetime, timedelta

import json
from utils import *
logger = log.init_logger(__name__, testing_mode=config.DEBUG_MODE)

"""
There are a contract code from AWS documentation (I need to waste huge time to find out that codes.
The codes is used to give a meaning in a unit/price.

OnDemand offerTermCode
'JRTCKXETXF' - OnDemand offerTermCode

RESERVED OFFER TERM CODE
'BPH4J8HBKS' - {'LeaseContractLength': '3yr', 'OfferingClass': 'standard', 'PurchaseOption': 'No Upfront'}
'NQ3QZPMQV9' - {'LeaseContractLength': '3yr', 'OfferingClass': 'standard', 'PurchaseOption': 'All Upfront'}
'HU7G6KETJZ' - {'LeaseContractLength': '1yr', 'OfferingClass': 'standard', 'PurchaseOption': 'Partial Upfront'}
'6QCMYABX3D' - {'LeaseContractLength': '1yr', 'OfferingClass': 'standard', 'PurchaseOption': 'All Upfront'}
'R5XV2EPZQZ' - {'LeaseContractLength': '3yr', 'OfferingClass': 'convertible', 'PurchaseOption': 'Partial Upfront'}
'VJWZNREJX2' - {'LeaseContractLength': '1yr', 'OfferingClass': 'convertible', 'PurchaseOption': 'All Upfront'}
'MZU6U2429S' - {'LeaseContractLength': '3yr', 'OfferingClass': 'convertible', 'PurchaseOption': 'All Upfront'}
'38NPMPTW36' - {'LeaseContractLength': '3yr', 'OfferingClass': 'standard', 'PurchaseOption': 'Partial Upfront'}
'7NE97W5U4E' - {'LeaseContractLength': '1yr', 'OfferingClass': 'convertible', 'PurchaseOption': 'No Upfront'}
'CUZHX8X6JH' - {'LeaseContractLength': '1yr', 'OfferingClass': 'convertible', 'PurchaseOption': 'Partial Upfront'}
'Z2E3P23VKM' - {'LeaseContractLength': '3yr', 'OfferingClass': 'convertible', 'PurchaseOption': 'No Upfront'}
'4NA7Y494T4' - {'LeaseContractLength': '1yr', 'OfferingClass': 'standard', 'PurchaseOption': 'No Upfront'}
"""


class AWSPrices(AWSInterface):
    """
      Auxiliary method: Extract the unit/price for Spot Instance

      """

    def __get_ec2_spot_price(self, instance_type, region_id):

        StartTime = (datetime.now() - timedelta(minutes=5)).isoformat()
        EndTime = datetime.now()
        client = boto3.client('ec2', region_name=region_id)
        price_raw = client.describe_spot_price_history(InstanceTypes=[instance_type],
                                                       MaxResults=1,
                                                       StartTime=StartTime,
                                                       EndTime=EndTime,
                                                       ProductDescriptions=['Linux/UNIX (Amazon VPC)'],
                                                       )
        unit = 'Hrs'
        price = 0.00
        if price_raw['SpotPriceHistory'][0].get('SpotPrice'):
            price = float(price_raw['SpotPriceHistory'][0].get('SpotPrice'))
        dateoffer = StartTime
        return unit, price, dateoffer

    """
        Auxiliary method: Return the AWS contract code for search the price
        Param1: Kind of Contract: OnDemand or Reserved
        Param2: Obligate for Reserved: NoUpfront or AllUpfron or PartialUpfront
        Param3: Obligate for Reserved: standart or convertible
        Param3: Obligate for Reserved: Lease time can be: 1yr or 3yr
        Return: List of contracts with this kind of contract
    """

    def __aws_contract_code(self, contract_category, reserved_type=None, offering_class=None,
                            lease_contract_length=None):
        contract_class = None
        # I need to finish this Dict similar the complet list above
        contracts = {'OnDemand': ['JRTCKXETXF'],
                     'Reserved': {'NoUpfront':
                         [
                             {'standard1yr': '4NA7Y494T4'},
                             {'convertible1yr': '7NE97W5U4E'},
                             {'standard3yr': 'BPH4J8HBKS'},
                             {'convertible3yr': 'Z2E3P23VKM'},
                         ]
                     },
                     }

        contract = None
        if contract_category is 'OnDemand':
            contract = contracts[contract_category][0]
            contract_class = "OnDemand"

        if contract_category == "Reserved":
            # Contract for NoUpfront, AllUpfron or PartialUpfront
            reserved_contracts_list = contracts['Reserved'].get(reserved_type)
            contract_class = "{}{}".format(offering_class, lease_contract_length)
            found_contract = False
            for dict_contract in reserved_contracts_list:
                for dict_key in dict_contract:
                    if contract_class in dict_contract.keys():
                        contract = dict_contract[dict_key]
                        found_contract = True
                        break
                if found_contract:
                    contract_class = "{} - {} - {}".format(contract_category, contract_class, reserved_type)
                    break

        return contract, contract_class

    """
    Auxiliary method: Get the Price Dataset from AWS API 
    Param1: Instance Type, exemple m4.4xlarge
    Param2: Regiond-id sa-east-1
    Return: Json with a complex dataset with a On-demand and Reservated price
    """
    def __query_awsec2_offer(self, instance_type, instance_region_id, preInstalledSw="NA"):
        price_connection = None
        intance_price_offer = None

        # Connection on AWS API Price
        price_api_regions = ['us-east-1', 'ap-south-1']
        try:
            #  By the doc, We gonna use the us-east-1 as endpoint for price quering.
            try:
                price_connection = self.aws_connection.client('pricing', region_name=price_api_regions[0])
                logging.debug("Connection on aws-price api throught region: {}".format(price_api_regions[0]))
            except Exception as e:
                logging.error("Fail on connect to AWS Price API throught the region {} - {}".format(price_api_regions[0], e))
            else:
                price_connection = self.aws_connection.client('pricing', region_name=price_api_regions[1])
                logging.debug("Connection on aws-price api throught region: {}".format(price_api_regions[1]))

            # Starting the code....

            region_full_name = self.aws_regions_id_to_name(instance_region_id)
            # Querying all prices for instance type on that region.
            intance_price_offer = price_connection.get_products(ServiceCode='AmazonEC2',
                                                                Filters=[
                                                                    {'Type': 'TERM_MATCH',
                                                                     'Field': "instanceType",
                                                                     'Value': instance_type
                                                                     },

                                                                    {'Type': 'TERM_MATCH',
                                                                     'Field': "tenancy",
                                                                     'Value': "Shared"
                                                                     },

                                                                    {'Type': 'TERM_MATCH',
                                                                     'Field': "servicename",
                                                                     'Value': "Amazon Elastic Compute Cloud"
                                                                     },

                                                                    {'Type': 'TERM_MATCH',
                                                                     'Field': "operatingSystem",
                                                                     'Value': "Linux"
                                                                     },

                                                                    {'Type': 'TERM_MATCH',
                                                                     'Field': "location",
                                                                     'Value': region_full_name
                                                                     },
                                                                    {
                                                                     'Type': 'TERM_MATCH',
                                                                      'Field': "preInstalledSw",
                                                                      'Value': preInstalledSw
                                                                    },
                                                                    {
                                                                        'Type': 'TERM_MATCH',
                                                                        'Field': "capacitystatus",
                                                                        'Value': 'Used'
                                                                    }
                                                                ]
                                                                )
        except Exception as e:
            logging.error("error to get result price with price api {}".format(e))
        price_list = intance_price_offer['PriceList'][0]
        #price_list = intance_price_offer['PriceList']
        # "operation":"RunInstances"}
        # "preInstalledSw":"NA"
        # for item in price_list:

        return json.loads(price_list)

    """
     Auxiliary method: Extract the unit/price for On-Demand or Reserved prince from big api returned dataset 
     Param1: Big JSON with a lot of data
     Param2: Category of the contract - OnDemand or Reserved
     Param3: Obligate for Reserved: NoUpfront or AllUpfron or PartialUpfront
     Param4: Obligate for Reserved: standart or convertible
     Param5: Obligate for Reserved: Lease time can be: 1yr or 3y
     Return: List with Unit/Price - exemple ['Hrs', '0.005']
    """
    def __get_ec2_prince_by_contract(self, json_price_list, contract_category, reserved_type=None, offering_class=None, lease_contract_length=None):
        offer = None
        try:
            json_items = json_price_list
            sku = str(json_items['product']['sku'])  # Stock Keeping Unit (SKU)

            contract_details = self.__aws_contract_code(contract_category, reserved_type=reserved_type, offering_class=offering_class, lease_contract_length=lease_contract_length)
            contract_code = contract_details[0]
            contract_description = contract_details[1]

            key = "{}.{}".format(sku, contract_code)
            priced_idx = str(list(json_items['terms'][contract_category][key]['priceDimensions'].keys())[0])
            unit = json_items['terms'][contract_category][key]['priceDimensions'][priced_idx]['unit']
            price = json_items['terms'][contract_category][key]['priceDimensions'][priced_idx]['pricePerUnit']['USD']
            offer = [unit, price, contract_code, contract_description]
        except Exception as e:
            logger.error("Error on get {} price {}".format(contract_category,e))
        finally:
            return offer


    """
    Auxiliary method: Convert the price in hours or minutes to month cost
    Param1: Unit (Hrs or Unit)
    Param2: Price in USD
    Return: Total per Month
    """
    def __convert_hour_prince_to_month(self, unit, price):
        month_cost = 0.0
        try:
            if 'Hrs' in unit:
                month_cost = float(price) * 720
            else:
                month_cost = (float(price) * 60) * 720
        except Exception as e:
            logging.error("Error during convertion price unit to month {}".format(e))
        return round(month_cost,3)



    """
        Get the EC2's price
        Having a look on this official document: https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/using-pelong.html
        We can use just two regions options for this query: us-east-1 or ap-south-1
    
        Param1: type of the instance, exeample: m4.2xlarge
        Param2: regions of this instance, example: sa-east-1
        Return: Dictionary with complete information of price
        - Price on-demand (Linux Option)
        - Monthly cost if on-demand
        - Reserved Instance price using the worst option ( No-upfront 1yrs)
        - Monthly cost if RI
        - Percentage of different monthly
        - Total saving using the worst RI option
    """
    def get_ec2_prices(self, instance_type, aws_region):
        json_total_ec2_offer = self.__query_awsec2_offer(instance_type, aws_region)

        # On-Demand Price
        ondemand_offer = self.__get_ec2_prince_by_contract(json_total_ec2_offer, contract_category="OnDemand")
        ondemand_offer_month_cost = self.__convert_hour_prince_to_month(ondemand_offer[0], ondemand_offer[1])

        spot_offer = self.__get_ec2_spot_price(instance_type, aws_region)
        spot_offer_month_cost = self.__convert_hour_prince_to_month(spot_offer[0], spot_offer[1])
        spot_date_offer = spot_offer[2]


        # Reserved Price
        reserved_offer = self.__get_ec2_prince_by_contract(json_total_ec2_offer, contract_category="Reserved", reserved_type='NoUpfront', offering_class='standard', lease_contract_length='1yr')
        if not reserved_offer:
            reserved_offer = ['Hrs', '0.00', 'Empty', 'Empty', 'Reseved']
        reserved_offer_month_cost = self.__convert_hour_prince_to_month(reserved_offer[0], reserved_offer[1])
        reserved_offer_contract_code = reserved_offer[2]
        reserved_offer_contract_description = reserved_offer[3]


        # Checking the deference between On-Demand vs Reserved price
        #if reserved_offer_month_cost < ondemand_offer_month_cost:
        #    percent_difference = round(((ondemand_offer_month_cost / reserved_offer_month_cost) - 1) * 100, 2)
        #    save_money = ondemand_offer_month_cost - reserved_offer_month_cost
        #else:
        #    percent_difference = -1
        #    save_money = 0.00
        #    logging.error("Fail to capture reserved price, maybe the value is in quantity instead of hours")

        cost_dict = {'ondemand_unit': ondemand_offer[0],
                     'ondemand_price': round(float(ondemand_offer[1]), 4),
                     'ondemand_month_cost': round(ondemand_offer_month_cost, 4),
                     'reserved_unit': reserved_offer[0],
                     'reserved_price': round(float(reserved_offer[1]), 4),
                     'reserved_offer_term_code': "{} - {}".format(reserved_offer_contract_code, reserved_offer_contract_description),
                     'reserved_month_cost': round(reserved_offer_month_cost, 4),
                     #'percent_difference': round(percent_difference, 6),
                     #'save_money_month': round(save_money, 2)
                     'spot_unit': spot_offer[0],
                     'spot_price': spot_offer[1],
                     'spot_price_month': spot_offer_month_cost,
                     'spot_date_offer': spot_date_offer
                    }
        return cost_dict
