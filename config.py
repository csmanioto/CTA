DEBUG_MODE = False
API_TCP_PORT = 8080
API_INTERFACE = "0.0.0.0"

# DATABASE settings
DATABASE_URI = 'postgresql+psycopg2://scott:tigger@192.168.172.131:5432/tracker'

DATABASE_TRACK_MODIFICATIONS = True

SSH_RULES = {
        "ssh_key_folder": "/Users/smaniottoc/.ssh/taxi",
        "ssh_connection_method": "hostname",  # other option would be "ip"
        "ssh_timeout_seconds": 5,
        "ssh_banner_timeout_seconds": 30,
        "ssh_tcp_port": 22,
        "ssh_compress": False,
        "ssh_bastion": {
            "enable": True,
            "ssh_bastion_host": None,
            "ssh_bastion_tcp_port": 22,
            "ssh_bastion_user": None,
            "ssh_bastion_key_file": None,
            "ssh_bastion_by_patterns": True, # Use it when you have multiples bastions for multiples enviroments.
            "ssh_bastion_patterns":[
                {
                    "pattern_word": "qa", # if pem key == qa.pem
                    "ssh_bastion_host": "mgmt.eu-west-1-qa.ext.qa.someonedrive.me",
                    "ssh_bastion_tcp_port": 22,
                    "ssh_bastion_user": "centos",
                    "ssh_bastion_key_file": "qa.pem"
                },
                {
                    "pattern_word": "cybageqa",
                    "ssh_bastion_host": "mgmt.us-east-2-cybageqa.ext.cybageqa.someonedrive.me",
                    "ssh_bastion_tcp_port": 22,
                    "ssh_bastion_user": "centos",
                    "ssh_bastion_key_file": "cybageqa.pem"
                },
                {
                    "pattern_word": "newprod",
                    "ssh_bastion_host": "mgmt.eu-west-1-prod.ext.rideways.com",
                    "ssh_bastion_tcp_port": 22,
                    "ssh_bastion_user": "centos",
                    "ssh_bastion_key_file": "newprod.pem"
                },
                {
                    "pattern_word": "dev",
                    "ssh_bastion_host": "mgmt.us-west-2-dev.ext.dev.someonedrive.me",
                    "ssh_bastion_tcp_port": 22,
                    "ssh_bastion_user": "centos",
                    "ssh_bastion_key_file": "dev.pem"
                }
            ]
        }
}

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
