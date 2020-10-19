select
       COALESCE(itt.total_instances, 0) total_instances,
       COALESCE(irn.total_instances, 0) total_running,
       COALESCE(istp.total_instances, 0) total_stopped,
       COALESCE(itm.total_instances, 0) total_terminated,
       irn.instance_state_date as scan_date
FROM
    (select count(instance_state)  as total_instances,
            instance_state_date::date as instance_state_date
     from aws_instances
      where instance_state = 'running'
      and workload_tag = 'QADEV'
      group by instance_state_date::date
     ) as irn
LEFT JOIN
    (select count(instance_state) as total_instances,
             instance_state_date::date as instance_state_date
     from aws_instances
     where instance_state = 'stopped'
     and workload_tag = 'QADEV'
     group by instance_state_date::date
    ) as istp
ON irn.instance_state_date = istp.instance_state_date

LEFT OUTER JOIN
    (select COALESCE(count(instance_id), 0) as total_instances,
            instance_state_date::date as instance_state_date
     from aws_instances
       where instance_state = 'terminated'
       and workload_tag = 'QADEV'
       group by instance_state_date::date
    ) as itm
ON irn.instance_state_date = itm.instance_state_date

LEFT OUTER JOIN
        (select COALESCE(count(instance_id), 0) as total_instances,
            instance_state_date::date as instance_state_date
     from aws_instances
        where workload_tag = 'QADEV'
        and instance_state <> 'terminated'
       group by instance_state_date::date
    ) as itt
ON irn.instance_state_date = itt.instance_state_date
order by scan_date desc