from flask import Flask
from flask import request
import logging.handlers
from python_json_config import ConfigBuilder
import sys
import tasks

app = Flask(__name__)

@app.route('/postjson', methods=['POST'])
def post():
    content = request.get_json()
    print(content)
    print(content['id'])
    print(content['name'])
    return 'JSON posted'

# define path to config file
#config_file = sys.argv[1:][0]
config_file = '.\config.json'

# create config parser
builder = ConfigBuilder()

# parse config
if tasks.check_file_exists(config_file):
    config = builder.parse_config(config_file)
else:
    print("No config file")
    sys.exit(1)

app.run(host=config.ip_address, port=config.port)

# create logger
logger = logging.getLogger(config.site_name)
logger.setLevel(logging.DEBUG)

# create file handler which logs messages
fh = logging.handlers.RotatingFileHandler(config.logpath + config.site_name + '.log', maxBytes=int(config.log_size_bytes),
                                          backupCount=int(config.log_file_count))
#fh = logging.FileHandler(config.logpath + config.site_name + '.log')
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
