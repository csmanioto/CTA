-- -------------
-- AWS ASG INSTANCES AND PRICE.
-- PARAM: WORLOAD_TAG, AWS TAG KEY, AWS TAG VALUE
-- EX:
-- Getting data from QA ENV and a specific team:
-- select * from faws_asg_instances_prices('QADEV', 'OwningTeam', 'TENG04');
-- Getting data from QA ENV:
-- select * from faws_asg_instances_prices('QADEV', null, null);
-- -------------
CREATE OR REPLACE FUNCTION faws_asg_instances_prices(vWorkload_tag varchar,
                                                    vAws_tag_key varchar,
                                                    vAws_tag_value varchar)
RETURNS SETOF type_aws_asg_instances_aws_prices language plpgsql as
$$
declare JSON_WHERE varchar;
BEGIN

                IF vAws_tag_key is not null then

                    JSON_WHERE = CAST(CONCAT('[{"',vAws_tag_key, '": "',  vAws_tag_value, '"}]') as JSON);
                    RAISE NOTICE 'JSON QUERY  (%)', JSON_WHERE;

                    RETURN QUERY
                    select * from
                    (
                            select count(aws_prices.instance_type)::bigint as instances_number,
                               aws_prices.instance_type::varchar,
                               aws_prices.aws_region::varchar,
                               ec2.instance_auto_scaling_group_name::varchar,
                               sum(aws_prices.price_ondemand_price_mth_usd)::float as ondemmand_price_monthly,
                               sum(aws_prices.price_reserved_price_mth_usd)::float as reserved_price_monthly,
                               sum(aws_prices.price_ondemand_reserved_saving)::float as discount_reserved_monthly,
                               sum(aws_prices.price_spot_price_mth_usd)::float as spot_price_monthly,
                               sum(aws_prices.price_ondemand_spot_saving)::float as discount_spot_monthly,
                               ec2_workload.workload_date
                        from aws_prices
                        INNER JOIN (
                            select
                                ec2_price.instance_id, ec2_price.instance_type,
                                ec2_price.aws_region from aws_instance_price as ec2_price
                                inner join
                                    aws_instances as ec2 ON
                                    ec2_price.instance_id = ec2.instance_id and
                                    ec2_price.aws_region = ec2.aws_region and
                                    ec2_price.instance_type = ec2.instance_type and
                                    ec2_price.workload_tag = ec2.workload_tag

                                where ec2.instance_auto_scaling_group = true
                                and ec2.instance_running_price = 'OnDemand'
                                and ec2.workload_tag = vWorkload_tag
                                and ec2.instance_tags_json @> JSON_WHERE::jsonb
                        ) as asg on
                            asg.instance_type = aws_prices.instance_type and
                            asg.aws_region = aws_prices.aws_region
                        INNER JOIN
                            aws_instances_workload as ec2_workload on
                            ec2_workload.instance_id = asg.instance_id
                        INNER JOIN aws_instances as ec2 on
                        ec2_workload.instance_id  = ec2.instance_id
                        where ec2_workload.workload_date = (select max(workload_date) from aws_instances_workload limit 1)
                        group by aws_prices.instance_type,
                                 aws_prices.aws_region,
                                 ec2.instance_auto_scaling_group_name,
                                 aws_prices.price_ondemand_price_mth_usd,
                                 aws_prices.price_ondemand_reserved_saving,
                                 aws_prices.price_spot_price_mth_usd,
                                 aws_prices.price_ondemand_spot_saving,
                                 ec2_workload.workload_date
                        ) as fit_spot
                    where instances_number > 1;
            ELSE
                 RETURN QUERY
                    select * from
                    (
                            select count(aws_prices.instance_type)::bigint as instances_number,
                               aws_prices.instance_type::varchar,
                               aws_prices.aws_region::varchar,
                               ec2.instance_auto_scaling_group_name::varchar,
                               sum(aws_prices.price_ondemand_price_mth_usd)::float as ondemmand_price_monthly,
                               sum(aws_prices.price_reserved_price_mth_usd)::float as reserved_price_monthly,
                               sum(aws_prices.price_ondemand_reserved_saving)::float as discount_reserved_monthly,
                               sum(aws_prices.price_spot_price_mth_usd)::float as spot_price_monthly,
                               sum(aws_prices.price_ondemand_spot_saving)::float as discount_spot_monthly,
                               ec2_workload.workload_date
                        from aws_prices
                        INNER JOIN (
                            select
                                ec2_price.instance_id, ec2_price.instance_type,
                                ec2_price.aws_region from aws_instance_price as ec2_price
                                inner join
                                    aws_instances as ec2 ON
                                    ec2_price.instance_id = ec2.instance_id and
                                    ec2_price.aws_region = ec2.aws_region and
                                    ec2_price.instance_type = ec2.instance_type and
                                    ec2_price.workload_tag = ec2.workload_tag

                                where ec2.instance_auto_scaling_group = true
                                and ec2.instance_running_price = 'OnDemand'
                                and ec2.workload_tag = vWorkload_tag
                        ) as asg on
                            asg.instance_type = aws_prices.instance_type and
                            asg.aws_region = aws_prices.aws_region
                        INNER JOIN
                            aws_instances_workload as ec2_workload on
                            ec2_workload.instance_id = asg.instance_id
                        INNER JOIN aws_instances as ec2 on
                        ec2_workload.instance_id  = ec2.instance_id
                        where ec2_workload.workload_date = (select max(workload_date) from aws_instances_workload limit 1)
                        group by aws_prices.instance_type,
                                 aws_prices.aws_region,
                                 ec2.instance_auto_scaling_group_name,
                                 aws_prices.price_ondemand_price_mth_usd,
                                 aws_prices.price_ondemand_reserved_saving,
                                 aws_prices.price_spot_price_mth_usd,
                                 aws_prices.price_ondemand_spot_saving,
                                 ec2_workload.workload_date
                        ) as fit_spot
                    where instances_number > 1;
            END IF;



