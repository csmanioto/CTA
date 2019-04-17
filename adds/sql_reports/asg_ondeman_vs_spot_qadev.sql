
select
       count(ec2_ondemand.instance_id) as ondemand_ec2,
       sum(aws_prices.price_ondemand_price_mth_usd) as ondemand_month,
       sum(aws_prices.price_spot_price_mth_usd) as spot_month,
       sum(aws_prices.price_ondemand_spot_saving) as total_saving_spot,
       concat(round(avg(aws_prices.price_ondemand_spot_saving_pct)), '%') as saving_pct


from aws_prices
INNER JOIN (
    select
    ec2_price.instance_id, ec2_price.instance_type,
                           ec2_price.aws_region from aws_instance_price as ec2_price
inner join aws_instances as ec2 ON
ec2_price.instance_id = ec2.instance_id and
ec2_price.aws_region = ec2.aws_region and
ec2_price.instance_type = ec2.instance_type and
ec2_price.workload_profile = ec2.workload_profile


where ec2.instance_running_price = 'OnDemand'
and ec2.workload_profile = 'QADEV'
and ec2.instance_auto_scaling_group = True
    ) as ec2_ondemand
on ec2_ondemand.instance_type = aws_prices.instance_type and
   ec2_ondemand.aws_region = aws_prices.aws_region
