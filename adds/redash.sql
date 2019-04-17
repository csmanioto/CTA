INSERT INTO organizations VALUES ('2019-04-15 15:38:11.041151+00', '2019-04-11 21:06:39.467732+00', 1, 'BookingGO', 'default', '{"settings": {"feature_show_permissions_control": false}}');
INSERT INTO data_sources VALUES (1, 1, 'Tracker', 'pg', '\x6741414141414263723679676e575346466750634a6765546b545f654362617348655a303154497a574c4e395641616272513276474c794c30506258694b727a6d4c49364f4872684a4d35565064766a4e79674934306d6136594836725043777470525347314758665971466b372d726758787a324855694145514d49506b49637270387541514952596f636a41434c44506c73772d6c384d6e447a665337513964616a30413947666b3878505339573774704b647568626d766539506e56715846467a70583451655444564158596d7a6630696436514841586e6e304e677137773d3d', 'queries', 'scheduled_queries', '2019-04-11 21:07:36.398738+00');
INSERT INTO queries VALUES ('2019-04-15 11:20:57.932686+00', '2019-04-15 08:45:11.409661+00', 10, 1, 1, 1, 1079, 'TOTAL INSTANCES - QADEV', NULL, 'select
       COALESCE(itt.total_instances, 0) total_instances,
       COALESCE(irn.total_instances, 0) total_running,
       COALESCE(istp.total_instances, 0) total_stopped,
       COALESCE(itm.total_instances, 0) total_terminated,
       irn.instance_state_date as scan_date
FROM
    (select count(instance_state)  as total_instances,
            instance_state_date::date as instance_state_date
     from aws_instances
      where instance_state = ''running''
      and workload_profile = ''QADEV''
      group by instance_state_date::date
     ) as irn
LEFT JOIN
    (select count(instance_state) as total_instances,
             instance_state_date::date as instance_state_date
     from aws_instances
     where instance_state = ''stopped''
     and workload_profile = ''QADEV''
     group by instance_state_date::date
    ) as istp
ON irn.instance_state_date = istp.instance_state_date

LEFT OUTER JOIN
    (select COALESCE(count(instance_id), 0) as total_instances,
            instance_state_date::date as instance_state_date
     from aws_instances
       where instance_state = ''terminated''
       and workload_profile = ''QADEV''
       group by instance_state_date::date
    ) as itm
ON irn.instance_state_date = itm.instance_state_date

LEFT OUTER JOIN
        (select COALESCE(count(instance_id), 0) as total_instances,
            instance_state_date::date as instance_state_date
     from aws_instances
        where workload_profile = ''QADEV''
       group by instance_state_date::date
    ) as itt
ON irn.instance_state_date = itt.instance_state_date
', 'cbf1a971478d3c1c6502c6e31fc7aa5d', 'GkSzNTud8O9PpZZMdQk2xNGyp56LywfMxu7rNKtD', 1, 1, false, false, NULL, 0, '{"parameters": []}', '''0'':10,17,24,31,129,177 ''10'':1B ''and'':64,100,148 ''as'':38,46,53,74,82,89,110,130,137,158,178,185,202 ''aws'':58,94,142,190 ''by'':69,105,153,197 ''coalesce'':6,13,20,27,125,173 ''count'':43,79,126,174 ''date'':37,40,51,52,56,72,73,87,88,92,108,109,116,120,135,136,140,156,157,164,168,183,184,188,200,201,208,212 ''from'':41,57,93,141,189 ''group'':68,104,152,196 ''id'':128,176 ''instance'':35,44,49,54,61,70,80,85,90,97,106,114,118,127,133,138,145,154,162,166,175,181,186,198,206,210 ''instances'':3A,9,12,16,23,30,48,59,84,95,132,143,180,191 ''irn'':14,34,75,113,161,205 ''istp'':21,111,117 ''itm'':28,159,165 ''itt'':7,203,209 ''join'':77,123,171 ''left'':76,121,169 ''on'':112,160,204 ''outer'':122,170 ''profile'':66,102,150,194 ''qadev'':4A,67,103,151,195 ''running'':19,63 ''scan'':39 ''select'':5,42,78,124,172 ''state'':36,45,50,55,62,71,81,86,91,98,107,115,119,134,139,146,155,163,167,182,187,199,207,211 ''stopped'':26,99 ''terminated'':33,147 ''total'':2A,8,11,15,18,22,25,29,32,47,83,131,179 ''where'':60,96,144,192 ''workload'':65,101,149,193', NULL);
INSERT INTO queries VALUES ('2019-04-15 11:18:27.332778+00', '2019-04-11 21:26:47.293942+00', 2, 1, 1, 1, 17, 'New Query', NULL, 'select * from aws_instances_workload', 'a7a7410af2d3c877ab9a8e3abdb4ef4c', 'BT2gJpRzoY7suZPRNOu30TwRFEe5DhxUEF1WVoYH', 1, 1, true, true, NULL, 0, '{"parameters": []}', '''2'':1B ''aws'':6 ''from'':5 ''instances'':7 ''new'':2A ''query'':3A ''select'':4 ''workload'':8', NULL);
INSERT INTO queries VALUES ('2019-04-15 12:48:23.332625+00', '2019-04-12 09:47:20.986331+00', 3, 1, 1, 1, 1082, 'Underused - QADEV', NULL, 'select count(workload_date) as underused,
       concat(round(avg(cpu_percentage)),''% used'') as cpu, 
       concat(round(avg(available_memory_percentage)), ''% free'') as memory_free
from aws_instances_workload as wk
inner join aws_instances as ec2 on
ec2.instance_id = wk.instance_id
where workload_low_utilization = True
and ec2.workload_profile = ''QADEV''', 'e621eec00333f14e6d087a243e836fca', 'cDVanxnvQE2V1TnE0UJ2vNoYNzLtvN6fKNV8VxjM', 1, 1, false, false, NULL, 0, '{"parameters": []}', '''3'':1B ''and'':52 ''as'':8,16,25,32,38 ''available'':21 ''avg'':12,20 ''aws'':29,36 ''concat'':10,18 ''count'':5 ''cpu'':13,17 ''date'':7 ''ec2'':39,41,53 ''free'':24,27 ''from'':28 ''id'':43,46 ''inner'':34 ''instance'':42,45 ''instances'':30,37 ''join'':35 ''low'':49 ''memory'':22,26 ''on'':40 ''percentage'':14,23 ''profile'':55 ''qadev'':3A,56 ''round'':11,19 ''select'':4 ''true'':51 ''underused'':2A,9 ''used'':15 ''utilization'':50 ''where'':47 ''wk'':33,44 ''workload'':6,31,48,54', NULL);
INSERT INTO queries VALUES ('2019-04-12 15:40:45.06686+00', '2019-04-12 12:48:29.897568+00', 8, 1, 1, 1, 1073, 'OnDemand x Reservation QADEV', NULL, '
select
           sum(aws_prices.price_ondemand_price_mth_usd) as ondemand_month,
           sum(aws_prices.price_reserved_price_mth_usd) as reserved_month,
           sum(aws_prices.price_ondemand_reserved_saving) as potential_saving_reserved,
           avg(aws_prices.price_ondemand_reserved_saving_pct) as saving_pct

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


where ec2.instance_running_price = ''OnDemand''
and ec2.workload_profile = ''QADEV''
    ) as ec2_ondemand
on ec2_ondemand.instance_type = aws_prices.instance_type and
   ec2_ondemand.aws_region = aws_prices.aws_region

-- group by aws_prices.instance_type,
--          aws_prices.price_ondemand_price_mth_usd,
--          aws_prices.price_ondemand_reserved_saving,
--          aws_prices.price_spot_price_mth_usd,
--          aws_prices.price_ondemand_spot_saving', 'ee2623f5b5540ad5405dbf610aa54539', '2bUUDI6LaU0XDSi6O1VkahPYEflnyPzx0Abwp0JD', 1, 1, false, false, NULL, 0, '{"parameters": []}', '''8'':1B ''and'':90,98,106,120,137 ''as'':15,26,36,48,73,80,125 ''avg'':40 ''aws'':8,19,30,41,52,67,70,78,93,96,133,140,142,144,148,152,159,165,172 ''by'':147 ''ec2'':57,61,65,74,81,83,87,91,95,99,103,107,111,115,121,126,129,138 ''from'':51,69 ''group'':146 ''id'':60,86,89 ''inner'':54,76 ''instance'':59,63,71,85,88,101,104,116,131,135,150 ''instances'':79 ''join'':55,77 ''month'':17,28 ''mth'':13,24,157,170 ''on'':82,128 ''ondemand'':2A,11,16,33,44,119,127,130,139,155,162,175 ''pct'':47,50 ''potential'':37 ''price'':10,12,21,23,32,43,58,62,66,72,75,84,92,100,108,118,154,156,161,167,169,174 ''prices'':9,20,31,42,53,134,143,149,153,160,166,173 ''profile'':110,113,123 ''qadev'':5A,124 ''region'':68,94,97,141,145 ''reservation'':4A ''reserved'':22,27,34,39,45,163 ''running'':117 ''saving'':35,38,46,49,164,177 ''select'':6,56 ''spot'':168,176 ''sum'':7,18,29 ''type'':64,102,105,132,136,151 ''usd'':14,25,158,171 ''where'':114 ''workload'':109,112,122 ''x'':3A', NULL);
INSERT INTO queries VALUES ('2019-04-15 12:46:39.035373+00', '2019-04-12 10:11:06.543485+00', 4, 1, 1, 1, 1085, 'ASG - DISCOUNT SPOT - QADEV', NULL, 'select aws_prices.instance_type,
       aws_prices.aws_region,
       aws_prices.price_ondemand_price_mth_usd as ondemmand_price_monthly,
       aws_prices.price_spot_price_mth_usd as spot_price_monthly,
       aws_prices.price_ondemand_reserved_saving as reserved_price_monthly,
       aws_prices.price_ondemand_spot_saving as discount_spot_monthly

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


where ec2.instance_auto_scaling_group = true
and ec2.instance_running_price = ''OnDemand''
and ec2.workload_profile = ''QADEV''
    ) as asg
on asg.instance_type = aws_prices.instance_type and
   asg.aws_region = aws_prices.aws_region

group by aws_prices.instance_type,
         aws_prices.aws_region,
         aws_prices.price_ondemand_price_mth_usd,
         aws_prices.price_ondemand_reserved_saving,
         aws_prices.price_spot_price_mth_usd,
         aws_prices.price_ondemand_spot_saving', '71d8a38644d96876cde34e8711270bec', 'bKd1ohSj0q8h5tOGbfgPxSWAUNLI2V4JRr5romkP', 1, 1, false, false, NULL, 0, '{"parameters": []}', '''4'':1B ''and'':96,104,112,127,133,148 ''as'':22,33,43,53,79,86,138 ''asg'':2A,139,141,149 ''auto'':123 ''aws'':7,11,13,15,26,37,47,58,73,76,84,99,102,144,150,152,154,158,162,164,166,173,179,186 ''by'':157 ''discount'':3A,54 ''ec2'':63,67,71,80,87,89,93,97,101,105,109,113,117,121,128,134 ''from'':57,75 ''group'':125,156 ''id'':66,92,95 ''inner'':60,82 ''instance'':9,65,69,77,91,94,107,110,122,129,142,146,160 ''instances'':85 ''join'':61,83 ''monthly'':25,36,46,56 ''mth'':20,31,171,184 ''on'':88,140 ''ondemand'':18,40,50,132,169,176,189 ''ondemmand'':23 ''price'':17,19,24,28,30,35,39,45,49,64,68,72,78,81,90,98,106,114,131,168,170,175,181,183,188 ''prices'':8,12,16,27,38,48,59,145,153,159,163,167,174,180,187 ''profile'':116,119,136 ''qadev'':5A,137 ''region'':14,74,100,103,151,155,165 ''reserved'':41,44,177 ''running'':130 ''saving'':42,52,178,191 ''scaling'':124 ''select'':6,62 ''spot'':4A,29,34,51,55,182,190 ''true'':126 ''type'':10,70,108,111,143,147,161 ''usd'':21,32,172,185 ''where'':120 ''workload'':115,118,135', NULL);
INSERT INTO queries VALUES ('2019-04-15 12:43:41.193608+00', '2019-04-12 11:55:12.902048+00', 6, 1, 1, 1, 1076, 'ASG OnDemand vs SPOT - QADEV', NULL, '
select
       count(ec2_ondemand.instance_id) as ondemand_ec2,
       sum(aws_prices.price_ondemand_price_mth_usd) as ondemand_month,
       sum(aws_prices.price_spot_price_mth_usd) as spot_month,
       sum(aws_prices.price_ondemand_spot_saving) as total_saving_spot,
       concat(round(avg(aws_prices.price_ondemand_spot_saving_pct)), ''%'') as saving_pct


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


where ec2.instance_running_price = ''OnDemand''
and ec2.workload_profile = ''QADEV''
and ec2.instance_auto_scaling_group = True
    ) as ec2_ondemand
on ec2_ondemand.instance_type = aws_prices.instance_type and
   ec2_ondemand.aws_region = aws_prices.aws_region
', '6bbe21c9c5d3baa50766797920c94bae', '8ZS3C2yWE294cCd6boB23Iyy8c9ZJbvJKVEzUfRk', 1, 1, false, false, NULL, 0, '{"parameters": []}', '''6'':1B ''and'':101,109,117,131,136,155 ''as'':13,24,35,45,59,84,91,143 ''asg'':2A ''auto'':139 ''avg'':51 ''aws'':17,28,39,52,63,78,81,89,104,107,151,158,160,162 ''concat'':49 ''count'':8 ''ec2'':9,15,68,72,76,85,92,94,98,102,106,110,114,118,122,126,132,137,144,147,156 ''from'':62,80 ''group'':141 ''id'':12,71,97,100 ''inner'':65,87 ''instance'':11,70,74,82,96,99,112,115,127,138,149,153 ''instances'':90 ''join'':66,88 ''month'':26,37 ''mth'':22,33 ''on'':93,146 ''ondemand'':3A,10,14,20,25,42,55,130,145,148,157 ''pct'':58,61 ''price'':19,21,30,32,41,54,69,73,77,83,86,95,103,111,119,129 ''prices'':18,29,40,53,64,152,161 ''profile'':121,124,134 ''qadev'':6A,135 ''region'':79,105,108,159,163 ''round'':50 ''running'':128 ''saving'':44,47,57,60 ''scaling'':140 ''select'':7,67 ''spot'':5A,31,36,43,48,56 ''sum'':16,27,38 ''total'':46 ''true'':142 ''type'':75,113,116,150,154 ''usd'':23,34 ''vs'':4A ''where'':125 ''workload'':120,123,133', NULL);
INSERT INTO queries VALUES ('2019-04-15 13:28:38.199032+00', '2019-04-12 10:29:54.223522+00', 5, 1, 1, 1, 1083, 'Lowutilisation - Ondemand x Underused - QADEV', NULL, 'select ec2_total_prices.total_instances,
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
                concat(round(avg(ec2_work.cpu_percentage)), ''% used'')              as cpu,
                concat(round(avg(ec2_work.available_memory_percentage)), ''% used'') as memory,
                round(sum(ec2_price.instance_mth_price_usd))                       as potential_waste_money_month

         from aws_instances_workload as ec2_work
                  inner join aws_instance_price ec2_price on
                 ec2_work.instance_id = ec2_price.instance_id and
                 ec2_work.aws_region = ec2_price.aws_region
         where ec2_work.workload_low_utilization = True
         and ec2_price.workload_profile = ''QADEV''
     )
as undersed_prices', '3125cfa44223183f6f7ac84f77e66841', '7ZAr3NxmX1cuJ28damKMsslaGfoOqGNBIaTTOg3U', 1, 1, false, false, NULL, 0, '{"parameters": []}', '''5'':1B ''and'':130,146 ''as'':40,52,61,71,81,92,102,111,152 ''available'':88 ''avg'':75,85 ''aws'':45,58,108,116,133,137 ''concat'':73,83 ''count'':37,66 ''cpu'':18,78,82 ''date'':70 ''ec2'':8,28,32,54,62,67,76,86,96,112,119,122,126,131,135,140,147 ''from'':35,57,107 ''id'':39,125,129 ''inner'':114 ''instance'':38,46,48,59,98,117,124,128 ''instances'':12,42,109 ''join'':115 ''low'':143 ''lowutilisation'':2A ''memory'':21,89,93 ''money'':26,33,55,105 ''month'':27,34,56,106 ''mth'':49,99 ''on'':121 ''ondemand'':3A ''percentage'':79,90 ''potential'':24,103 ''price'':47,50,60,97,100,118,120,127,136,148 ''prices'':10,14,17,20,23,30,64,154 ''profile'':150 ''qadev'':6A,151 ''region'':134,138 ''round'':43,74,84,94 ''select'':7,36,65 ''sum'':44,95 ''total'':9,11,29,31,41,53,63 ''true'':145 ''undersed'':13,16,19,22,153 ''underused'':5A,15,72 ''usd'':51,101 ''used'':80,91 ''utilization'':144 ''waste'':25,104 ''where'':139 ''work'':68,77,87,113,123,132,141 ''workload'':69,110,142,149 ''x'':4A', NULL);
INSERT INTO queries VALUES ('2019-04-12 15:59:08.54171+00', '2019-04-11 21:18:29.826753+00', 1, 1, 1, 1, 1081, 'Intances by regions - QADEV', NULL, 'select count(instance_state),
       aws_region,
       aws_region_name,
       aws_region_coordinate_lat,
       aws_region_coordinate_log
from aws_instances
where workload_profile = ''QADEV''
--and instance_state = "running"
group by aws_region, aws_region_name, aws_region_coordinate_lat, aws_region_coordinate_log
', 'ae4b7b7036ad6122dc5d6a0d4037dc97', 'gdIpw453hZBDz0F8Nh6Ugn7bwQeWgew2iO7lw9lE', 1, 1, false, false, NULL, 0, '{"parameters": []}', '''1'':1B ''and'':30 ''aws'':10,12,15,19,24,36,38,41,45 ''by'':3A,35 ''coordinate'':17,21,43,47 ''count'':7 ''from'':23 ''group'':34 ''instance'':8,31 ''instances'':25 ''intances'':2A ''lat'':18,44 ''log'':22,48 ''name'':14,40 ''profile'':28 ''qadev'':5A,29 ''region'':11,13,16,20,37,39,42,46 ''regions'':4A ''running'':33 ''select'':6 ''state'':9,32 ''where'':26 ''workload'':27', NULL);
INSERT INTO queries VALUES ('2019-04-15 15:41:43.834563+00', '2019-04-15 15:33:51.971349+00', 11, 1, 1, 1, 1070, 'Instance Kernel details - QADEV', NULL, 'select instance_type, 
       aws_region, 
       aws_region_name, 
       instance_linux_distribution, 
       instance_linux_kernel_version
from aws_instances
where workload_profile = ''QADEV''
and instance_linux_kernel_version is not null
group by instance_type, 
         aws_region,
         aws_region_name, 
         instance_linux_distribution,
         instance_linux_kernel_version
', 'f74ec2c44fcf96e7e62b8bca9709833c', 'O29L8ssMQ3UD52Cwk9VUjjtcFqiAtg3QMVhOVt7Z', 1, 1, false, false, NULL, 0, '{"parameters": []}', '''11'':1B ''and'':28 ''aws'':9,11,22,40,42 ''by'':37 ''details'':4A ''distribution'':16,47 ''from'':21 ''group'':36 ''instance'':2A,7,14,17,29,38,45,48 ''instances'':23 ''is'':33 ''kernel'':3A,19,31,50 ''linux'':15,18,30,46,49 ''name'':13,44 ''not'':34 ''null'':35 ''profile'':26 ''qadev'':5A,27 ''region'':10,12,41,43 ''select'':6 ''type'':8,39 ''version'':20,32,51 ''where'':24 ''workload'':25', NULL);
INSERT INTO queries VALUES ('2019-04-15 15:49:27.37535+00', '2019-04-15 15:38:11.041151+00', 12, 1, 1, 1, 1069, 'AWS Price - Instances price by Region', NULL, 'select instance_type,
       aws_region,
       price_date::date as offer_date,
       price_ondemand_price_mth_usd as ondemand, 
       price_reserved_price_mth_usd as reserved1yr,
       price_spot_price_mth_usd as spot
from aws_prices
order by price_ondemand_price_mth_usd, instance_type', '4b0406edcadb67d1bc0e31fc3b2612c7', 'Y966OvqO9PSdLprSW2gl4tHckluRVKFDfB3UKooG', 1, 1, false, false, NULL, 0, '{"parameters": []}', '''12'':1B ''as'':16,24,31,38 ''aws'':2A,11,41 ''by'':6A,44 ''date'':14,15,18 ''from'':40 ''instance'':9,50 ''instances'':4A ''mth'':22,29,36,48 ''offer'':17 ''ondemand'':20,25,46 ''order'':43 ''price'':3A,5A,13,19,21,26,28,33,35,45,47 ''prices'':42 ''region'':7A,12 ''reserved'':27 ''reserved1yr'':32 ''select'':8 ''spot'':34,39 ''type'':10,51 ''usd'':23,30,37,49', NULL);
INSERT INTO queries VALUES ('2019-04-15 12:15:53.45097+00', '2019-04-12 12:34:16.375563+00', 7, 1, 1, 1, 1080, 'OnDemand x Reserved by instance type - QA', NULL, 'select
           ec2_ondemand.instance_type as instance_type,
           aws_prices.price_ondemand_price_mth_usd as ondemand_month,
           aws_prices.price_spot_price_mth_usd as spot_month,
           aws_prices.price_reserved_price_mth_usd as reserved_month,
           aws_prices.price_ondemand_reserved_saving as total_saving_reserved,
           aws_prices.price_ondemand_reserved_saving_pct as saving_pct
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


where ec2.instance_running_price = ''OnDemand''
and ec2.workload_profile = ''QADEV''
    ) as ec2_ondemand
on ec2_ondemand.instance_type = aws_prices.instance_type and
   ec2_ondemand.aws_region = aws_prices.aws_region', '564cb81d4f5d37e15c5a64e561c31196', '0C0evsj3B6ZP2ep2DSrVxkVAqYxt4VtCtBFqsuAz', 1, 1, false, false, NULL, 0, '{"parameters": []}', '''7'':1B ''and'':106,114,122,136,153 ''as'':14,24,34,44,53,64,89,96,141 ''aws'':17,27,37,47,57,68,83,86,94,109,112,149,156,158,160 ''by'':5A ''ec2'':10,73,77,81,90,97,99,103,107,111,115,119,123,127,131,137,142,145,154 ''from'':67,85 ''id'':76,102,105 ''inner'':70,92 ''instance'':6A,12,15,75,79,87,101,104,117,120,132,147,151 ''instances'':95 ''join'':71,93 ''month'':26,36,46 ''mth'':22,32,42 ''on'':98,144 ''ondemand'':2A,11,20,25,50,60,135,143,146,155 ''pct'':63,66 ''price'':19,21,29,31,39,41,49,59,74,78,82,88,91,100,108,116,124,134 ''prices'':18,28,38,48,58,69,150,159 ''profile'':126,129,139 ''qa'':8A ''qadev'':140 ''region'':84,110,113,157,161 ''reserved'':4A,40,45,51,56,61 ''running'':133 ''saving'':52,55,62,65 ''select'':9,72 ''spot'':30,35 ''total'':54 ''type'':7A,13,16,80,118,121,148,152 ''usd'':23,33,43 ''where'':130 ''workload'':125,128,138 ''x'':3A', NULL);
INSERT INTO queries VALUES ('2019-04-12 15:41:09.81856+00', '2019-04-12 13:22:54.734063+00', 9, 1, 1, 1, 1084, 'ASG Ondemand x Spot - QADEV', NULL, 'select
        ec2.instance_auto_scaling_group_name as autoscaling_group,
        sum(price.price_ondemand_price_mth_usd) as ondemmand_price_monthly,
        sum(price.price_spot_price_mth_usd) as spot_price_monthly,
        sum(price.price_ondemand_spot_saving) as discount_spot_monthly

from aws_instances as ec2
     inner join aws_prices price on
ec2.instance_type = price.instance_type and
ec2.aws_region = price.aws_region
where ec2.instance_auto_scaling_group = true
and workload_profile = ''QADEV''
group by instance_auto_scaling_group_name', '8a2e5a47a139d9a0edb8e1a0dec85ec7', 'AghXyzPF8s2GEQdfOY79oNzyoYOZ2GEIPpjqKkdG', 1, 1, false, false, NULL, 0, '{"parameters": []}', '''9'':1B ''and'':66,80 ''as'':14,24,35,45,52 ''asg'':2A ''auto'':10,76,87 ''autoscaling'':15 ''aws'':50,56,68,71 ''by'':85 ''discount'':46 ''ec2'':8,53,60,67,74 ''from'':49 ''group'':12,16,78,84,89 ''inner'':54 ''instance'':9,61,64,75,86 ''instances'':51 ''join'':55 ''monthly'':27,38,48 ''mth'':22,33 ''name'':13,90 ''on'':59 ''ondemand'':3A,20,42 ''ondemmand'':25 ''price'':18,19,21,26,29,30,32,37,40,41,58,63,70 ''prices'':57 ''profile'':82 ''qadev'':6A,83 ''region'':69,72 ''saving'':44 ''scaling'':11,77,88 ''select'':7 ''spot'':5A,31,36,43,47 ''sum'':17,28,39 ''true'':79 ''type'':62,65 ''usd'':23,34 ''where'':73 ''workload'':81 ''x'':4A', NULL);

INSERT INTO dashboards VALUES ('2019-04-15 12:49:36.311888+00', '2019-04-11 21:08:01.350312+00', 1, 14, 1, 'qa', 'QA/DEV', 1, '[]', false, false, false, NULL);
INSERT INTO groups VALUES (1, 1, 'builtin', 'admin', '{admin,super_admin}', '2019-04-11 21:06:39.467732+00');
INSERT INTO groups VALUES (2, 1, 'builtin', 'default', '{create_dashboard,create_query,edit_dashboard,edit_query,view_query,view_source,execute_query,list_users,schedule_query,list_dashboards,list_alerts,list_data_sources}', '2019-04-11 21:06:39.467732+00');
INSERT INTO visualizations VALUES ('2019-04-11 21:18:29.826753+00', '2019-04-11 21:18:29.826753+00', 1, 'TABLE', 1, 'Table', '', '{}');
INSERT INTO visualizations VALUES ('2019-04-11 21:26:47.293942+00', '2019-04-11 21:26:47.293942+00', 3, 'TABLE', 2, 'Table', '', '{}');
INSERT INTO visualizations VALUES ('2019-04-15 12:49:36.311888+00', '2019-04-12 10:15:11.572812+00', 10, 'COUNTER', 4, 'Counter', '', '{"targetColName": null, "rowNumber": 1, "stringDecChar": ".", "defaultColumns": 2, "stringDecimal": 0, "countRow": true, "counterColName": "instance_type", "counterLabel": "total candidate for SPOT instances", "defaultRows": 5, "stringThouSep": ",", "targetRowNumber": 1}');
INSERT INTO visualizations VALUES ('2019-04-12 09:47:20.986331+00', '2019-04-12 09:47:20.986331+00', 5, 'TABLE', 3, 'Table', '', '{}');
INSERT INTO visualizations VALUES ('2019-04-12 09:49:28.416725+00', '2019-04-12 09:49:28.416725+00', 6, 'COUNTER', 3, 'Counter', '', '{"targetColName": null, "rowNumber": 1, "stringDecChar": ".", "defaultColumns": 2, "stringDecimal": 0, "countRow": false, "counterColName": "underused", "counterLabel": "Underused instances", "defaultRows": 5, "stringThouSep": ",", "targetRowNumber": 1}');
INSERT INTO visualizations VALUES ('2019-04-15 13:28:36.587264+00', '2019-04-12 11:15:52.281+00', 15, 'CHART', 5, 'TOTAL EC2 USD vs TOTAL UNDERUSED Instances - QA', '', '{"minColumns": 1, "series": {"stacking": null, "error_y": {"visible": true, "type": "data"}}, "sortX": true, "valuesOptions": {}, "dateTimeFormat": "DD/MM/YY HH:mm", "defaultRows": 8, "error_y": {"visible": true, "type": "data"}, "percentFormat": "0[.]00%", "yAxis": [{"type": "linear"}, {"type": "linear", "opposite": true}], "minRows": 5, "seriesOptions": {"potential_waste_money_month": {"index": 0, "name": "U$ Potential Saving", "yAxis": 0, "color": "#3BD973", "zIndex": 1, "type": "column"}, "total_ec2_money_month": {"index": 0, "name": "U$ Total money with EC2", "yAxis": 0, "color": "#356AFF", "zIndex": 0, "type": "column"}}, "showDataLabels": true, "numberFormat": "$ 0,0[.]0", "xAxis": {"labels": {"enabled": false}, "type": "category", "title": {"text": ""}}, "legend": {"enabled": true}, "customCode": "// Available variables are x, ys, element, and Plotly\n// Type console.log(x, ys); for more info about x and ys\n// To plot your graph call Plotly.plot(element, ...)\n// Plotly examples and docs: https://plot.ly/javascript/", "globalSeriesType": "column", "defaultColumns": 3, "reverseX": false, "reverseY": false, "columnMapping": {"potential_waste_money_month": "y", "total_instances": "x", "underused": "unused", "cpu": "unused", "total_ec2_money_month": "y"}, "textFormat": ""}');
INSERT INTO visualizations VALUES ('2019-04-12 10:11:06.543485+00', '2019-04-12 10:11:06.543485+00', 8, 'TABLE', 4, 'Table', '', '{}');
INSERT INTO visualizations VALUES ('2019-04-12 10:18:54.185607+00', '2019-04-12 10:18:54.185607+00', 11, 'CHART', 4, 'Chart', '', '{"showDataLabels": false, "error_y": {"visible": true, "type": "data"}, "numberFormat": "0,0[.]00000", "yAxis": [{"type": "linear"}, {"type": "linear", "opposite": true}], "minColumns": 1, "series": {"stacking": null, "error_y": {"visible": true, "type": "data"}}, "globalSeriesType": "column", "percentFormat": "0[.]00%", "minRows": 5, "defaultColumns": 3, "sortX": true, "seriesOptions": {}, "valuesOptions": {}, "xAxis": {"labels": {"enabled": true}, "type": "-"}, "dateTimeFormat": "DD/MM/YY HH:mm", "columnMapping": {}, "textFormat": "", "defaultRows": 8, "customCode": "// Available variables are x, ys, element, and Plotly\n// Type console.log(x, ys); for more info about x and ys\n// To plot your graph call Plotly.plot(element, ...)\n// Plotly examples and docs: https://plot.ly/javascript/", "legend": {"enabled": true}}');
INSERT INTO visualizations VALUES ('2019-04-12 10:20:11.613378+00', '2019-04-12 10:13:46.77+00', 9, 'PIVOT', 4, 'Total saving USD changing on demand to spot instance on ASG', '', '{"minColumns": 2, "cols": [], "rendererName": "Table", "vals": ["discount_spot_monthly"], "defaultRows": 10, "colOrder": "key_a_to_z", "menuLimit": 500, "rows": ["instance_type", "ondemmand_price_monthly", "spot_price_monthly", "discount_spot_monthly"], "showUI": true, "autoSortUnusedAttrs": false, "controls": {"enabled": true}, "hiddenFromAggregators": [], "unusedAttrsVertical": 85, "derivedAttributes": {}, "hiddenAttributes": [], "inclusions": {}, "aggregatorName": "Sum", "hiddenFromDragDrop": [], "sorters": {}, "defaultColumns": 3, "inclusionsInfo": {}, "rowOrder": "key_a_to_z", "exclusions": {}}');
INSERT INTO visualizations VALUES ('2019-04-12 11:55:12.902048+00', '2019-04-12 11:55:12.902048+00', 16, 'TABLE', 6, 'Table', '', '{}');
INSERT INTO visualizations VALUES ('2019-04-12 12:31:41.057116+00', '2019-04-12 09:51:10.47+00', 7, 'TABLE', 3, 'Table', '', '{"autoHeight": true, "minColumns": 2, "itemsPerPage": 5, "defaultColumns": 3, "defaultRows": 14, "columns": [{"linkUrlTemplate": "{{ @ }}", "name": "underused", "numberFormat": "0,0", "linkTextTemplate": "{{ @ }}", "imageUrlTemplate": "{{ @ }}", "title": "Instances Underused", "linkOpenInNewTab": true, "displayAs": "number", "allowSearch": false, "allowHTML": true, "imageTitleTemplate": "{{ @ }}", "visible": true, "alignContent": "center", "imageHeight": "", "highlightLinks": false, "imageWidth": "", "linkTitleTemplate": "{{ @ }}", "booleanValues": ["false", "true"], "type": "integer", "order": 100000}, {"linkUrlTemplate": "{{ @ }}", "name": "cpu", "highlightLinks": false, "linkTextTemplate": "{{ @ }}", "imageUrlTemplate": "{{ @ }}", "title": "avg cpu %", "linkOpenInNewTab": true, "displayAs": "string", "allowSearch": false, "allowHTML": true, "imageTitleTemplate": "{{ @ }}", "visible": true, "alignContent": "center", "imageHeight": "", "imageWidth": "", "linkTitleTemplate": "{{ @ }}", "booleanValues": ["false", "true"], "type": "string", "order": 100001}, {"linkUrlTemplate": "{{ @ }}", "name": "memory", "highlightLinks": false, "linkTextTemplate": "{{ @ }}", "imageUrlTemplate": "{{ @ }}", "title": "avg memory used %", "linkOpenInNewTab": true, "displayAs": "string", "allowSearch": false, "allowHTML": true, "imageTitleTemplate": "{{ @ }}", "visible": true, "alignContent": "center", "imageHeight": "", "imageWidth": "", "linkTitleTemplate": "{{ @ }}", "booleanValues": ["false", "true"], "type": "string", "order": 100002}, {"linkUrlTemplate": "{{ @ }}", "name": "potential_waste_money_month", "numberFormat": "U$ 0,0.00", "linkTextTemplate": "{{ @ }}", "imageUrlTemplate": "{{ @ }}", "title": "Potential waste $", "linkOpenInNewTab": true, "displayAs": "number", "allowSearch": false, "allowHTML": true, "imageTitleTemplate": "{{ @ }}", "visible": true, "alignContent": "center", "imageHeight": "", "highlightLinks": false, "imageWidth": "", "linkTitleTemplate": "{{ @ }}", "booleanValues": ["false", "true"], "type": "float", "order": 100003}, {"linkUrlTemplate": "{{ @ }}", "name": "total_ec2_money_month", "numberFormat": "U$ 0,0.00", "linkTextTemplate": "{{ @ }}", "imageUrlTemplate": "{{ @ }}", "title": "Total EC2", "linkOpenInNewTab": true, "displayAs": "number", "allowSearch": false, "allowHTML": true, "imageTitleTemplate": "{{ @ }}", "visible": true, "alignContent": "center", "imageHeight": "", "highlightLinks": false, "imageWidth": "", "linkTitleTemplate": "{{ @ }}", "booleanValues": ["false", "true"], "type": "float", "order": 100004}]}');
INSERT INTO visualizations VALUES ('2019-04-12 15:58:48.281058+00', '2019-04-11 21:21:01.864+00', 2, 'MAP', 1, 'Map (Markers)', '', '{"mapTileUrl": "//{s}.tile.openstreetmap.fr/osmfr/{z}/{x}/{y}.png", "clusterMarkers": true, "minColumns": 2, "bounds": {"_southWest": {"lat": 0, "lng": -200.21484375000003}, "_northEast": {"lat": 65.6582745198266, "lng": 47.63671875000001}}, "defaultColumns": 3, "groups": {"All": {"color": "#1f77b4"}}, "latColName": "aws_region_coordinate_lat", "defaultRows": 8, "lonColName": "aws_region_coordinate_log", "classify": "none"}');
INSERT INTO visualizations VALUES ('2019-04-12 12:25:16.104748+00', '2019-04-12 10:29:54.223+00', 12, 'TABLE', 5, 'Table', '', '{"autoHeight": true, "minColumns": 2, "itemsPerPage": 25, "defaultColumns": 3, "defaultRows": 14, "columns": [{"linkUrlTemplate": "{{ @ }}", "name": "total_instances", "numberFormat": "0,0", "linkTextTemplate": "{{ @ }}", "imageUrlTemplate": "{{ @ }}", "title": "total ec2", "linkOpenInNewTab": true, "displayAs": "number", "allowSearch": false, "allowHTML": true, "imageTitleTemplate": "{{ @ }}", "visible": true, "alignContent": "center", "imageHeight": "", "highlightLinks": false, "imageWidth": "", "linkTitleTemplate": "{{ @ }}", "booleanValues": ["false", "true"], "type": "integer", "order": 100000}, {"linkUrlTemplate": "{{ @ }}", "name": "underused", "numberFormat": "0,0", "linkTextTemplate": "{{ @ }}", "imageUrlTemplate": "{{ @ }}", "title": "underused", "linkOpenInNewTab": true, "displayAs": "number", "allowSearch": false, "allowHTML": true, "imageTitleTemplate": "{{ @ }}", "visible": true, "alignContent": "center", "imageHeight": "", "highlightLinks": false, "imageWidth": "", "linkTitleTemplate": "{{ @ }}", "booleanValues": ["false", "true"], "type": "integer", "order": 100001}, {"linkUrlTemplate": "{{ @ }}", "name": "cpu", "highlightLinks": false, "linkTextTemplate": "{{ @ }}", "imageUrlTemplate": "{{ @ }}", "title": "cpu", "linkOpenInNewTab": true, "displayAs": "string", "allowSearch": false, "allowHTML": true, "imageTitleTemplate": "{{ @ }}", "visible": true, "alignContent": "center", "imageHeight": "", "imageWidth": "", "linkTitleTemplate": "{{ @ }}", "booleanValues": ["false", "true"], "type": "string", "order": 100002}, {"linkUrlTemplate": "{{ @ }}", "name": "memory", "highlightLinks": false, "linkTextTemplate": "{{ @ }}", "imageUrlTemplate": "{{ @ }}", "title": "memory", "linkOpenInNewTab": true, "displayAs": "string", "allowSearch": false, "allowHTML": true, "imageTitleTemplate": "{{ @ }}", "visible": true, "alignContent": "center", "imageHeight": "", "imageWidth": "", "linkTitleTemplate": "{{ @ }}", "booleanValues": ["false", "true"], "type": "string", "order": 100003}, {"linkUrlTemplate": "{{ @ }}", "name": "potential_waste_money_month", "numberFormat": "0,0.00", "linkTextTemplate": "{{ @ }}", "imageUrlTemplate": "{{ @ }}", "title": "potential_waste_money_month", "linkOpenInNewTab": true, "displayAs": "number", "allowSearch": false, "allowHTML": true, "imageTitleTemplate": "{{ @ }}", "visible": true, "alignContent": "center", "imageHeight": "", "highlightLinks": false, "imageWidth": "", "linkTitleTemplate": "{{ @ }}", "booleanValues": ["false", "true"], "type": "float", "order": 100004}, {"linkUrlTemplate": "{{ @ }}", "name": "total_ec2_money_month", "numberFormat": "0,0.00", "linkTextTemplate": "{{ @ }}", "imageUrlTemplate": "{{ @ }}", "title": "total_ec2_money_month", "linkOpenInNewTab": true, "displayAs": "number", "allowSearch": false, "allowHTML": true, "imageTitleTemplate": "{{ @ }}", "visible": true, "alignContent": "center", "imageHeight": "", "highlightLinks": false, "imageWidth": "", "linkTitleTemplate": "{{ @ }}", "booleanValues": ["false", "true"], "type": "float", "order": 100005}]}');
INSERT INTO visualizations VALUES ('2019-04-12 12:03:21.790498+00', '2019-04-12 11:55:12.902+00', 17, 'CHART', 6, 'Current Ondemand x  Posible Reservation 1yrs no-upfront', '', '{"showDataLabels": true, "error_y": {"visible": true, "type": "data"}, "numberFormat": "$ 0,0[.]0", "minColumns": 1, "defaultColumns": 3, "series": {"stacking": null, "error_y": {"visible": true, "type": "data"}}, "globalSeriesType": "column", "yAxis": [{"type": "linear"}, {"type": "linear", "opposite": true}], "minRows": 5, "percentFormat": "0[.]00%", "reverseX": false, "sortX": true, "seriesOptions": {"spot_month": {"zIndex": 1, "index": 0, "type": "column", "yAxis": 0}, "ondemand_month": {"zIndex": 0, "index": 0, "type": "column", "color": "#3BD973", "yAxis": 0}}, "valuesOptions": {}, "xAxis": {"labels": {"enabled": true}, "type": "category", "title": {"text": "Potential save"}}, "dateTimeFormat": "DD/MM/YY HH:mm", "columnMapping": {"saving_pct": "x", "ondemand_ec2": "unused", "total_saving_spot": "unused", "spot_month": "y", "ondemand_month": "y"}, "textFormat": "", "defaultRows": 8, "customCode": "// Available variables are x, ys, element, and Plotly\n// Type console.log(x, ys); for more info about x and ys\n// To plot your graph call Plotly.plot(element, ...)\n// Plotly examples and docs: https://plot.ly/javascript/", "legend": {"enabled": true}}');
INSERT INTO visualizations VALUES ('2019-04-12 12:34:16.375563+00', '2019-04-12 12:34:16.375563+00', 18, 'TABLE', 7, 'Table', '', '{}');
INSERT INTO visualizations VALUES ('2019-04-12 13:22:54.734063+00', '2019-04-12 13:22:54.734063+00', 22, 'TABLE', 9, 'Table', '', '{}');
INSERT INTO visualizations VALUES ('2019-04-12 12:48:29.897568+00', '2019-04-12 12:48:29.897568+00', 20, 'TABLE', 8, 'Table', '', '{}');
INSERT INTO visualizations VALUES ('2019-04-12 12:50:51.175191+00', '2019-04-12 12:48:50.133+00', 21, 'CHART', 8, 'Ondemand x Reservation - 1yr without upfront', '', '{"showDataLabels": true, "error_y": {"visible": true, "type": "data"}, "numberFormat": "U$ 0,0[.]00000", "minColumns": 1, "defaultColumns": 3, "series": {"stacking": null, "error_y": {"visible": true, "type": "data"}}, "globalSeriesType": "column", "yAxis": [{"type": "linear"}, {"type": "linear", "opposite": true}], "minRows": 5, "percentFormat": "0[.]00%", "reverseX": false, "sortX": true, "seriesOptions": {"reserved_month": {"zIndex": 1, "index": 0, "type": "column", "color": "#50F5ED", "yAxis": 0}, "ondemand_month": {"zIndex": 0, "index": 0, "type": "column", "color": "#3BD973", "yAxis": 0}}, "valuesOptions": {}, "xAxis": {"labels": {"enabled": true}, "type": "category", "title": {"text": "Potential saving %"}}, "dateTimeFormat": "DD/MM/YY HH:mm", "columnMapping": {"saving_pct": "x", "reserved_month": "y", "ondemand_month": "y"}, "textFormat": "", "defaultRows": 8, "customCode": "// Available variables are x, ys, element, and Plotly\n// Type console.log(x, ys); for more info about x and ys\n// To plot your graph call Plotly.plot(element, ...)\n// Plotly examples and docs: https://plot.ly/javascript/", "legend": {"enabled": true}}');
INSERT INTO visualizations VALUES ('2019-04-15 11:21:14.752522+00', '2019-04-15 08:45:11.409661+00', 24, 'TABLE', 10, 'Table', '', '{}');
INSERT INTO visualizations VALUES ('2019-04-12 14:08:31.139072+00', '2019-04-12 13:27:55.878+00', 23, 'PIVOT', 9, 'Total potencial saving month using Spot instance', '', '{"minColumns": 2, "cols": [], "rendererName": "Table", "vals": ["discount_spot_monthly"], "defaultRows": 10, "colOrder": "key_a_to_z", "menuLimit": 500, "rows": ["autoscaling_group", "ondemmand_price_monthly", "discount_spot_monthly", "spot_price_monthly"], "showUI": true, "autoSortUnusedAttrs": false, "controls": {"enabled": true}, "hiddenFromAggregators": [], "unusedAttrsVertical": 85, "derivedAttributes": {}, "hiddenAttributes": [], "inclusions": {}, "aggregatorName": "Sum", "hiddenFromDragDrop": [], "sorters": {}, "defaultColumns": 3, "inclusionsInfo": {}, "rowOrder": "key_a_to_z", "exclusions": {}}');
INSERT INTO visualizations VALUES ('2019-04-15 12:15:51.138604+00', '2019-04-12 12:35:35.673+00', 19, 'CHART', 7, 'Chart', '', '{"showDataLabels": true, "error_y": {"visible": true, "type": "data"}, "numberFormat": "U$ 0,0[.]00000", "minColumns": 1, "defaultColumns": 3, "series": {"stacking": null, "error_y": {"visible": true, "type": "data"}}, "globalSeriesType": "column", "yAxis": [{"type": "linear", "rangeMin": 10, "title": {"text": "USD Month"}}, {"type": "linear", "rangeMin": 5, "opposite": true}], "minRows": 5, "percentFormat": "0[.]00%", "reverseX": false, "sortX": true, "seriesOptions": {"reserved_month": {"index": 0, "name": "U$ reserved/month", "yAxis": 0, "color": "#50F5ED", "zIndex": 1, "type": "column"}, "ondemand_month": {"index": 0, "name": "U$ ondemand/month", "yAxis": 0, "color": "#3BD973", "zIndex": 0, "type": "column"}}, "valuesOptions": {}, "xAxis": {"labels": {"enabled": true}, "type": "category", "title": {"text": "OnDemand x Reserved Monthly price"}}, "dateTimeFormat": "DD/MM/YY HH:mm", "columnMapping": {"saving_pct": "unused", "instance_type": "x", "total_saving_reserved": "unused", "reserved_month": "y", "ondemand_month": "y"}, "textFormat": "", "defaultRows": 8, "customCode": "// Available variables are x, ys, element, and Plotly\n// Type console.log(x, ys); for more info about x and ys\n// To plot your graph call Plotly.plot(element, ...)\n// Plotly examples and docs: https://plot.ly/javascript/", "legend": {"enabled": true}}');
INSERT INTO visualizations VALUES ('2019-04-15 11:20:54.90215+00', '2019-04-15 11:17:02.596+00', 25, 'CHART', 10, 'Chart', '', '{"showDataLabels": true, "error_y": {"visible": true, "type": "data"}, "numberFormat": "0,0[.]00000", "minColumns": 1, "defaultColumns": 3, "series": {"stacking": null, "percentValues": false, "error_y": {"visible": true, "type": "data"}}, "globalSeriesType": "column", "yAxis": [{"type": "linear"}, {"type": "linear", "opposite": true}], "minRows": 5, "percentFormat": "0[.]00%", "reverseX": false, "sortX": true, "seriesOptions": {"total_instances": {"zIndex": 0, "index": 0, "type": "area", "color": "#799CFF", "yAxis": 1}, "total_stopped": {"zIndex": 2, "index": 0, "type": "line", "color": "#FB8D3D", "yAxis": 1}, "total_terminated": {"zIndex": 3, "index": 0, "type": "line", "color": "#E92828", "yAxis": 1}, "total_running": {"zIndex": 1, "index": 0, "type": "line", "color": "#3BD973", "yAxis": 1}}, "valuesOptions": {}, "xAxis": {"labels": {"enabled": true}, "type": "datetime"}, "dateTimeFormat": "DD/MM/YY HH:mm", "columnMapping": {"total_instances": "y", "total_stopped": "y", "scan_date": "x", "total_terminated": "y", "total_running": "y"}, "textFormat": "", "defaultRows": 8, "customCode": "// Available variables are x, ys, element, and Plotly\n// Type console.log(x, ys); for more info about x and ys\n// To plot your graph call Plotly.plot(element, ...)\n// Plotly examples and docs: https://plot.ly/javascript/", "legend": {"enabled": true}}');
INSERT INTO visualizations VALUES ('2019-04-15 15:33:51.971349+00', '2019-04-15 15:33:51.971349+00', 26, 'TABLE', 11, 'Table', '', '{}');
INSERT INTO visualizations VALUES ('2019-04-15 15:38:11.041151+00', '2019-04-15 15:38:11.041151+00', 27, 'TABLE', 12, 'Table', '', '{}');
INSERT INTO visualizations VALUES ('2019-04-15 15:48:50.253574+00', '2019-04-15 15:44:34.472+00', 28, 'PIVOT', 12, 'AWS Price - Region prices', '', '{"minColumns": 2, "cols": [], "rendererName": "Col Heatmap", "vals": ["ondemand"], "defaultRows": 10, "colOrder": "value_a_to_z", "menuLimit": 500, "rows": ["instance_type", "aws_region", "spot", "reserved1yr", "ondemand"], "showUI": true, "autoSortUnusedAttrs": false, "controls": {"enabled": true}, "hiddenFromAggregators": [], "unusedAttrsVertical": 85, "derivedAttributes": {}, "hiddenAttributes": [], "inclusions": {}, "aggregatorName": "First", "hiddenFromDragDrop": [], "sorters": {}, "defaultColumns": 3, "inclusionsInfo": {}, "rowOrder": "value_a_to_z", "exclusions": {}}');

INSERT INTO widgets VALUES ('2019-04-15 11:22:58.224865+00', '2019-04-12 12:41:04.679904+00', 7, 19, '', 1, '{"position": {"autoHeight": false, "sizeX": 3, "sizeY": 6, "maxSizeY": 1000, "maxSizeX": 6, "minSizeY": 5, "minSizeX": 1, "col": 3, "row": 0}, "isHidden": false, "parameterMappings": {}}', 1);
INSERT INTO widgets VALUES ('2019-04-15 11:22:58.226719+00', '2019-04-12 09:53:09.430846+00', 2, 7, '', 1, '{"position": {"autoHeight": false, "sizeX": 3, "sizeY": 4, "maxSizeY": 1000, "maxSizeX": 6, "minSizeY": 1, "minSizeX": 2, "col": 3, "row": 6}, "isHidden": false, "parameterMappings": {}}', 1);
INSERT INTO widgets VALUES ('2019-04-15 11:22:58.22479+00', '2019-04-11 21:24:28.72822+00', 1, 2, '', 1, '{"position": {"autoHeight": false, "sizeX": 3, "sizeY": 6, "maxSizeY": 1000, "maxSizeX": 6, "minSizeY": 1, "minSizeX": 2, "col": 0, "row": 0}, "isHidden": false, "parameterMappings": {}}', 1);
INSERT INTO widgets VALUES ('2019-04-15 11:22:58.252798+00', '2019-04-12 11:20:26.944552+00', 5, 15, '', 1, '{"position": {"autoHeight": false, "sizeX": 3, "sizeY": 5, "maxSizeY": 1000, "maxSizeX": 6, "minSizeY": 5, "minSizeX": 1, "col": 3, "row": 10}, "isHidden": false, "parameterMappings": {}}', 1);
INSERT INTO widgets VALUES ('2019-04-15 11:22:58.274712+00', '2019-04-15 11:21:14.752522+00', 10, 24, '', 1, '{"position": {"autoHeight": false, "sizeX": 3, "sizeY": 4, "maxSizeY": 1000, "maxSizeX": 6, "minSizeY": 1, "minSizeX": 2, "col": 0, "row": 6}, "isHidden": false, "parameterMappings": {}}', 1);
INSERT INTO widgets VALUES ('2019-04-15 12:50:12.860418+00', '2019-04-12 14:08:31.139072+00', 8, 23, '', 1, '{"position": {"autoHeight": false, "sizeX": 3, "sizeY": 8, "maxSizeY": 1000, "maxSizeX": 6, "minSizeY": 1, "minSizeX": 2, "col": 0, "row": 14}, "isHidden": false, "parameterMappings": {}}', 1);
INSERT INTO widgets VALUES ('2019-04-15 12:50:12.861+00', '2019-04-15 12:49:36.311888+00', 11, 10, '', 1, '{"position": {"autoHeight": false, "sizeX": 3, "sizeY": 4, "maxSizeY": 1000, "maxSizeX": 6, "minSizeY": 1, "minSizeX": 1, "col": 0, "row": 10}, "isHidden": false, "parameterMappings": {}}', 1);