END;
$$;


-- -----------------------------
-- Aggroup instances by status and regions.
-- -----------------------------

CREATE OR REPLACE FUNCTION faws_regions_latlong(vWorkload_tag varchar,
                                                    vAws_tag_key varchar,
                                                    vAws_tag_value varchar)
RETURNS SETOF type_aws_lat_long language plpgsql
AS $$
declare JSON_WHERE varchar;
BEGIN
                IF vAws_tag_key is not null then

                    JSON_WHERE = CAST(CONCAT('[{"',vAws_tag_key, '": "',  vAws_tag_value, '"}]') as JSON);
                    RAISE NOTICE 'JSON QUERY  (%)', JSON_WHERE;

                    RETURN QUERY
                    SELECT  count(instance_state) as number_instances,
                                aws_region,
                                aws_region_name,
                                aws_region_coordinate_lat,
                                aws_region_coordinate_log
                        FROM aws_instances
                        WHERE workload_tag = vWorkload_tag
                        AND instance_tags_json @> JSON_WHERE::jsonb
                        group by aws_region,
                                 aws_region_name,
                                 aws_region_coordinate_lat,
                                 aws_region_coordinate_log;
                ELSE
                   RETURN QUERY
                    SELECT  count(instance_state) as number_instances,
                                aws_region,
                                aws_region_name,
                                aws_region_coordinate_lat,
                                aws_region_coordinate_log
                        FROM aws_instances
                        WHERE workload_tag = vWorkload_tag
                        group by aws_region,
                                 aws_region_name,
                                 aws_region_coordinate_lat,
                                 aws_region_coordinate_log;
                END IF ;

END;
$$;

----------
--  faws_ondemand_reservation
---------

