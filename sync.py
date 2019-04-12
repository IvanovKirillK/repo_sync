import logging.handlers
import os
from python_json_config import ConfigBuilder
import sys
import tasks
import json

# define path to config file
# config_file = sys.argv[1:][0]
config_file = './config.json'

# create config parser
builder = ConfigBuilder()

# parse config
if tasks.check_file_exists(config_file):
    config = builder.parse_config(config_file)
else:
    print("No config file")
    sys.exit(1)

# check log dir exists
if not tasks.check_dir_exists(config.log.path):
    os.makedirs(config.log.path)

# create logger
logger = logging.getLogger("repo_sync")
logger.setLevel(logging.DEBUG)

# create file handler which logs messages
fh = logging.handlers.RotatingFileHandler(config.log.path + config.log.filename, maxBytes=int(config.log.size_bytes),
                                          backupCount=int(config.log.file_count))
fh = logging.FileHandler(config.log.path + config.log.filename)
fh.setLevel(logging.DEBUG)

# create console handler
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)

# add the handlers to the logger
logger.addHandler(fh)
logger.addHandler(ch)

logger.info('######################## Starting new job ########################')
logger.info('Initial config read')

with open(config_file, 'r', encoding='utf8') as f:
    config = json.load(f)

# getlast commit from main repo branch
logger.info('Trying to get last commit for master branch ')
master_branch_commit = tasks.get_last_commit(config['master'], logger)
logger.info('Got last commit for master branch ')
logger.info(master_branch_commit)
logger.info('Got last slave branch ')
# getLast commit from slave repo branch
slave_branch_commit = tasks.get_last_commit(config['slave'], logger)
logger.info('Got last commit for slave branch ')
logger.info(slave_branch_commit)
# compare and sync branches
if master_branch_commit == slave_branch_commit:
    logger.info('branches are equal, do nothing')
elif master_branch_commit != slave_branch_commit:
    tasks.sync_branches(config['master'], logger)
# write data to log
tasks.write_to_Influx(config['monitoring'], 1, logger)
logger.info('Job done, see ya next time!')
