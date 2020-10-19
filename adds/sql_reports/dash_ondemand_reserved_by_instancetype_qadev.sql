select instance_type,
       sum(ondemand_month) as ondemand_month,
       sum(spot_month) as spot_month,
       sum(reserved_month) as reserved_month,
       sum(total_saving_reserved) as total_saving_reserved,
       sum(saving_pct) as saving_pct
FROM
           (
           select
            ec2_ondemand.instance_type as instance_type,
            round(aws_prices.price_ondemand_price_mth_usd) as ondemand_month,
            round(aws_prices.price_spot_price_mth_usd) as spot_month,
            round(aws_prices.price_reserved_price_mth_usd) as reserved_month,
            round(aws_prices.price_ondemand_reserved_saving) as total_saving_reserved,
            round(aws_prices.price_ondemand_reserved_saving_pct) as saving_pct
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

where ec2.instance_running_price = 'OnDemand'
and ec2.instance_state = 'running'
and ec2.workload_tag = 'QADEV'
    ) as ec2_ondemand
on ec2_ondemand.instance_type = aws_prices.instance_type and
   ec2_ondemand.aws_region = aws_prices.aws_region
) as onxreserv
group by instance_type