create or replace function faws_ondemand_reservation(vworkload_tag character varying, vaws_tag_key character varying, vaws_tag_value character varying)
returns SETOF type_aws_ondemand_reservation language plpgsql as
$$
declare JSON_WHERE varchar;
BEGIN
                IF vAws_tag_key is not null then

                    JSON_WHERE = CAST(CONCAT('[{"',vAws_tag_key, '": "',  vAws_tag_value, '"}]') as JSON);
                    RAISE NOTICE 'JSON QUERY  (%)', JSON_WHERE;

                    RETURN QUERY
                        select
                            sum(aws_prices.price_ondemand_price_mth_usd) as ondemand_month,
                            sum(aws_prices.price_reserved_price_mth_usd) as reserved_month,
                            sum(aws_prices.price_ondemand_reserved_saving) as potential_saving_reserved,
                            avg(aws_prices.price_ondemand_reserved_saving_pct) as saving_pct
                            from aws_prices
                            INNER JOIN
                            (
                                select
                                    ec2_price.instance_id, ec2_price.instance_type,
                                    ec2_price.aws_region from aws_instance_price as ec2_price
                                    inner join aws_instances as ec2 ON
                                        ec2_price.instance_id = ec2.instance_id and
                                        ec2_price.aws_region = ec2.aws_region and
                                        ec2_price.instance_type = ec2.instance_type and
                                        ec2_price.workload_tag = ec2.workload_tag

                                where ec2.instance_running_price = 'OnDemand'
                                  and ec2.workload_tag = vworkload_tag
                                  and instance_tags_json @> JSON_WHERE::jsonb
                            ) as ec2_ondemand
                            on ec2_ondemand.instance_type = aws_prices.instance_type and
                               ec2_ondemand.aws_region = aws_prices.aws_region;
                ELSE
                        RETURN  QUERY
                        select
                            sum(aws_prices.price_ondemand_price_mth_usd) as ondemand_month,
                            sum(aws_prices.price_reserved_price_mth_usd) as reserved_month,
                            sum(aws_prices.price_ondemand_reserved_saving) as potential_saving_reserved,
                            avg(aws_prices.price_ondemand_reserved_saving_pct) as saving_pct
                            from aws_prices
                            INNER JOIN
                            (
                                select
                                    ec2_price.instance_id, ec2_price.instance_type,
                                    ec2_price.aws_region from aws_instance_price as ec2_price
                                    inner join aws_instances as ec2 ON
                                        ec2_price.instance_id = ec2.instance_id and
                                        ec2_price.aws_region = ec2.aws_region and
                                        ec2_price.instance_type = ec2.instance_type and
                                        ec2_price.workload_tag = ec2.workload_tag

                                where ec2.instance_running_price = 'OnDemand'
                                  and ec2.workload_tag = vworkload_tag
                            ) as ec2_ondemand
                            on ec2_ondemand.instance_type = aws_prices.instance_type and
                               ec2_ondemand.aws_region = aws_prices.aws_region;
                END IF ;
END;
$$;

---
--
---

create or replace function faws_ondemand_reservation_by_instance(vworkload_tag character varying, vaws_tag_key character varying, vaws_tag_value character varying) returns SETOF type_aws_ondemand_reserved_by_instance
    language plpgsql
as
$$
declare JSON_WHERE varchar;
BEGIN
                IF vAws_tag_key is not null then

                    JSON_WHERE = CAST(CONCAT('[{"',vAws_tag_key, '": "',  vAws_tag_value, '"}]') as JSON);
                    RAISE NOTICE 'JSON QUERY  (%)', JSON_WHERE;

                    RETURN QUERY
                            SELECT instance_type,
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
                                        SELECT
                                        ec2_price.instance_id, ec2_price.instance_type,
                                        ec2_price.aws_region from aws_instance_price as ec2_price
                                        inner join aws_instances as ec2 ON
                                            ec2_price.instance_id = ec2.instance_id and
                                            ec2_price.aws_region = ec2.aws_region and
                                            ec2_price.instance_type = ec2.instance_type and
                                            ec2_price.workload_tag = ec2.workload_tag
                                        where ec2.instance_running_price = 'OnDemand'
                                            and ec2.instance_state = 'running'
                                            and ec2.workload_tag = vworkload_tag
                                            and ec2.instance_tags_json @> JSON_WHERE::jsonb
                            ) as ec2_ondemand
                            on ec2_ondemand.instance_type = aws_prices.instance_type and
                               ec2_ondemand.aws_region = aws_prices.aws_region
                            ) as onxreserv
                            group by instance_type;
                    ELSE
                           RETURN QUERY
                            SELECT instance_type,
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
                                        SELECT
                                        ec2_price.instance_id, ec2_price.instance_type,
                                        ec2_price.aws_region from aws_instance_price as ec2_price
                                        inner join aws_instances as ec2 ON
                                            ec2_price.instance_id = ec2.instance_id and
                                            ec2_price.aws_region = ec2.aws_region and
                                            ec2_price.instance_type = ec2.instance_type and
                                            ec2_price.workload_tag = ec2.workload_tag
                                        where ec2.instance_running_price = 'OnDemand'
                                            and ec2.instance_state = 'running'
                                            and ec2.workload_tag = vworkload_tag
                            ) as ec2_ondemand
                            on ec2_ondemand.instance_type = aws_prices.instance_type and
                               ec2_ondemand.aws_region = aws_prices.aws_region
                            ) as onxreserv
                            group by instance_type;

                    END IF;

