# from database import db
#from geoalchemy2 import Geometry
#from sqlalchemy import Column
from sqlalchemy.dialects.postgresql.json import JSONB

from app import db


class AWSInstance(db.Model):
    __tablename__ = 'aws_instances'

    instance_id = db.Column(db.String(30), primary_key=True)
    instance_model = db.Column(db.String(30), index=True, nullable=False)
    aws_region = db.Column(db.String(30), primary_key=True, nullable=False)
    aws_region_name = db.Column(db.String(60), nullable=False)
    aws_region_coordinate_lat = db.Column(db.String(255), nullable=True)
    aws_region_coordinate_log = db.Column(db.String(255), nullable=True)
    aws_region_coordinate_geojson = db.Column(db.JSON, nullable=True)

    instance_low_utilization_suspected = db.Column(db.Boolean,
                                                   index=True,
                                                   nullable=False)
    instance_ami_id = db.Column(db.String(30))

    instance_running_price = db.Column(db.String(30))
    instance_state = db.Column(db.String(19),
                               nullable=False)
    instance_state_date = db.Column(db.DateTime,
                                    nullable=False)
    instance_previous_state = db.Column(db.String(19),
                                        nullable=True)
    instance_linux_kernel_version = db.Column(db.String(30))
    instance_linux_distribution = db.Column(db.String(30))
    instance_ssh_pem_key = db.Column(db.String(255))
    instance_auto_scaling_group = db.Column(db.Boolean)
    instance_auto_scaling_group_name = db.Column(db.String(255))
    instance_type = db.Column(db.String(255),
                              nullable=False)
    instance_ebs_optimized = db.Column(db.Boolean)
    instance_vpc_id = db.Column(db.String(30))
    instance_vpc_subnet_id = db.Column(db.String(30))
    instance_vpc_ip = db.Column(db.String(30))
    instance_vpc_availability_zone = db.Column(db.String(30))
    instance_aws_account_id = db.Column(db.String(30))
    instance_reservation_id = db.Column(db.String(50))
    instance_spot_id = db.Column(db.String(30))
    instance_launch_time = db.Column(db.DateTime)
    instance_tags = db.Column(db.String(9999))
    instance_tags_json = db.Column(JSONB, index=True)
    workload_tag = db.Column(db.String(255), index=True, nullable=False) # Profile would be: test, qa, prod.

    def __init__(self, instance_id, instance_model, aws_region, aws_region_name,
                 instance_low_utilization_suspected, instance_ami_id, instance_state,
                 instance_linux_kernel_version, instance_linux_distribution, instance_ssh_pem_key
                 , instance_auto_scaling_group, instance_auto_scaling_group_name, instance_type, instance_ebs_optimized
                 , instance_vpc_id, instance_vpc_subnet_id, instance_vpc_ip, instance_vpc_availability_zone
                 , instance_aws_account_id, instance_reservation_id, instance_spot_id, instance_launch_time,
                 instance_tags, instance_tags_json, instance_state_date, workload_tag,
                 aws_region_coordinate_lat=None, aws_region_coordinate_log=None, aws_region_coordinate_geojson=None,
                 instance_previous_state=None, instance_running_price=None):
        self.instance_id = instance_id
        self.instance_model = instance_model
        self.aws_region = aws_region
        self.aws_region_name = aws_region_name
        self.aws_region_coordinate_lat = aws_region_coordinate_lat
        self.aws_region_coordinate_log = aws_region_coordinate_log
        self.aws_region_coordinate_geojson = aws_region_coordinate_geojson
        self.instance_low_utilization_suspected = instance_low_utilization_suspected
        self.instance_ami_id = instance_ami_id
        self.instance_state = instance_state
        self.instance_linux_kernel_version = instance_linux_kernel_version
        self.instance_linux_distribution = instance_linux_distribution
        self.instance_ssh_pem_key = instance_ssh_pem_key
        self.instance_auto_scaling_group = instance_auto_scaling_group
        self.instance_auto_scaling_group_name = instance_auto_scaling_group_name
        self.instance_type = instance_type
        self.instance_ebs_optimized = instance_ebs_optimized
        self.instance_vpc_id = instance_vpc_id
        self.instance_vpc_subnet_id = instance_vpc_subnet_id
        self.instance_vpc_ip = instance_vpc_ip
        self.instance_vpc_availability_zone = instance_vpc_availability_zone
        self.instance_aws_account_id = instance_aws_account_id
        self.instance_reservation_id = instance_reservation_id
        self.instance_spot_id = instance_spot_id
        self.instance_launch_time = instance_launch_time
        self.instance_tags = instance_tags
        self.instance_tags_json = instance_tags_json
        self.instance_state_date = instance_state_date
        self.instance_previous_state = instance_previous_state
        self.instance_running_price = instance_running_price
        self.workload_tag = workload_tag.upper()

    def __repr__(self):
        return "<AWSInstance '{}'>".format(self.instance_id)

