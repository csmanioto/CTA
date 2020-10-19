select
        ec2.instance_auto_scaling_group_name as autoscaling_group_name,
        ec2.aws_region,
        sum(price.price_spot_price_mth_usd) as spot_price_monthly,
        sum(price.price_ondemand_price_mth_usd) as ondemmand_price_monthly,
        sum(price.price_ondemand_spot_saving) as saving_monthly,
        ec2_workload.workload_date as workload_date
from aws_instances_workload as ec2_workload
    inner join aws_prices price on
    ec2_workload.instance_type = price.instance_type and
    ec2_workload.aws_region = price.aws_region 
    inner join aws_instances as ec2 on 
    ec2_workload.instance_id = ec2.instance_id  

where ec2.instance_auto_scaling_group = true
and ec2.workload_tag = 'QADEV'
and ec2_workload.workload_date = (select max(workload_date) from aws_instances_workload limit 1)
group by ec2.instance_auto_scaling_group_name, ec2.aws_region, ec2_workload.workload_date