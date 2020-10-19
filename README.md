## Table of Content.

- [About the project](#about-the-project)
- [How it's work](#how-it-s-work)
- [Version 1 - Re:Dash as report.](#version-1---re-dash-as-report)
  * [Roadmap](#roadmap)
    + [Instances Price](#instances-price)
    + [Reserved x OnDemand](#reserved-x-ondemand)
    + [Spot Instance x OnDemand](#spot-instance-x-ondemand)
    + [Regions](#regions)
    + [RDS and Aurora.](#rds-and-aurora)
- [Instalation](#instalation)
    + [PEM KEY Files](#pem-key-files)
    + [AWS Credential](#aws-credential)
    + [Python](#python)
    + [Database](#database)
    + [Re:Dash](#re-dash)
- [How rum it.](#how-rum-it)
  * [Crontab](#crontab)
- [Contact](#contact)
- [License](#license)



## About the project 

**The Clould Tracker cost API (CTA)** is an Rest API (At least in v2) that advise you about optimisations that you should to consider. 

This version, we are using [Re:Dash(https://redash.io ) as report tool.


## How it's work

 
CTA perform a scan getting details from AWS about all EC2 instances in ALL AWS' regions and get details 
from cloudwatch and using SSH get details about memory, kernel version, distro and others. 

Crossing information from cloudwatch + OS details, CTA can determine if an instance is a true "low utilization"
and also create a comparision between others model of prices.  

## Version 1 - Re:Dash as report.
![ScreenShot](screenshot.png)


### Roadmap
- API for read data: 
    http://cta/v2/instance_price?m4.xlarge
    will return the cheapest region fot that instance
    (this is available on Re:Dash) 
  
    #### Instances Price 
    http://cta/v2/price
    will return the aws prices for all instances that we have in our enviorment.
    (this is available on Re:Dash)
    
    #### Reserved x OnDemand
    http://cta/v2/reserved
    will return reserved price 1 year without upfront for all ondemand instance type that we have.
    (this is available on Re:Dash)
    
    http://cta/v2/reserved?env="QADEV"
    the same but only for QADEV or other environment that you have flagged on config.py
    
    #### Spot Instance x OnDemand
    http://cta/v2/spot
    will return spot price for all ondemand instances included on AS group that we have.
    (this is available on Re:Dash)
    
    http://cta.bookinggo.com/v2/spot?env="QADEV"
    the same but only for QADEV or other environment that you have flagged on config.py
    
    #### Regions
    http://cta/v2/regions
    will return regions that we have instances deployed there.
    (this is available on Re:Dash)
    
    http://cta/v2/regions?env="QADEV"
    the same but only for QADEV or other environment that you have flagged on config.py
    
    #### RDS and Aurora. 
    Introducing advising about RDS and Aurora as well. 
    


## Instalation 

Below we are going to explain the usage and installation of CTA.

#### PEM KEY Files
Is necessary all pem key files of instances that the CTA need to ssh check. Without it, the project will work but the 
accurase get injures because won't be possivel details from memory.
 
You can inform the pem files path using config.py using key ssh_key_folder

````python
        "ssh_key_folder": "/opt/taxi/ssh_pem",
````

#### AWS Credential

You can use aws creditial profile or using a traditional access_key for each type of environment using the key

```python
AWS_CREDENTIAL_CONFIG = [
    {
        "credential":"dev/qa", # If nothing will be use the default aws credential or aws_access_key_id
        "enable": True,
        "aws_access_key_id": None,
        "aws_secret_access_key": None,
        "profile": "qadev"
    },
    {
        "credential": "prod",
        "enable": False,
        "aws_access_key_id": None,
        "aws_secret_access_key": None,
        "profile": "prod"
    },
]
```

**IMPORTANT!**
"profile" key contains the PROFILE(kind of workload) value used on reports. So if you have more environments and needs to tracking it,
create more credential details for the new environment and tag it using the key "profile". During the report (or with ?env="")
always use scapital letter 


#### Python 
python3 is required ;) 

````bash
cd /projectpath/
pip3 -r requirements.txt
echo "alias flask='python3 -m flask'" >> ~/.bashrc
````

#### Database
CTA uses PostgreSQL.

- You must to create a database with you like name, example tracker. Can be RDS, PostgreSQL 9, 10. 
- Configure the key **DATABASE_URI** on config.py with connections details

```python
DATABASE_URI = 'postgresql+psycopg2://scott:tigger@127.0.0.0.1:5432/tracker'

```
- Execute the flask command **resetdb** and it will creating all tables. 

````bash
cd /projectpath && flask resetdb
```` 

#### Re:Dash
============

- Following the instalation details from redash.io, configure the first credentials. 
- import file redash.sql into Re:Dash's database 
- Configure PostgreSQL connection Details on Re:Dash. 


## How rum it. 

The data must to be collect at least once a day and feeding the Database with fresh details.

Our sugggestion is using it at least 6x day (24 hours) for create a good history of stopped, terminated and running instances. It's
possible to colect it using cloudwatch but tracking the state change we can create more reports in terms of advising price. 

For running it we just need to execute the command shell:

````bash
cd /projectpath && flask scan_aws
```` 

### Crontab

This example, execute the command every 4 hours
````bash
* */4 * * * cd /projectpath/ && flask scan_aws >/dev/null 2>&1
````
<!-- CONTACT -->
## Contact
BookingGO - Product Service Team 3 (Taxi)


<!-- LICENSE -->
## License
Distributed under the MIT License. See `LICENSE` for more information.