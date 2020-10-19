select count(instance_state),
       aws_region,
       aws_region_name,
       aws_region_coordinate_lat,
       aws_region_coordinate_log
from aws_instances
where workload_tag = 'QADEV'
--and instance_state = "running"
group by aws_region, aws_region_name, aws_region_coordinate_lat, aws_region_coordinate_log
