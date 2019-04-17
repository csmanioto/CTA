select ec2_total_prices.total_instances,
       undersed_prices.underused,
       undersed_prices.cpu,
       undersed_prices.memory,
       undersed_prices.potential_waste_money_month,
       ec2_total_prices.total_ec2_money_month
from (
     select
            count(instance_id) as total_instances,
            round(sum(aws_instance_price.instance_mth_price_usd)) as total_ec2_money_month
        from aws_instance_price
         )
as ec2_total_prices,
     (
         select count(ec2_work.workload_date)                                      as underused,
                concat(round(avg(ec2_work.cpu_percentage)), '% used')              as cpu,
                concat(round(avg(ec2_work.available_memory_percentage)), '% used') as memory,
                round(sum(ec2_price.instance_mth_price_usd))                       as potential_waste_money_month

         from aws_instances_workload as ec2_work
                  inner join aws_instance_price ec2_price on
                 ec2_work.instance_id = ec2_price.instance_id and
                 ec2_work.aws_region = ec2_price.aws_region
         where ec2_work.workload_low_utilization = True
         and ec2_price.workload_profile = 'QADEV'
     )
as undersed_prices