select instance_type,
       aws_region,
       aws_region_name,
       instance_linux_distribution,
       instance_linux_kernel_version
from aws_instances
where workload_tag = 'QADEV'
and instance_linux_kernel_version is not null
group by instance_type,
         aws_region,
         aws_region_name,
         instance_linux_distribution,
         instance_linux_kernel_version
