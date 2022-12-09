from daily_panda_task_agent import Daily_Panda_Task_Agent
import yaml

def assign_config_values():
    daily_task = Daily_Panda_Task_Agent()
    with open("/media/data/fastAPI/PandaServiceDesk/panda_task_agent/Task_Agent_Config.yml", "r") as ymlfile:
        cfg = yaml.safe_load(ymlfile)
        #print(cfg)

    # Panda Task Agent config
    daily_task.task_type = cfg["task_agent"]["task_type"]
    daily_task.store_code = cfg["task_agent"]["store_code"]
    daily_task.database_name = cfg["task_agent"]["database_name"]
    daily_task.BASE_URL = cfg["task_agent"]["base_url"]
    daily_task.REMOTE_BASE_URL = cfg["task_agent"]["remote_base_url"]

    # Sqldump config
    daily_task.dump_path = cfg["sqldump_cfg"]["dump_path"]
    daily_task.d_hostname = cfg["sqldump_cfg"]["hostname"]
    daily_task.d_port = cfg["sqldump_cfg"]["port"]
    daily_task.d_username = cfg["sqldump_cfg"]["username"]
    daily_task.d_pwd = cfg["sqldump_cfg"]["passwd"]

    # COMPRESS/DECOMPRESS config
    daily_task.zip_store_path = cfg["zip_cfg"]["zip_store_path"]
    daily_task.unzip_store_path = cfg["zip_cfg"]["unzip_store_path"]

    # SFTP congfig
    daily_task.sftp_hostname = cfg["sftp_cfg"]["hostname"]
    daily_task.sftp_username = cfg["sftp_cfg"]["username"]
    daily_task.sftp_password = cfg["sftp_cfg"]["password"]
    daily_task.sftp_remote_path = cfg["sftp_cfg"]["sftp_remote_path"]
    daily_task.sftp_port = cfg["sftp_cfg"]["port"]

    ymlfile.close()

    return daily_task

# Reference Link to set up Passwordless SFTP or SSH
# https://www.tecmint.com/ssh-passwordless-login-using-ssh-keygen-in-5-easy-steps
