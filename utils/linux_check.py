#from utils import *
from utils.ssh import *
import config

"""
Convert the raw string data in a dict" with key/value
    :param long string in format key: value
    :return: dictonary key:value

"""


def __os_parse_ssh_info(data):
    dict_os_info = {}
    # parse meminfo

    # Convert all ssh result in a big text
    raw_info = ""
    for raw_row in data:
        if data[raw_row]:
            raw_info = raw_info + data[raw_row].decode()

    # Parsing the bigtext and converting it in a dict of key:values
    if raw_info:
        for line in raw_info.split('\n'):
            key = None
            valeu = None
            if "nr_mapped" in line:
                key = 'nr_mapped'
                value = line.strip().split()[1]
                dict_os_info[key] = value
            else:
                key = (line.strip().split()[0].split(':')[0]).lower()
                value = line.strip().split()[1]
                dict_os_info[key] = value

    return dict_os_info


"""
http://balodeamit.blogspot.com/2015/11/deep-dive-into-linux-memory-management.html
"""


def __calc_available_percent_memory(dict_mem_info):
    perc = None
    free_avaliable = dict()
    free_avaliable['available_kbytes_str'] = "{} kB".format(0)
    free_avaliable['available_kbytes'] = 0
    free_avaliable['avaliable_perc'] = 0.0
    try:
        if dict_mem_info:
                # if 'memavailable' in dict_mem_info.keys():
                #     total = float(dict_mem_info['memtotal'].replace('kB',''))
                #     available = float(dict_mem_info['memavailable'].replace('kB',''))
                # else: # OLD Kernel  / CentOS  6
                #     total = float(dict_mem_info['memtotal'].replace('kB',''))
                #     free = float(dict_mem_info['memfree'].replace('kB',''))
                #     perc = round(((free * 100) / total),2)

                # http://elixir.free-electrons.com/linux/v4.0.9/source/fs/proc/meminfo.c
                if 'low_watermark' in dict_mem_info.keys():
                    if dict_mem_info['low_watermark'] is not None or dict_mem_info['low_watermark'] > 0:
                        low_watermark = int(dict_mem_info['low_watermark'])
                        total = float(dict_mem_info['memtotal'].replace('kB', '')) * 1024
                        free = float(dict_mem_info['memfree'].replace('kB', '')) * 1024
                        sreclaimable = float(dict_mem_info['sreclaimable'].replace('kB', '')) * 1024
                        files_inactive = float(dict_mem_info['inactive(file)'].replace('kB', '')) * 1024
                        files_active = float(dict_mem_info['active(file)'].replace('kB', '')) * 1024
                        # Calculation...
                        available = free - low_watermark
                        pagecache = (files_active + files_inactive)
                        pagecache -= low_watermark
                        available += pagecache
                        available += sreclaimable - (sreclaimable / 2)

                        free_avaliable['available_kbytes_str'] = "{} kB".format(int(available / 1024))
                        free_avaliable['available_kbytes'] = int(available / 1024) # Bytes
                        free_avaliable['avaliable_perc'] = round(((available /total) * 100 ),2)
    except Exception as e:
        logger.debug("Error with memory calculation {}".format(e))
        pass
    return free_avaliable


"""
       Connect into the INSTANCE and get information about the real use of mememory .

       :param dict instance_details: connection information to perform a ssh connection
       :param bool single_line: Define if the commands will be in a single ssh query or one per commmand, use in debug only

       :return:
           a dict with avaliable memory in string, int and percentage. - {'availablekb_str': '3634833 kB', 'availablekb': 3634833, 'avaliable_perc': 89.97}

"""


def get_os_helthcheck(instance_details):
    single_line = instance_details['single_line']
    ssh_rules = config.SSH_RULES
    ssh_client = SSH(**ssh_rules)

    # low_watermark += (int(line) * PAGESIZE)  ||  sum(line) * 12k
    # Linux PAGESIZE = 4096
    os_commands = {
        'low_watermark': 'sum=0 && for low in $(cat /proc/zoneinfo | grep low |cut -d"w" -f2 | tr -d [:blank:]); do ((sum += low)) ; done;  echo "low_watermark: $((sum * 12))"',
        'meminfo': "cat /proc/meminfo | grep Mem",
        'mapped': "cat /proc/meminfo | grep -w \"Mapped\"",
        'nr_mapped': "cat /proc/vmstat  | grep nr_mapped",
        'mem_active_files': "cat /proc/meminfo | grep \"Active(file)\"",
        'mem_inactive_files': "cat /proc/meminfo | grep \"Inactive(file)\"",
        'sreclaimable': "cat /proc/meminfo | grep \"SReclaimable\"",
        'kernel_version': "echo \"Kernel: $(uname -r)\"",
        'linux_distro': "echo \"Distro: $(cat /etc/issue|head -1)\"",
    }

    # It mean: I will hit the server 1 time and concatenate the commands using a single big instruction or for each command i need to hit using ssh ?
    if single_line:
        single_line_row = ""
        for cmd in os_commands:
            single_line_row = str(single_line_row) + "{};".format(os_commands[cmd])
        os_commands.clear()
        os_commands['all_in_one'] = single_line_row

    dict_data = {}
    for cmd in os_commands:
        logger.debug("Getting {} on remote instance".format(cmd))
        # conn_details = {
        #     'srv_host': instance_details['InstanceHostName'],
        #     'srv_ip': instance_details['InstanceIP'],
        #     'srv_user': None,
        #     'srv_key_file_name': "{}.pem".format(instance_details['SSHKey']),
        #     'instance_id': instance_details['instance_id'],
        #     'aws_region': instance_details['aws_region'],
        #     'single_line': True,
        # }
        dict_data[cmd] = ssh_client.execute_command(remote_command=os_commands[cmd], connection_details=instance_details)

    dict_linux_info = __os_parse_ssh_info(dict_data)
    processed_mem_info = __calc_available_percent_memory(dict_linux_info)
    kernel = None
    Distro = None

    try:
        kernel = dict_linux_info['kernel']
        Distro = dict_linux_info['distro']
    except Exception as e :
        logger.error("Error {}".format(e))
        pass
    linux_info = {
        'available_kbytes_str':processed_mem_info['available_kbytes_str'],
        'available_kbytes':processed_mem_info['available_kbytes'],
        'avaliable_perc': processed_mem_info['avaliable_perc'],
        'kernel': kernel,
        'distro': Distro

    }
    return linux_info
