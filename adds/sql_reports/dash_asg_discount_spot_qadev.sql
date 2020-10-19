select * from
(

select count(aws_prices.instance_type) as instances_number,
       aws_prices.instance_type,
       aws_prices.aws_region,
       aws_prices.price_ondemand_price_mth_usd as ondemmand_price_monthly,
       aws_prices.price_spot_price_mth_usd as spot_price_monthly,
       aws_prices.price_ondemand_reserved_saving as reserved_price_monthly,
       aws_prices.price_ondemand_spot_saving as discount_spot_monthly,
       ec2_workload.workload_date

from aws_prices
INNER JOIN (
    select
    ec2_price.instance_id, ec2_price.instance_type,
                           ec2_price.aws_region from aws_instance_price as ec2_price
inner join aws_instances as ec2 ON
ec2_price.instance_id = ec2.instance_id and
ec2_price.aws_region = ec2.aws_region and
ec2_price.instance_type = ec2.instance_type and
ec2_price.workload_tag = ec2.workload_tag


where ec2.instance_auto_scaling_group = true
and ec2.instance_running_price = 'OnDemand'
and ec2.workload_tag = 'QADEV'
    ) as asg
on asg.instance_type = aws_prices.instance_type and
   asg.aws_region = aws_prices.aws_region
inner join aws_instances_workload as ec2_workload on
ec2_workload.instance_id = asg.instance_id

where ec2_workload.workload_date = (select max(workload_date) from aws_instances_workload limit 1)

group by aws_prices.instance_type,
         aws_prices.aws_region,
         aws_prices.price_ondemand_price_mth_usd,
         aws_prices.price_ondemand_reserved_saving,
         aws_prices.price_spot_price_mth_usd,
         aws_prices.price_ondemand_spot_saving,
         ec2_workload.workload_date
) as fit_spot
where instances_number > 1