class AWSEBS(db.Model):
    __tablename__ = 'aws_ebs'

    ebs_volume_id = db.Column(db.String(30), primary_key=True)
    ebs_aws_az = db.Column(db.String(30), primary_key=True)
    instance_id = db.Column(db.String(30), index=True)
    snapshot_id = db.Column(db.String(30), index=True)

    ebs_size = db.Column(db.String(14), nullable=False)
    ebs_volume_type = db.Column(db.String(14), nullable=False)
    ebs_iops = db.Column(db.String(14), nullable=False)
    ebs_alarm_status = db.Column(db.String(30))
    ebs_status = db.Column(db.String(30))
    ebs_volume_status_ok = db.Column(db.Boolean)
    ebs_volume_encryption = db.Column(db.Boolean)
    ebs_creation_data = db.Column(db.DateTime)
    ebs_dettached_data = db.Column(db.DateTime)
    ebs_tag = db.Column(JSONB, index=True)

    def __init__(self, ebs_volume_id, ebs_aws_az, instance_id, snapshot_id,
             ebs_size, ebs_volume_type, ebs_iops, ebs_alarm_status, ebs_status,
             ebs_volume_status_ok, ebs_volume_encryption,
             ebs_creation_data, ebs_dettached_data, ebs_tag):

        self.ebs_volume_id = ebs_volume_id
        self.ebs_aws_az = ebs_aws_az
        self.instance_id = instance_id
        self.snapshot_id = snapshot_id
        self.ebs_size = ebs_size
        self.ebs_volume_type = ebs_volume_type
        self.ebs_iops = ebs_iops
        self.ebs_alarm_status = ebs_alarm_status
        self.ebs_status = ebs_status
        self.ebs_volume_status_ok = ebs_volume_status_ok
        self.ebs_volume_encryption = ebs_volume_encryption
        self.ebs_creation_data = ebs_creation_data
        self.ebs_dettached_data = ebs_dettached_data
        self.ebs_tag = ebs_tag

    def __repr__(self):
        return '<AWSEBS {} {}>'.format(self.ebs_volume_id, self.ebs_aws_az)

class AWSnapshot(db.Model):
    __tablename__ = 'aws_snap'

    snapshot_id = db.Column(db.String(30), primary_key=True)
    ebs_volume_id = db.Column(db.String(30), index=True)

    snap_size = db.Column(db.String(14), nullable=False)
    snap_status = db.Column(db.String(30))
    snap_progress = db.Column(db.String(30))
    snap_encryption = db.Column(db.Boolean)

    snap_description = db.Column(db.String(255))

    snap_started_data = db.Column(db.DateTime)
    snap_tag = db.Column(JSONB, index=True)

    def __init__(self, snapshot_id, ebs_volume_id, snap_size, snap_status,
                 snap_progress, snap_encryption, snap_description, snap_started_data, snap_tag):

        self.snapshot_id = snapshot_id
        self.ebs_volume_id = ebs_volume_id
        self.snap_size = snap_size
        self.snap_status = snap_status
        self.snap_progress = snap_progress
        self.snap_encryption = snap_encryption
        self.snap_description = snap_description
        self.snap_started_data = snap_started_data
        self.snap_tag = snap_tag


    def __repr__(self):
        return '<AWSnapshot {} {}>'.format(self.snapshot_id, self.snap_size)

