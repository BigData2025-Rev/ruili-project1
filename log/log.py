import logging
from logging.handlers import TimedRotatingFileHandler
import os

LOG_DIR = os.path.join(os.path.dirname(__file__), 'logs')
os.makedirs(LOG_DIR, exist_ok=True)

GENERAL_LOG_FILE = os.path.join(LOG_DIR, 'general.log')  # normal logger info path
MYSQL_LOG_FILE = os.path.join(LOG_DIR, 'mysql.log')  # mysql logger info

general_handler = TimedRotatingFileHandler(
    GENERAL_LOG_FILE, when='midnight', interval=1, backupCount=7, encoding='utf-8'
)
general_handler.setFormatter(
    logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
)

mysql_handler = TimedRotatingFileHandler(
    MYSQL_LOG_FILE, when='midnight', interval=1, backupCount=7, encoding='utf-8'
)
mysql_handler.setFormatter(
    logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
)

def get_logger(name, is_mysql=False):
    # return the logger due to the name
    logger = logging.getLogger(name)
    if not logger.handlers:
        if is_mysql: 
            # return a logger for mysql seperatly
            logger.addHandler(mysql_handler)
        else:
            # return a logger for all other modules
            logger.addHandler(general_handler) 
        logger.setLevel(logging.DEBUG) 
    return logger
