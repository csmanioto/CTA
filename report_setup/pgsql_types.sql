CREATE TYPE type_aws_asg_instances_aws_prices AS (
    instances_number bigint,
    instance_type varchar,
    aws_region varchar,
    instance_auto_scaling_group_name varchar,
    potential_ondemmand_price_monthly float,
    potential_reserved_price_monthly float,
    potential_discount_reserved_monthly float,
    potential_spot_price_monthly float,
    potential_discount_spot_monthly float,
    workload_date date
    );

--

CREATE TYPE type_aws_lat_long AS (
    number_of_instances bigint,
    aws_region varchar,
    aws_region_name varchar,
    aws_region_coordinate_lat varchar,
    aws_region_coordinate_log varchar
    );
--
CREATE TYPE type_aws_ondemand_reservation AS (
    ondemand_month float,
    reserved_month float,
    potential_saving_reserved float,
    saving_pct float
    );

--
create type type_aws_ondemand_reserved_by_instance as (
    instance_type varchar,
    ondemand_month float,
    spot_month float,
    reserved_month float,
    total_saving_reserved float,
    saving_pct float
    );

CREATE TYPE type_aws_total_ec2 as (
    total_instances bigint,
    total_running bigint,
    total_stopped bigint,
    total_terminated bigint,
    scan_date date
    );


CREATE TYPE type_ondemand_reserved_underuser as (
    total_instances bigint,
    underused bigint,
    cpu varchar,
    memory varchar,
    potential_waste_money_month float,
    total_ec2_money_month float,
    gap float
    );