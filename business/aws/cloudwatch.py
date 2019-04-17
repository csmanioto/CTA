from business.aws import *
import logging.config


class AWSCloudWatch(AWSInterface):
    """
    Converse the total information returned from cloudwatch (Data Points rows) from a range of time to a single row
    """
    def __avg_cloudwatch_metrics(self, cloudwatch_datapoints):
        try:
            average = 0
            datapoints = cloudwatch_datapoints['Datapoints']
            if len(datapoints) > 0:
                sum_datapoint = 0
                for n in datapoints:
                    sum_datapoint = sum_datapoint + n['Average']
                average = sum_datapoint / len(datapoints)
                return average
            else:
                return 0
        except Exception as e:
            logging.debug("Error function __avg_cloudwatch_metrics {}".format(e))

    """
    Basic structure for querying on cloudwatch
    """
    def __query_building(self, namespace, metric_name, dimensions, time_start, time_end, period, statistics=['Average']):
        query = {
            "Namespace": namespace,
            "MetricName": metric_name,
            "Dimensions": dimensions,
            "StartTime": time_start,
            "EndTime": time_end,
            "Period": period,
            "Statistics": statistics
        }
        return query

    """
    Query on Cloudwatch informations about EC2 instance:
    Params: instanceID, aws region, name of metric, date time from, date time end, period 
    Exeample:
    cloudwatch_ec2('i-0b66427293bf597ca', 'us-east-2', 'CPUUtilization', datetime_start, datetime_end, 3600))
    return: JSON from cloudwatch api.
    """
    def cloudwatch_ec2(self, instance_id, region_id, metric_name, time_start, time_end, period):
        cloudwatch_connection = self.aws_connection.client('cloudwatch', region_name=region_id)
        dimensions = [{"Name": "InstanceId", "Value": instance_id}]
        statiscts = ['Average']
        try:
            query = self.__query_building("AWS/EC2",
                                          metric_name,
                                          dimensions,
                                          time_start,
                                          time_end,
                                          period,
                                          statiscts)
            logging.debug("Trying to query {} on Cloudwatch region {}".format(query, region_id))
            raw_result = cloudwatch_connection.get_metric_statistics(**query)
            if not raw_result:
                logging.warning("No cloudwatch information to ec2 instance {}:{}".format(instance_id, region_id))
            result = round(self.__avg_cloudwatch_metrics(raw_result),2)
            return result
        except Exception as e:
            logging.error("Error with query ec2 information on cloudwatch {}".format(e))
