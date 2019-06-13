 SELECT   (select count(1) as total_instances
           from aws_instances_workload as wk
           where wk.workload_date = (select max(workload_date) from aws_instances_workload limit 1)
          ) as total_instances,
          count(1) as underused,
          concat(round(avg(cpu_percentage)), '% used')              as cpu,
          concat(round(avg(available_memory_percentage)), '% free') as memory_free
         from aws_instances_workload as wk
             inner join aws_instances as ec2 on
             ec2.instance_id = wk.instance_id
         where workload_low_utilization = True
           and ec2.workload_tag = 'QADEV'
           and wk.workload_date = (select max(workload_date) from aws_instances_workload limit 1)