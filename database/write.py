from datetime import datetime, timedelta
#from datetime import timedelta
from database.models import AWSInstance, AWSPrices, AWSInstancePrice, AWSInstanceWorkLoad, AWSSummary
from database.utils import check_if_exist, simple_query_count, simple_sum, simple_query

from utils import init_logger
import config

logger = init_logger(__name__, testing_mode=config.DEBUG_MODE)


class WriteData(object):

    base_datetime = datetime.now().date()

    def __init__(self, conn, workload_tag):
        self.conn = conn
        self.workload_tag = workload_tag

    # --- INSTANCE ---#
    def save_instance(self, dict_instance_details, workload_profile):
        saved = False
        geoJson = None
        try:
            instance_type = dict_instance_details['deep_details']['Instance_type'],
            instance_id = dict_instance_details['instance_id']
            aws_region = dict_instance_details['aws_region']

            lat = None
            log = None
            if dict_instance_details['aws_region_coordinate']:
                lat_long = dict_instance_details['aws_region_coordinate'].replace(' ', '').split(',')
                lat = float(lat_long[0])
                log = float(lat_long[1])

                geoJson = {
                    "type": "Point",
                    "coordinates": [float(log), float(lat)]
                }

            query = {'instance_id': instance_id}
            if not check_if_exist(self.conn, AWSInstance, query):
                new_instance = AWSInstance(
                    instance_state_date= datetime.today(),
                    instance_id=instance_id,
                    instance_model=dict_instance_details['instance_model'],
                    aws_region_name=dict_instance_details['aws_region_name'],
                    aws_region_coordinate_lat = lat,
                    aws_region_coordinate_log = log,
                    aws_region_coordinate_geojson = geoJson,
                    instance_low_utilization_suspected=dict_instance_details['low_utilization_suspected'],
                    instance_ami_id=dict_instance_details['deep_details']['instance_ami'],
                    instance_state=dict_instance_details['deep_details']['InstanceState'],
                    instance_running_price=dict_instance_details['instance_running_price'],
                    instance_linux_kernel_version=dict_instance_details['deep_details']['kernel_version'],
                    instance_linux_distribution=dict_instance_details['deep_details']['Linux_distro'],
                    instance_ssh_pem_key=dict_instance_details['deep_details']['SSHKey'],
                    instance_auto_scaling_group=dict_instance_details['deep_details']['InASG'],
                    instance_auto_scaling_group_name=dict_instance_details['deep_details']['ASGName'],
                    instance_type=instance_type,
                    instance_ebs_optimized=dict_instance_details['deep_details']['Instance_ebsoptimized'],
                    aws_region=aws_region,
                    instance_vpc_id=dict_instance_details['deep_details']['Instance_vpc_id'],
                    instance_vpc_ip=dict_instance_details['deep_details']['InstanceIP'],
                    instance_vpc_subnet_id=dict_instance_details['deep_details']['instance_subnet_id'],
                    instance_vpc_availability_zone=dict_instance_details['deep_details']['instance_availabilityzone'],
                    instance_aws_account_id=dict_instance_details['deep_details']['instance_account_id'],
                    instance_reservation_id=dict_instance_details['deep_details']['instance_reservation_id'],
                    instance_spot_id=dict_instance_details['deep_details']['spot_instance_request_id'],
                    instance_launch_time=dict_instance_details['deep_details']['instance_launch_time'],
                    instance_tags=dict_instance_details['deep_details']['tags_string'],
                    instance_tags_json=dict_instance_details['deep_details']['tags_json'],
                    workload_tag= self.workload_tag
                )
                self.conn.session.add(new_instance)
                saved = True

            else:
                self.update_instance(dict_instance_details=dict_instance_details)
        except Exception as e:
            logger.error("Error on save data AWSInstance! {}".format(e))
        return saved

    def update_instance(self, instance_id=None, aws_region=None, dict_instance_details=None):
        saved = False
        try:
            instance_id = dict_instance_details['instance_id']
            aws_region = dict_instance_details['aws_region']

            query = {'instance_id': instance_id, 'aws_region': aws_region}
            aws_instances = simple_query(self.conn, AWSInstance, query)

            new_instance_type = dict_instance_details['deep_details']['Instance_type']
            if aws_instances.instance_type != new_instance_type:
                aws_instances.instance_type = new_instance_type
                logger.info("Updating instance type to instance {} to {}".format(instance_id,new_instance_type ))

            new_instance_state = dict_instance_details['deep_details']['InstanceState']
            if aws_instances.instance_state != new_instance_state:
                aws_instances.instance_previous_state = aws_instances.instance_state
                aws_instances.instance_state = new_instance_state
                aws_instances.instance_state_date = self.base_datetime
                logger.info("Updating instance state on instance {} to {}".format(instance_id, new_instance_state))

            new_instance_running_price = dict_instance_details['instance_running_price']
            if aws_instances.instance_running_price != new_instance_running_price:
                aws_instances.instance_running_price = new_instance_running_price
                aws_instances.instance_reservation_id = dict_instance_details['deep_details']['instance_reservation_id']
                logger.info("Updating price model on instance {} - {}".format(instance_id, new_instance_running_price))


            new_instance_ebs_optimized = dict_instance_details['deep_details']['Instance_ebsoptimized']
            if aws_instances.instance_ebs_optimized != new_instance_ebs_optimized:
                aws_instances.instance_ebs_optimized = new_instance_ebs_optimized
                logger.info("Updating ebs on instance {}".format(instance_id))


            new_instance_tags_json = dict_instance_details['deep_details']['tags_json']
            if aws_instances.instance_tags_json != new_instance_tags_json:
                aws_instances.instance_tags_json = new_instance_tags_json
                logger.info("Updating tag on instance {}".format(instance_id))

            self.conn.session.commit()
            saved = True
        except Exception as e:
            logger.error("Error on update Instance {} - {}".format(instance_id, e))
        return saved

    def delete_instance(self, instance_id, aws_region, dict_instance_details=None):
        pass

    # ---- PRICE ----#
    def save_price(self, dict_instance_details=None):
        saved = False
        try:
            instance_type = dict_instance_details['deep_details']['Instance_type'],
            aws_region = dict_instance_details['aws_region']

            ond_hrs_price = dict_instance_details['deep_details']['pricing_offers']['ondemand_price']
            ond_mth_price = dict_instance_details['deep_details']['pricing_offers']['ondemand_month_cost']

            rsv_hrs_price = dict_instance_details['deep_details']['pricing_offers']['reserved_price']
            rsv_mth_price = dict_instance_details['deep_details']['pricing_offers']['reserved_month_cost']
            rsv_offer_cod = dict_instance_details['deep_details']['pricing_offers']['reserved_offer_term_code']

            spt_hrs_price = dict_instance_details['deep_details']['pricing_offers']['spot_price'],
            spt_mth_price = dict_instance_details['deep_details']['pricing_offers']['spot_price_month']
            spt_offer_dat = dict_instance_details['deep_details']['pricing_offers']['spot_date_offer']

            ond_x_rsv_price_discount = ond_mth_price - rsv_mth_price
            rsv_price_discount_pct = ((ond_x_rsv_price_discount / ond_mth_price) * 100)

            ond_x_spt_price_discount = ond_mth_price - spt_mth_price
            spt_price_discount_pct = ((ond_x_spt_price_discount / ond_mth_price) * 100)

            query = {'instance_type': instance_type, 'aws_region': aws_region}
            if not check_if_exist(self.conn, AWSPrices, query):
                new_price = AWSPrices(
                    instance_type=instance_type,
                    aws_region=aws_region,
                    price_date=self.base_datetime,

                    price_ondemand_price_hrs_usd=ond_hrs_price,
                    price_ondemand_price_mth_usd=ond_mth_price,

                    price_reserved_price_hsr_usd=rsv_hrs_price,
                    price_reserved_price_mth_usd=rsv_mth_price,
                    price_reserved_price_offer_code=rsv_offer_cod,

                    price_spot_price_hsr_usd=spt_hrs_price,
                    price_spot_price_mth_usd=spt_mth_price,
                    price_spot_offer_date=spt_offer_dat,

                    price_ondemand_reserved_saving= round(ond_x_rsv_price_discount,2),
                    price_ondemand_reserved_saving_pct = round(rsv_price_discount_pct,2),

                    price_ondemand_spot_saving=round(ond_x_spt_price_discount,2),
                    price_ondemand_spot_saving_pct=round(spt_price_discount_pct,2),

                )
                self.conn.session.add(new_price)
                self.conn.session.commit()
                saved = True
        except Exception as e:
            logger.error("Error on save data AWSPrices! {}".format(e))
        return saved

    def update_price(self, instance_type=None, aws_region=None, dict_instance_details=None):
        pass

    def dele_price(self, instance_type=None, aws_region=None, dict_instance_details=None):
        pass

    # ---- INSTANCE-PRICE ---#
    def save_instance_price(self,  dict_instance_details, workload_tag):
        saved = False
        try:
            instance_id = dict_instance_details['instance_id']
            instance_type = dict_instance_details['deep_details']['Instance_type'],
            aws_region = dict_instance_details['aws_region']
            running_type = dict_instance_details['instance_running_price']

            if running_type == 'OnDemand':
                instance_hrs_price_usd = dict_instance_details['deep_details']['pricing_offers']['ondemand_price']
                instance_mth_price_usd = dict_instance_details['deep_details']['pricing_offers']['ondemand_month_cost']

            if running_type == 'Reserved':
                instance_hrs_price_usd = dict_instance_details['deep_details']['pricing_offers']['reserved_price']
                instance_mth_price_usd = dict_instance_details['deep_details']['pricing_offers']['reserved_month_cost']

            if running_type == 'Spot':
                instance_hrs_price_usd = dict_instance_details['deep_details']['pricing_offers']['spot_price']
                instance_mth_price_usd = dict_instance_details['deep_details']['pricing_offers']['spot_price_month']

            query = {'instance_id': instance_id,
                     'instance_type': instance_type,
                     'instance_price_date': self.base_datetime}
            if not check_if_exist(self.conn, AWSInstancePrice, query):
                new_inst_price = AWSInstancePrice(
                    instance_id=instance_id,
                    instance_type=instance_type,
                    aws_region=aws_region,
                    instance_price_date=self.base_datetime,
                    instance_running_price=running_type,
                    instance_hrs_price_usd=instance_hrs_price_usd,
                    instance_mth_price_usd=instance_mth_price_usd,
                    instance_last_state=dict_instance_details['deep_details']['InstanceState'],
                    workload_tag= self.workload_tag

                )
                self.conn.session.add(new_inst_price)
                self.conn.session.commit()
                saved = True
        except Exception as e:
            logger.error("Error on save data AWSInstancePrice! {}".format(e))
        return saved

    # --- INSTANCE-WORKLOAD --#
    def save_instance_workload(self, dict_instance_details=None):
        saved = False
        try:
            instance_id = dict_instance_details['instance_id']
            instance_type = dict_instance_details['deep_details']['Instance_type'],
            aws_region = dict_instance_details['aws_region']
            running_type = dict_instance_details['instance_running_price']

            if running_type == 'OnDemand':
                instance_hrs_price_usd = dict_instance_details['deep_details']['pricing_offers']['ondemand_price']
                instance_mth_price_usd = dict_instance_details['deep_details']['pricing_offers']['ondemand_month_cost']

            if running_type == 'Reserved':
                instance_hrs_price_usd = dict_instance_details['deep_details']['pricing_offers']['reserved_price']
                instance_mth_price_usd = dict_instance_details['deep_details']['pricing_offers']['reserved_month_cost']

            if running_type == 'Spot':
                instance_hrs_price_usd = dict_instance_details['deep_details']['pricing_offers']['spot_price']
                instance_mth_price_usd = dict_instance_details['deep_details']['pricing_offers']['spot_price_month']

            query = {'instance_id': instance_id,
                     'workload_date': self.base_datetime,
                     'aws_region': aws_region,
                     'instance_type': instance_type }

            if not check_if_exist(self.conn, AWSInstanceWorkLoad, query):
                new_inst_workload = AWSInstanceWorkLoad(
                    workload_date=self.base_datetime,
                    instance_id=instance_id,
                    aws_region=aws_region,
                    instance_type=dict_instance_details['deep_details']['Instance_type'],

                    cpu_percentage=dict_instance_details['deep_details']['cloudw_cpu'],
                    available_memory_percentage=dict_instance_details['deep_details']['avaliable_ram_pct'],
                    network_in_bytes_aggr=dict_instance_details['deep_details']['cloudw_netin'],
                    network_ou_bytes_aggr=dict_instance_details['deep_details']['cloudw_netou'],

                    cloudwatch_aggregation_type=dict_instance_details['deep_details']['cloudw_aggregation_type'],
                    cloudwatch_aggregation_days=dict_instance_details['deep_details']['cloudw_aggregation_days'],
                    cloudwatch_aggregation_period_from=dict_instance_details['deep_details'][
                        'cloudw_aggregation_period_from'],
                    cloudwatch_aggregation_period_to=dict_instance_details['deep_details'][
                        'cloudw_aggregation_period_to'],
                    cloudwatch_period_seconds=dict_instance_details['deep_details']['cloudw_period_seconds'],

                    workload_criteria_check=dict_instance_details['deep_details']['low_utilizaion_check'],
                    workload_low_utilization=dict_instance_details['low_utilization_suspected']
                )
                self.conn.session.add(new_inst_workload)
                self.conn.session.commit()
                saved = True
        except Exception as e:
            logger.error("Error on save data AWSInstanceWorkLoad! {}".format(e))
        return saved

    def save_summary_workload(self, dict_instance_details=None):
        saved = False
        query = {'summary_date': self.base_datetime}
        if not check_if_exist(self.conn, AWSSummary, query):
            try:

                total_ec2_ondemand = simple_query_count(self.conn, AWSInstance, {'instance_running_price': "OnDemand"})
                total_ec2_reserved = simple_query_count(self.conn, AWSInstance, {'instance_running_price': "Reserved"})
                total_ec2_spot = simple_query_count(self.conn, AWSInstance, {'instance_running_price': "Spot"})
                total_instances_flagged_lowuse = simple_query_count(self.conn, AWSInstance, {'instance_low_utilization_suspected': True})

                total_cost_ec2_ondemand_month = simple_query_count(self.conn, AWSInstance, {'instance_low_utilization_suspected': True})
                total_cost_ec2_reserved_month = simple_query_count(self.conn, AWSInstance, {'instance_low_utilization_suspected': True})
                total_cost_ec2_spot_month  = simple_query_count(self.conn, AWSInstance, {'instance_low_utilization_suspected': True})

                opportunity_save_money_reservation = simple_sum(self.conn, AWSInstance, {'instance_running_price': "OnDemand"})
                opportunity_save_money_spot_asg = simple_sum(self.conn, AWSInstance, {'instance_low_utilization_suspected': True})

                new_summary = AWSSummary(
                    summary_date = self.base_datetime,
                    total_ec2_ondemand = total_ec2_ondemand,
                    total_ec2_reserved = total_ec2_reserved,
                    percentage_rsv_x_ond = ((total_ec2_ondemand/total_ec2_reserved) * 100),
                    total_ec2_spot = total_ec2_spot,
                    total_instances_flagged_lowuse = total_instances_flagged_lowuse,

                    total_cost_ec2_ondemand_month = total_cost_ec2_ondemand_month,
                    total_cost_ec2_reserved_month = total_cost_ec2_reserved_month,
                    total_cost_ec2_spot_month = total_cost_ec2_spot_month,

                    opportunity_save_money_reservation = opportunity_save_money_reservation,
                    opportunity_save_money_spot_asg = opportunity_save_money_spot_asg,

                    summary_tag = self.workload_tag

                )
                self.conn.session.add(new_summary)
                self.conn.session.commit()
                saved = True
            except Exception as e:
                logger.error("Error on save data AWSSummary! {}".format(e))
        return saved


    def save(self, dict_instance_details):
        saved = False
        try:
            logger.info("Saving data into Database")

            self.save_instance(dict_instance_details, self.workload_tag)
            self.save_price(dict_instance_details)
            self.save_instance_price(dict_instance_details, self.workload_tag)
            self.save_instance_workload(dict_instance_details)
            #self.save_summary_workload(dict_instance_details,  ,self.workload_profile)

            self.conn.session.commit()

            saved = True
        except Exception as e:
            logger.error("Error on saving data {}".format(e))
        return saved