END;
$$;

--------
--
--------
create or replace function faws_total_ec2(vworkload_tag character varying, vaws_tag_key character varying, vaws_tag_value character varying) returns SETOF type_aws_total_ec2
    language plpgsql
as
$$
declare JSON_WHERE varchar;
BEGIN
            IF vAws_tag_key is not null then

                    JSON_WHERE = CAST(CONCAT('[{"',vAws_tag_key, '": "',  vAws_tag_value, '"}]') as JSON);
                    RAISE NOTICE 'JSON QUERY  (%)', JSON_WHERE;

                RETURN QUERY

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
                      and workload_tag = vworkload_tag
                      and instance_tags_json @> JSON_WHERE::jsonb
                      group by instance_state_date::date
                     ) as irn
                LEFT JOIN
                    (select count(instance_state) as total_instances,
                             instance_state_date::date as instance_state_date
                     from aws_instances
                     where instance_state = 'stopped'
                     and workload_tag = vworkload_tag
                     and instance_tags_json @> JSON_WHERE::jsonb
                     group by instance_state_date::date
                    ) as istp
                ON irn.instance_state_date = istp.instance_state_date

                LEFT OUTER JOIN
                    (select COALESCE(count(instance_id), 0) as total_instances,
                            instance_state_date::date as instance_state_date
                     from aws_instances
                       where instance_state = 'terminated'
                       and workload_tag = vworkload_tag
                       and instance_tags_json @> JSON_WHERE::jsonb
                       group by instance_state_date::date
                    ) as itm
                ON irn.instance_state_date = itm.instance_state_date

                LEFT OUTER JOIN
                        (select COALESCE(count(instance_id), 0) as total_instances,
                            instance_state_date::date as instance_state_date
                     from aws_instances
                        where workload_tag = vworkload_tag
                        and instance_tags_json @> JSON_WHERE::jsonb
                        and instance_state <> 'terminated'
                       group by instance_state_date::date
                    ) as itt
                ON irn.instance_state_date = itt.instance_state_date
                order by scan_date desc;
        ELSE
             RETURN QUERY
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
                      and workload_tag = vworkload_tag
                      group by instance_state_date::date
                     ) as irn
                LEFT JOIN
                    (select count(instance_state) as total_instances,
                             instance_state_date::date as instance_state_date
                     from aws_instances
                     where instance_state = 'stopped'
                     and workload_tag = vworkload_tag
                     group by instance_state_date::date
                    ) as istp
                ON irn.instance_state_date = istp.instance_state_date

                LEFT OUTER JOIN
                    (select COALESCE(count(instance_id), 0) as total_instances,
                            instance_state_date::date as instance_state_date
                     from aws_instances
                       where instance_state = 'terminated'
                       and workload_tag = vworkload_tag
                       group by instance_state_date::date
                    ) as itm
                ON irn.instance_state_date = itm.instance_state_date

                LEFT OUTER JOIN
                        (select COALESCE(count(instance_id), 0) as total_instances,
                            instance_state_date::date as instance_state_date
                     from aws_instances
                        where workload_tag = vworkload_tag
                        and instance_state <> 'terminated'
                       group by instance_state_date::date
                    ) as itt
                ON irn.instance_state_date = itt.instance_state_date
                order by scan_date desc;
        END IF;

END;
$$;


create or replace function faws_ondemand_reserved_underuser(vworkload_tag character varying, vaws_tag_key character varying,
                               vaws_tag_value character varying) returns SETOF type_ondemand_reserved_underuser
    language plpgsql
