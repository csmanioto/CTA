
# App imports
from utils import *
import config

logger = log.init_logger(__name__, testing_mode=config.DEBUG_MODE)


class SSH(object):
    setting_profile = None
    ssh_key_folder = None

    def __init__(self, ssh_key_folder = None, ssh_connection_method = None, ssh_tcp_port = 22,  ssh_timeout_seconds=10, ssh_banner_timeout_seconds = 30, ssh_compress=False, ssh_bastion=None):
        self.allow_agent = True
        self.look_for_keys = False
        self.SSH_ALTERNATIVE_METHOD = True


        self.ssh_connection_method = ssh_connection_method
        self.ssh_timeout = ssh_timeout_seconds
        self.ssh_banner_timeout = ssh_banner_timeout_seconds
        self.compress = ssh_compress
        self.ssh_key_folder = ssh_key_folder
        self.ssh_bastion = ssh_bastion
        logger.debug("SSH Initialized with successful")

    def _ssh_proxy_command_builder(self, bastion_key_filename=None, bastion_server=None, bastion_user=None,
                                   bastion_password=None):
        proxycommand = None
        proxy_pre_command = "ssh -o 'StrictHostKeyChecking no' -W %h:%p {} {}@{} 2> /dev/null"

        if bastion_server:
            if bastion_key_filename:
                bastion_key_filename = "-i {}".format(bastion_key_filename)
                proxy_pre_command = proxy_pre_command.format(bastion_key_filename, bastion_user, bastion_server)
                if self.SSH_ALTERNATIVE_METHOD:
                    proxycommand = proxy_pre_command
                #else:
                #    proxycommand = paramiko.ProxyCommand(proxy_pre_command)

        # if self.setting_profile['ssh_bastion']:
        #     bastion_key_filename = "{}/{}".format(self.ssh_key_folder,self.setting_profile['ssh_bastion_key_file'])
        #     bastion_user = self.setting_profile['ssh_bastion_user']
        #     bastion_server = self.setting_profile['ssh_bastion_host']
        #     if bastion_key_filename:
        #         bastion_key_filename = "-i {}".format(bastion_key_filename)
        #     proxy_pre_command = proxy_pre_command.format(bastion_key_filename, bastion_user, bastion_server)
        #     logger.debug("Using bastion host {}".format(proxy_pre_command))
        #     proxycommand = proxy_pre_command
        return proxycommand

    def __execute_using_os(self, ssh_config, remote_command, proxycommand=None, auto_connect=True):
        return_command = None
        SSH_USER_LIST = ['ec2-user', 'centos', 'root']

        # if 'ssh_user_options' in config.SSH_RULES:
        #     SSH_USER_LIST = config.SSH_RULES['ssh_user_options']

        if ssh_config['username'] is not None:
            SSH_USER_LIST = [ssh_config['username']] # Replace the constant list with a single user.

        for ssh_user in SSH_USER_LIST: ### Try all users available to connect...
            pkey = None
            ssh_pre_cmd = "ssh {} {}@{} -o 'StrictHostKeyChecking no'"
            try:
                if ssh_config['pkey']:
                    pkey = "-i {}".format(ssh_config['pkey'])

                if proxycommand:
                    ssh_pre_cmd = ssh_pre_cmd + " -o \"proxycommand {} \" '{}'"
                    ssh_cmd = ssh_pre_cmd.format(pkey, ssh_user,  ssh_config['hostname'], proxycommand, remote_command)
                else:
                    ssh_pre_cmd = ssh_pre_cmd + " '{}'"
                    ssh_cmd = ssh_pre_cmd.format(pkey, ssh_user,  ssh_config['hostname'], remote_command)
                logger.info("Executing ssh commando on host {}".format(ssh_config['hostname']))
                logger.debug("Executing ssh command {}".format(ssh_cmd))
                return_command = tools.run_os_cmd(ssh_cmd)
                le = len(return_command)
                if len(return_command) > 10:
                    logger.info("Not was possible perform a ssh with user {} trying other option".format(ssh_user))
                    break
            except Exception as e:
                logger.error("Error on execute ssh thoryght the OS {}".format(e))
                logger.info("Trying using another login user...")
                pass
        return return_command


    # def __execute_using_paramiko(self, ssh_config, remote_command, proxycommand=None, auto_connect=True):
    #     data = None
    #     if proxycommand:
    #         sock = paramiko.ProxyCommand(proxycommand)
    #         sock.settimeout(self.ssh_banner_timeout)
    #         ssh_config['sock'] = socket
    #     try:
    #         logger.debug("Paramiko version {}".format(paramiko.__version__))
    #         self.ssh_config['pkey'] = paramiko.RSAKey.from_private_key_file(ssh_config['pkey'])
    #         self.ssh_client = paramiko.SSHClient()
    #         self.ssh_client.load_system_host_keys()
    #         self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    #         if auto_connect:
    #             self.ssh_client.connect(**self.ssh_config)
    #
    #         logger.info("SSH - Extraction information on server {} ".format(ssh_config['hostname']))
    #         stdin, stdout, stderr = self.ssh_client.exec_command(remote_command, get_pty=True, timeout=self.ssh_timeout)
    #         stdin.flush()
    #         data = ""
    #         for line in iter(stdout.readline, ""):
    #             data += line
    #         logger.debug("SSH closing the session")
    #         if auto_connect:
    #             self.ssh_client.close()
    #     except:
    #         pass
    #     return data
    #
    #
    # def connect(self):
    #     try:
    #         logger.debug("Connectin on server")
    #         self.ssh_client.connect(**self.ssh_config)
    #         return True
    #     except Exception as e:
    #         logger.error("Fail on connect ssh")
    #
    # def desconect(self):
    #     try:
    #         logger.debug("Desconnection on ssh server")
    #         self.ssh_client.close()
    #         return True
    #     except Exception as e:
    #         logger.error("Fail on desconect ssh")


    def execute_command(self, remote_command, connection_details, auto_connect=False):
        srv_password = None
        srv_user = None
        proxycommand = None
        data = None
        srv_key_file_name = None

        if config.SSH_RULES['ssh_connection_method'].upper() == 'HOSTNAME':
            srv_host = connection_details['srv_host']
        else:
            srv_host = connection_details['srv_ip']

        srv_tcp_port = config.SSH_RULES['ssh_tcp_port']
        raw_srv_key_file_name = connection_details['srv_key_file_name']
        ssh_config = {
            'hostname': srv_host,
            'port': srv_tcp_port,
            'username': srv_user,
            'compress': self.compress,
            'look_for_keys': self.look_for_keys,
            'allow_agent': self.allow_agent,
            'banner_timeout': self.ssh_banner_timeout
        }

        if srv_password is not None:
            ssh_config['password'] = srv_password

        if raw_srv_key_file_name is not None:
            srv_key_file_name = "{}/{}".format(self.ssh_key_folder, raw_srv_key_file_name)
            if tools.check_is_file_exist(srv_key_file_name):
                ssh_config['pkey'] = srv_key_file_name
            else:
                logger.error("PEM FILE {} NOT FOUND, CANCELING SSH COMMAND ".format(srv_key_file_name))
                return None

        ######
        # BASTION LOGIC
        ######
        bastion_key_filename = None,
        bastion_server = None
        bastion_user = None
        bastion_password = None
        ssh_config['sock'] = None

        if 'ssh_bastion' in config.SSH_RULES:
            if config.SSH_RULES['ssh_bastion']['enable']:
                if not config.SSH_RULES['ssh_bastion']['ssh_bastion_by_patterns']:
                    bastion_key_filename = config.SSH_RULES['ssh_bastion']['ssh_bastion_key_file']
                    bastion_user = config.SSH_RULES['ssh_bastion']['ssh_bastion_user']
                    bastion_server = config.SSH_RULES['ssh_bastion']['ssh_bastion_host']
                else:  # We have a custom rule here with base a some rules...
                    for rule in config.SSH_RULES['ssh_bastion']['ssh_bastion_patterns']:
                        pattern_word = "{}.pem".format(rule['pattern_word'])
                        #srv_host_name = connection_details['srv_host']
                        #if (pattern_word in srv_host_name) or (pattern_word in srv_key_file_name):
                        if pattern_word == raw_srv_key_file_name:
                            bastion_key_filename = "{}/{}".format(self.ssh_key_folder, rule['ssh_bastion_key_file'])
                            bastion_user = rule['ssh_bastion_user']
                            bastion_server = rule['ssh_bastion_host']
                            break
                proxycommand = self._ssh_proxy_command_builder(bastion_key_filename, bastion_server, bastion_user, bastion_password)
                ssh_config['sock'] = proxycommand


        try:
            logger.debug("Performaing connection ssh with parameters {}".format(ssh_config))
            if self.SSH_ALTERNATIVE_METHOD:
               #logger.debug("Going to alternative way to get data - using ssh of OS")
                data = self.__execute_using_os(ssh_config, remote_command, proxycommand, auto_connect)
            #else:
            #    logger.info("Going to python paramiko way to get data")
            #    data = self.__execute_using_paramiko(ssh_config, remote_command, proxycommand)
            return data
        except Exception as authe:
            logger.warning("Error to user {}, ssh_key {}, {}".format(srv_user, srv_key_file_name, authe))