class AWSPrices(db.Model):
    __tablename__ = 'aws_prices'

    instance_type = db.Column(db.String(30), primary_key=True)
    aws_region = db.Column(db.String(30), primary_key=True)
    price_date = db.Column(db.Date, index=True)
    price_ondemand_price_hrs_usd = db.Column(db.Float)
    price_ondemand_price_mth_usd = db.Column(db.Float)
    price_reserved_price_hsr_usd = db.Column(db.Float)
    price_reserved_price_mth_usd = db.Column(db.Float)
    price_reserved_price_offer_code = db.Column(db.String(255))
    price_spot_price_hsr_usd = db.Column(db.Float)
    price_spot_price_mth_usd = db.Column(db.Float)
    price_spot_offer_date = db.Column(db.DateTime)

    price_ondemand_reserved_saving = db.Column(db.Float)
    price_ondemand_reserved_saving_pct = db.Column(db.Float)

    price_ondemand_spot_saving = db.Column(db.Float)
    price_ondemand_spot_saving_pct = db.Column(db.Float)

    def __init__(self, instance_type, aws_region, price_date, price_ondemand_price_hrs_usd,
                 price_ondemand_price_mth_usd, price_reserved_price_hsr_usd,
                 price_reserved_price_mth_usd, price_reserved_price_offer_code, price_spot_price_hsr_usd,
                 price_spot_price_mth_usd, price_spot_offer_date,
                 price_ondemand_reserved_saving, price_ondemand_reserved_saving_pct,
                 price_ondemand_spot_saving, price_ondemand_spot_saving_pct):
        self.instance_type = instance_type
        self.aws_region = aws_region
        self.price_date = price_date

        self.price_ondemand_price_hrs_usd = price_ondemand_price_hrs_usd
        self.price_ondemand_price_mth_usd = price_ondemand_price_mth_usd

        self.price_reserved_price_hsr_usd = price_reserved_price_hsr_usd
        self.price_reserved_price_mth_usd = price_reserved_price_mth_usd
        self.price_reserved_price_offer_code = price_reserved_price_offer_code
        self.price_spot_price_hsr_usd = price_spot_price_hsr_usd
        self.price_spot_price_mth_usd = price_spot_price_mth_usd
        self.price_spot_offer_date = price_spot_offer_date

        self.price_ondemand_reserved_saving = price_ondemand_reserved_saving
        self.price_ondemand_reserved_saving_pct = price_ondemand_reserved_saving_pct

        self.price_ondemand_spot_saving = price_ondemand_spot_saving
        self.price_ondemand_spot_saving_pct = price_ondemand_spot_saving_pct

    def __repr__(self):
        return '<AWSPrices {} {} {}>'.format(self.instance_type, self.aws_region, self.price_offer_date)

class AWSInstancePrice(db.Model):
    #     __tablename__ = 'aws_instances_price'

    instance_price_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    instance_id = db.Column(db.String(30), nullable=False, index=True)
    aws_region = db.Column(db.String(30), nullable=False, index=True)
    instance_type = db.Column(db.String(30), nullable=False, index=True)
    instance_price_date = db.Column(db.Date, nullable=False)
    instance_running_price = db.Column(db.String(30), nullable=False, index=True)
    instance_hrs_price_usd = db.Column(db.Float)
    instance_mth_price_usd = db.Column(db.Float)
    instance_last_state = db.Column(db.String(30))
    workload_tag = db.Column(db.String(255), index=True, nullable=False) # Profile would be: test, qa, prod.


    def __init__(self, instance_id, aws_region, instance_type, instance_price_date, instance_running_price, instance_hrs_price_usd, instance_mth_price_usd, instance_last_state, workload_tag):
        self.instance_id = instance_id
        self.aws_region = aws_region
        self.instance_type = instance_type
        self.instance_price_date = instance_price_date
        self.instance_running_price = instance_running_price
        self.instance_hrs_price_usd = instance_hrs_price_usd
        self.instance_mth_price_usd = instance_mth_price_usd
        self.instance_last_state = instance_last_state
        self.workload_tag = workload_tag.upper()

    def __repr__(self):
        return '<AWSInstancePrice {} {} {}>'.format(self.instance_id, self.instance_type, self.aws_region)