as
$$
declare
    JSON_WHERE varchar;
BEGIN
    IF vAws_tag_key is not null then
        JSON_WHERE = CAST(CONCAT('[{"', vAws_tag_key, '": "', vAws_tag_value, '"}]') as JSON);
        RAISE NOTICE 'JSON QUERY  (%)', JSON_WHERE;

        RETURN QUERY
            select ec2_total_prices.total_instances::bigint,
                   undersed_prices.underused::bigint,
                   undersed_prices.cpu::varchar,
                   undersed_prices.memory::varchar,
                   undersed_prices.potential_waste_money_month::float,
                   ec2_total_prices.total_ec2_money_month::float,
                   (ec2_total_prices.total_ec2_money_month - undersed_prices.potential_waste_money_month)::float as gap
            from (
                     select count(ec2_price.instance_id)                 as total_instances,
                            round(sum(ec2_price.instance_mth_price_usd)) as total_ec2_money_month
                     from aws_instance_price as ec2_price
                              inner join aws_instances_workload as ec2_workload
                                         on ec2_price.instance_id = ec2_workload.instance_id
                              inner join aws_instances as ec2
                                         on ec2.instance_id = ec2_workload.instance_id
                     where ec2_workload.workload_date = (select max(workload_date) from aws_instances_workload limit 1)
                       and ec2.instance_tags_json @> JSON_WHERE::jsonb
                 )
                     as ec2_total_prices,
                 (
                     select count(ec2_work.workload_date)                                 as underused,
                            concat(round(avg(ec2_work.cpu_percentage)), '% avg used')::varchar              as cpu,
                            concat(round(avg(ec2_work.available_memory_percentage)), '% avg free')::varchar as memory,
                            round(sum(ec2_price.instance_mth_price_usd))                  as potential_waste_money_month

                     from aws_instances_workload as ec2_work
                              inner join aws_instance_price ec2_price on
                             ec2_work.instance_id = ec2_price.instance_id and
                             ec2_work.aws_region = ec2_price.aws_region
                              inner join aws_instances as ec2 on
                         ec2.instance_id = ec2_work.instance_id
                     where ec2_work.workload_low_utilization = True
                       and ec2_work.workload_date = (select max(workload_date) from aws_instances_workload limit 1)
                       and ec2_price.workload_tag = vworkload_tag
                       and ec2.instance_tags_json @> JSON_WHERE::jsonb
                 )
                     as undersed_prices;
    ELSE
        RETURN QUERY
           select ec2_total_prices.total_instances::bigint,
                   undersed_prices.underused::bigint,
                   undersed_prices.cpu::varchar,
                   undersed_prices.memory::varchar,
                   undersed_prices.potential_waste_money_month::float,
                   ec2_total_prices.total_ec2_money_month::float,
                   (ec2_total_prices.total_ec2_money_month - undersed_prices.potential_waste_money_month)::float as gap
            from (
                     select count(ec2_price.instance_id)                 as total_instances,
                            round(sum(ec2_price.instance_mth_price_usd)) as total_ec2_money_month
                     from aws_instance_price as ec2_price
                              inner join aws_instances_workload as ec2_workload
                                         on ec2_price.instance_id = ec2_workload.instance_id
                     where ec2_workload.workload_date = (select max(workload_date) from aws_instances_workload limit 1)
                 )
                     as ec2_total_prices,
                 (
                     select count(ec2_work.workload_date)                                          as underused,
                            concat(round(avg(ec2_work.cpu_percentage)), '% avg used')              as cpu,
                            concat(round(avg(ec2_work.available_memory_percentage)), '% avg free') as memory,
                            round(sum(ec2_price.instance_mth_price_usd))                           as potential_waste_money_month

                     from aws_instances_workload as ec2_work
                              inner join aws_instance_price ec2_price on
                             ec2_work.instance_id = ec2_price.instance_id and
                             ec2_work.aws_region = ec2_price.aws_region
                     where ec2_work.workload_low_utilization = True
                       and ec2_work.workload_date = (select max(workload_date) from aws_instances_workload limit 1)
                       and ec2_price.workload_tag = vworkload_tag
                 )
                     as undersed_prices;
    END IF;
END;
$$;

