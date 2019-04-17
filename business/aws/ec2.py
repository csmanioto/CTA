from business.aws import *
from business.aws import cloudwatch, price
from utils.ssh import *
from utils import linux_check
from utils import tools
from datetime import datetime, timedelta
#import json



class EC2(AWSInterface):
    logger = init_logger(__name__, testing_mode=config.DEBUG_MODE)
    settings_profile = None
    credential = None

    """
           Connect into the AWS and get all instance using criteria filter.

           :param str state: 'all' for all state(pending, running, stopped, etc) or individual state
           :param str tag_key: default None, tag name used on the instances
           :param str tag_name: default None, value of tag_key name
           :return:
               a list with dictionary containts two key: id and region with instance_id  and instance region.

    """

    def __get_instances_list(self, state='all', tag_key=None, tag_value=None):

        if "all" in state:
            state = ['pending', 'running', 'shutting-down', 'terminated', 'stopping', 'stopped']
        else:
            state = [state]

        filters = [{'Name': 'instance-state-name',
                    'Values': state}]

        if tag_key is not None and tag_value is not None:
            filters.append({'Name': 'tag:{}'.format(tag_key), 'Values': [tag_value]})

        instance_list = []
        for region_id in self.aws_get_regions_id():
            self.logger.info(
                "Getting instances list of region {} - {}".format(region_id, self.aws_regions_id_to_name(region_id)))
            ec2_connection = self.aws_connection.resource('ec2', region_name=region_id)
            instances = ec2_connection.instances.filter(Filters=filters)
            try:
                for instance in instances:
                    instance_list.append({"id": instance.id, "region": region_id})
            except Exception as e:
                self.logger.error("Error on get instances for region {} - {}".format(region_id,
                                                                                     self.aws_regions_id_to_name(
                                                                                         region_id)))
                self.logger.error("Error was {}".format(e))
                pass
        return instance_list

    def __check_instance_in_asg(self, instance_id, instance_region):
        try:
            asg_connection = self.aws_connection.client('autoscaling', region_name=instance_region)
            instances = asg_connection.describe_auto_scaling_instances(InstanceIds=[instance_id])
            instance_status = instances['AutoScalingInstances']
            if instance_status:
                asgname = instances['AutoScalingInstances'][0]['AutoScalingGroupName']
                logger.debug("Instance %s is in autoscale group {}".format(instance_id,instance_status[0]['AutoScalingGroupName']))
                return True, asgname
            return False, None
        except Exception as e:
            logger.error("Error on get ASG information - {} ".format(e))
            pass

    def __check_reserved_instances(self, aws_region, instance_type=None, availability_zone=None, state='active'):
        reserved = {}
        try:
            reserved_connection = self.aws_connection.client('ec2', region_name=aws_region)
            if instance_type is None:
                return reserved

            else:
                rs = reserved_connection.describe_reserved_instances(Filters=[
                    {'Name': 'instance-type',
                     'Values': [instance_type]
                     },
                     {'Name': 'state',
                     'Values': [state]
                     }])

                if 'ReservedInstances' in rs.keys():
                    if len(rs['ReservedInstances']) > 0:
                        reserved['scope'] = rs['ReservedInstances'][0]['Scope']
                        reserved['reservedprice'] = rs['ReservedInstances'][0]['UsagePrice']
                        reserved['offeringclass'] = rs['ReservedInstances'][0]['OfferingClass']
                        if 'Region' in rs['ReservedInstances'][0]['Scope']:
                            reserved['availabilityzone'] = aws_region
                        else:
                            reserved['availabilityzone'] = rs['ReservedInstances'][0]['AvailabilityZone']
                        reserved['reservedinstancesid'] = rs['ReservedInstances'][0]['ReservedInstancesId']
                return reserved
        except Exception as e:
            logger.error("Error on get reserved information: {}".format(e))

    def __describe_deeply_instance(self, instance_id, aws_region):
        BLACK_LIST_TAGS_LIST = ['elasticbeanstalk:', 'aws:']

        instance_details = {}
        instances = []
        nasg = None
        asg_name = None
        inasg = None
        launchtime = None
        sshkey = None
        private_ip_address = None
        private_dns_name = None
        vpcid = None
        subnetid = None
        tag_name = None
        tag_team = None
        tag_product = None
        tag_owner = None
        tag_env = None
        tags_string = None
        tags_json = None
        starttime = None

        aws_ec2_client = self.aws_connection.client('ec2', region_name=aws_region)
        try:
            rs = aws_ec2_client.describe_instances(InstanceIds=[instance_id])
            imageid = rs['Reservations'][0]['Instances'][0]['ImageId']
            instance_type = rs['Reservations'][0]['Instances'][0]['InstanceType']
            ebs_optimized = rs['Reservations'][0]['Instances'][0]['EbsOptimized']
            state = rs['Reservations'][0]['Instances'][0]['State']['Name']
            state_code = int(rs['Reservations'][0]['Instances'][0]['State']['Code'])

            # 0(pending), 16(running), 32(shutting - down), 48(terminated), 64(stopping), and 80(stopped).
            if state_code in [16, 64, 80]:
                private_ip_address = rs['Reservations'][0]['Instances'][0]['PrivateIpAddress']
                private_dns_name = rs['Reservations'][0]['Instances'][0]['PrivateDnsName']
                vpcid = rs['Reservations'][0]['Instances'][0]['VpcId']
                subnetid = rs['Reservations'][0]['Instances'][0]['SubnetId']

            availability_zone = rs['Reservations'][0]['Instances'][0]['Placement']['AvailabilityZone']
            ownerid = rs['Reservations'][0]['OwnerId']

            try:
                tags = rs['Reservations'][0]['Instances'][0]['Tags']
                instance_details = {}
                tags_string = None
                tag_list_json = []
                for tag in tags:
                    if not tools.check_string_in_list(tag['Key'], BLACK_LIST_TAGS_LIST):
                        if tags_string is None:
                            tags_string = "<{}:{}>".format(tag['Key'], tag['Value'])
                        tags_string = "{},<{}:{}>".format(tags_string, tag['Key'], tag['Value'])
                        tag_list_json.append({tag['Key']: tag['Value']})
                        # instance_details.update({'tag_{}'.format(tag['Key']): tag['Value']})

                tags_string = tags_string
                tags_json = tag_list_json
            except Exception as e:
                logger.exception("Error on capture tags - {}".format(e), exc_info=True)
                pass

            try:
                inasg, asg_name = self.__check_instance_in_asg(instance_id, aws_region)
            except Exception as e:
                logger.error("Error on get information about ASG of instance {}:{} - {}".format(instance_id, aws_region,e))
                pass

            try:
                instance_launchtime = rs['Reservations'][0]['Instances'][0]['LaunchTime']
                launchtime = tools.datetime_striso8601(instance_launchtime)
            except Exception as e:
                logger.error("Error to get launchtime of instance {} -  {} - {}".format(instance_id, aws_region, e))
                pass

            # If inasg = True then not exist KeyName.
            try:
                sshkey = rs['Reservations'][0]['Instances'][0]['KeyName']
            except Exception as e:
                logger.error("Error {}".format(e))
                pass

            reserved_info = self.__check_reserved_instances(aws_region, instance_type, availability_zone)
            reservationid = None
            if reserved_info:
                if aws_region == reserved_info['availabilityzone']:
                    reservationid = reserved_info['reservedinstancesid']

            #checking spot
            spot_instance_id = None
            if 'spot_instance_request_id' in rs['Reservations'][0]['Instances'][0]:
                spot_instance_id = rs['Reservations'][0]['Instances'][0]['spot_instance_request_id']

            instance_running_price_mode = "OnDemand"
            if reservationid:
                instance_running_price_mode = "Reserved"
            if spot_instance_id:
                instance_running_price_mode = "Spot"


            instance_details.update({
                "InstanceState": state,
                "SSHKey": sshkey,
                "InASG": inasg,
                "ASGName": asg_name,
                "Instance_type": instance_type,
                "instance_running_price" : instance_running_price_mode,
                "Instance_ebsoptimized": ebs_optimized,
                'InstanceIP': private_ip_address,
                "InstanceHostName": private_dns_name,
                "Instance_vpc_id": vpcid,
                "instance_subnet_id": subnetid,
                "instance_availabilityzone": availability_zone,
                "instance_ami": imageid,
                "instance_account_id": ownerid,
                "instance_reservation_id": reservationid,
                "spot_instance_request_id": spot_instance_id,
                "instance_launch_time": launchtime,
                "tags_string": tags_string,
                "tags_json": tags_json,
            })
        except Exception as e:
            logger.error("Error on get describe instance {}".format(e))
        return instance_details

    def __get_instance_metrics(self, instance_id=None, aws_region=None, aggregation_type='days', aggregation=30, period=3600, instance_details=None):
        cw = cloudwatch.AWSCloudWatch(self.settings_profile)

        if not instance_details:
            return None

        instance_ssh_details = {
            'srv_host': instance_details['InstanceHostName'],
            'srv_ip': instance_details['InstanceIP'],
            'srv_user': None,
            'srv_key_file_name': "{}.pem".format(instance_details['SSHKey']),
            'instance_id': instance_id,
            'aws_region': aws_region,
            'single_line': True,
        }

        if 'days' in aggregation_type:
            starttime = datetime.today() - timedelta(days=int(aggregation))
        if 'minutes' in aggregation_type:
            starttime = datetime.today() - timedelta(minutes=int(aggregation))

        endtime = datetime.today()

        #cloud watch netrics
        cloudw_cpu = cw.cloudwatch_ec2(instance_id,   aws_region, 'CPUUtilization', starttime, endtime, period)
        cloudw_diskr = cw.cloudwatch_ec2(instance_id, aws_region, 'DiskReadOps', starttime, endtime, period)
        cloudw_diskw = cw.cloudwatch_ec2(instance_id, aws_region, 'DiskWriteOps', starttime, endtime, period)
        cloudw_netin = cw.cloudwatch_ec2(instance_id, aws_region, 'NetworkIn', starttime, endtime, period)
        cloudw_netou = cw.cloudwatch_ec2(instance_id, aws_region, 'NetworkOut', starttime, endtime, period)


        # intrusive ssh linux_details

        ssh_info = {'available_kbytes_str': 0, 'available_kbytes': 0, 'avaliable_perc': 0, 'kernel': "Undefined",
                    'distro': "Undefined"}

        if instance_details['InstanceState'] == "running":
            linux_details = linux_check.get_os_helthcheck(instance_ssh_details)
            if linux_details:
                ssh_info = linux_details

        log_message = "instande_id: {} - {} - cpu {}% - memory free {}% - network in {} bytes - network out {} bytes - disk iop read {} - disk iop write - avg in {} days "
        logger.debug(log_message.format(instance_id, aws_region, cloudw_cpu, ssh_info, cloudw_netin, cloudw_netou, cloudw_diskr, cloudw_diskw, aggregation))

        dict_instance_metric = {
            'cloudw_cpu': cloudw_cpu,
            'cloudw_netin': cloudw_netin,
            'cloudw_netou': cloudw_netou,
            'cloudw_aggregation_type': aggregation_type,
            'cloudw_aggregation_days': aggregation,
            'cloudw_aggregation_period_from': starttime,
            'cloudw_aggregation_period_to': endtime,
            'cloudw_period_seconds': period,
            'network_io_mb': round((cloudw_netin + cloudw_netou) / (1024 ** 2),2),
            'avaliable_ram_kb': ssh_info['available_kbytes'],
            'avaliable_ram_pct': ssh_info['avaliable_perc'],
            'kernel_version': ssh_info['kernel'],
            'Linux_distro': ssh_info['distro'],
        }
        return dict_instance_metric


    def __check_low_utilization_suspected(self, instance_metrics, max_cpu=50, max_mem_available_pct=50, network=150):
        # finding the low utilization instances using the criteria...
        low_network = False
        low_memory = False
        low_cpu = False
        instance_underused = False
        cpu_info = None
        network_info = None
        ram_info = None

        cpu = instance_metrics['cloudw_cpu']
        netin = instance_metrics['cloudw_netin']
        netout = instance_metrics['cloudw_netou']
        ram_free_pcpt = instance_metrics['avaliable_ram_pct']

        if cpu <= max_cpu:
            cpu_info = "CPU: the avg cpu is {}% lower than the minimum criteria: {}%".format((max_cpu - cpu), max_cpu)
            logger.debug(cpu_info)
            low_cpu = True

        try:
            network_bytes = int(network) * (1024 ** 2)
            if netin <= network_bytes and netout <= network_bytes:
                netio_mb = ((netin + netout) / (1024 ** 2))
                net_pect = round((network / netio_mb),2)
                network_info = "NETWORK: The avg network io is {}% lower than the minimum criteria: {}".format(net_pect, network)
                logger.debug(network_info)
                low_network = True
        except Exception as e:
            logger.error("Error {}".format(e))
            pass

        try:
            if ram_free_pcpt == 0.0:
                low_memory = True
            elif ram_free_pcpt >= max_mem_available_pct:
                ram_info = "RAM: the avg memory ram use is {}% lower than the minimum criteria: {}%".format((ram_free_pcpt - max_mem_available_pct), max_mem_available_pct)
                logger.debug(ram_info)
                low_memory = True
        except Exception as e:
            logger.error("Error {}".format(e))
            pass


        # IF CPU <=50% and NetworkIO <= 500Mb &FreeMemory >= 50%
        if low_cpu and low_memory and low_network:
            instance_underused = True

        criteria = "{} | {} | {}".format(tools.str_none_to_empty(cpu_info),
                                     tools.str_none_to_empty(network_info),
                                     tools.str_none_to_empty(ram_info))
        logger.debug(criteria)
        return instance_underused, criteria


    #  2019-04-01 17:13:35,711 - utils.ssh - __aggregation_details - DEBUG - Getting data from instance i-047870d8f758e7894:us-east-2
    def __aggregation_details(self, instance_id, aws_region):

        aws_price = price.AWSPrices(self.settings_profile)

        logger.debug("Getting data from instance {}:{}".format(instance_id, aws_region))
        instance_details = self.__describe_deeply_instance(instance_id=instance_id, aws_region=aws_region)
        instance_metric = self.__get_instance_metrics(instance_id=instance_id, aws_region=aws_region,
                                                          aggregation=30, period=3600,
                                                          instance_details=instance_details)
        try:
            instance_type = instance_details['Instance_type']
            instance_prices = aws_price.get_ec2_prices(instance_type=instance_type, aws_region=aws_region)
        except Exception as e:
            logger.error("No data available for instance {} - {}".format(instance_id,e))
            return None


        running_price = 0.0
        if instance_details['instance_running_price'] == "OnDemand":
            running_price = instance_prices['ondemand_price']

        if instance_details['instance_running_price'] == "Reserved":
            running_price = instance_prices['reserved_price']

        if instance_details['instance_running_price'] == "Spot":
            running_price = instance_prices['spot_price']

        # It's a low utilization suspected ?
        # Memory perc <= 50%
        # CPU utilization <= 50%
        underused = self.__check_low_utilization_suspected(instance_metric)

        pricing_offers = {"pricing_offers": instance_prices}

        low_check = {'low_utilizaion_check': underused[1]}
        metadata = {
            "instance_id": instance_id,
            "aws_region": aws_region,
            "aws_region_name":  self.aws_regions_id_to_name(aws_region),
            "aws_region_coordinate": self.aws_get_geo_region(aws_region),
            "low_utilization_suspected": underused[0],
            "instance_running_price": instance_details['instance_running_price'],
            "running_price": running_price,
            "deep_details": {**instance_details, **instance_metric, **low_check, **pricing_offers},

        }
        return metadata


    def get_ec2_details(self, instance_id=None, aws_region=None, db_conn=None):
        from database.write import WriteData
        workload_profile = self.settings_profile['profile']

        db = WriteData(db_conn, workload_profile)

        all_instances = []

        #Doing for single instance
        if instance_id and aws_region:
            details = self.__aggregation_details(instance_id, aws_region)
            if details:
                #if config.DEBUG_MODE:
                #    with open('instances_details.json', 'a') as file:
                #        json.dump(details, file)
                if db_conn:
                    db.save(details)
            all_instances.append(details)

        # Doing for all instances...
        else:
            logger.debug("Getting details over whole AWS's account")
            for instance_information in self.__get_instances_list():
                instance_id = instance_information['id']
                aws_region = instance_information['region']
                details = self.__aggregation_details(instance_id, aws_region)
                if details:
                    # if config.DEBUG_MODE:
                    #    with open('instances_details.json', 'a') as file:
                    #        json.dump(details, file)
                    if db_conn:
                        db.save(details)
                        #db.save_instance(details)
                        #db.save_price(details)
                        #db.save_instance_price(details)
                        #db.save_instance_workload(details)

                    all_instances.append(details)

        return all_instances



