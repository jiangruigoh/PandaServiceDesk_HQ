# Main Runner Local to Remote
"""
SQLDUMP -> COMPRESSION -> SFTP
Version No: 1
Release Date: 23 September 2021 
KKSC
"""

from daily_task_backup import sqldump_run
from daily_task_compressor import compress_run
from daily_task_SFTP import sftp_run

sqldump_run()
compress_run()
sftp_run()
