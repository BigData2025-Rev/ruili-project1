import logging
from logging.handlers import TimedRotatingFileHandler
import os
from filelock import FileLock

LOG_DIR = os.path.join(os.path.dirname(__file__), 'logs')
os.makedirs(LOG_DIR, exist_ok=True)

GENERAL_LOG_FILE = os.path.join(LOG_DIR, 'general.log')  # normal logger info path
MYSQL_LOG_FILE = os.path.join(LOG_DIR, 'mysql.log')  # mysql logger info

general_handler = TimedRotatingFileHandler(
    GENERAL_LOG_FILE, when='midnight', interval=1, backupCount=7, encoding='utf-8', delay=True
)
general_handler.setFormatter(
    logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
)

mysql_handler = TimedRotatingFileHandler(
    MYSQL_LOG_FILE, when='midnight', interval=1, backupCount=7, encoding='utf-8', delay=True
)
mysql_handler.setFormatter(
    logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
)

def get_logger(name, is_mysql=False):
    logger = logging.getLogger(name)
    if not any(isinstance(handler, TimedRotatingFileHandler) for handler in logger.handlers):
        lock_file = os.path.join(LOG_DIR, 'log.lock')  # 定义锁文件
        with FileLock(lock_file):  # 确保线程安全
            if is_mysql:
                logger.addHandler(mysql_handler)
            else:
                logger.addHandler(general_handler)
        logger.setLevel(logging.DEBUG)
    return logger