class AWSInstanceWorkLoad(db.Model):
    __tablename__ = 'aws_instances_workload'

    workload_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    workload_date = db.Column(db.Date, nullable=False, index=True)
    instance_id = db.Column(db.String(19), nullable=False, index=True)
    instance_type = db.Column(db.String(255), nullable=False, index=True)
    aws_region = db.Column(db.String(19), nullable=False, index=True)

    cpu_percentage = db.Column(db.Float)
    available_memory_percentage = db.Column(db.Float)
    network_in_bytes_aggr = db.Column(db.Float)
    network_ou_bytes_aggr = db.Column(db.Float)

    cloudwatch_aggregation_type = db.Column(db.String(19))
    cloudwatch_aggregation_days = db.Column(db.Integer)
    cloudwatch_aggregation_period_from = db.Column(db.DateTime)
    cloudwatch_aggregation_period_to = db.Column(db.DateTime)
    cloudwatch_period_seconds = db.Column(db.Integer)

    #workload_criteria_cpu = db.Column(db.Float)
    #workload_criteria_memory = db.Column(db.Float)
    #workload_criteria_network = db.Column(db.Float)
    workload_criteria_check = db.Column(db.String(255))
    workload_low_utilization = db.Column(db.Boolean, index=True)
    workload_java_vm_tuning_suspect = db.Column(db.Boolean, index=True)
    workload_java_vm_criteria_check = db.Column(db.String(255))


    def __init__(self, workload_date,instance_id, aws_region, instance_type, cpu_percentage, available_memory_percentage, network_in_bytes_aggr,
                 network_ou_bytes_aggr, cloudwatch_aggregation_type, cloudwatch_aggregation_days, cloudwatch_aggregation_period_from,
                 cloudwatch_aggregation_period_to, cloudwatch_period_seconds, workload_criteria_check, workload_low_utilization,
                 workload_java_vm_tuning_suspect=False, workload_java_vm_criteria_check=None):
        self.workload_date = workload_date
        self.instance_id = instance_id
        self.aws_region = aws_region
        self.instance_type = instance_type
        self.cpu_percentage = cpu_percentage
        self.available_memory_percentage = available_memory_percentage
        self.network_in_bytes_aggr = network_in_bytes_aggr
        self.network_ou_bytes_aggr = network_ou_bytes_aggr
        self.cloudwatch_aggregation_type = cloudwatch_aggregation_type
        self.cloudwatch_aggregation_days = cloudwatch_aggregation_days
        self.cloudwatch_aggregation_period_from = cloudwatch_aggregation_period_from
        self.cloudwatch_aggregation_period_to = cloudwatch_aggregation_period_to
        self.cloudwatch_period_seconds = cloudwatch_period_seconds
        self.workload_criteria_check = workload_criteria_check
        self.workload_low_utilization = workload_low_utilization
        self.workload_java_vm_tuning_suspect = workload_java_vm_tuning_suspect
        self.workload_java_vm_criteria_check = workload_java_vm_criteria_check




    def __repr__(self):
        return '<AWSInstanceWorkLoad {} {}>'.format(self.instance_id, self.aws_region)

class AWSSummary(db.Model):
    __tablename__ = 'aws_summary_workload'

    summary_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    summary_date = db.Column(db.Date, nullable=False, index=True)
    total_ec2_ondemand =  db.Column(db.Integer)
    total_ec2_reserved =  db.Column(db.Integer)
    percentage_rsv_x_ond = db.Column(db.Integer)
    total_ec2_spot =  db.Column(db.Integer)
    total_instances_flagged_lowuse = db.Column(db.Integer)

    total_cost_ec2_ondemand_month =  db.Column(db.Float)
    total_cost_ec2_reserved_month = db.Column(db.Float)
    total_cost_ec2_spot_month = db.Column(db.Float)

    oportunity_save_money_reservation = db.Column(db.Float)
    opportunity_save_money_spot_asg = db.Column(db.Float)

    summary_tag = db.Column(db.String(255)) # Profile would be: test, qa, prod, qadev, anything util



    def __init__(self, summary_date,
                 total_ec2_ondemand,
                 total_ec2_reserved, percentage_rsv_x_ond, total_ec2_spot, total_instances_flagged_lowuse,
                 total_cost_ec2_ondemand_month, total_cost_ec2_reserved_month,total_cost_ec2_spot_month,
                 oportunity_save_money_reservation, oportunity_save_money_spot_asg, summary_tag):

        self.summary_date = summary_date
        self.total_ec2_ondemand =  total_ec2_ondemand
        self.total_ec2_reserved = total_ec2_reserved
        self.percentage_rsv_x_ond = percentage_rsv_x_ond
        self.total_ec2_spot = total_ec2_spot
        self.total_instances_flagged_lowuse = total_instances_flagged_lowuse
        self.total_cost_ec2_ondemand_month = total_cost_ec2_ondemand_month
        self.total_cost_ec2_reserved_month = total_cost_ec2_reserved_month
        self.total_cost_ec2_spot_month =  total_cost_ec2_spot_month
        self.opportunity_save_money_reservation = oportunity_save_money_reservation
        self.opportunity_save_money_spot_asg = oportunity_save_money_spot_asg
        self.summary_tag = summary_tag.upper()

    def __repr__(self):
        return '<AWSSummary {} {}>'.format(self.summary_id, self.summary_date)
