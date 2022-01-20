import logging
import os
from logging.handlers import TimedRotatingFileHandler
from common.config import LOGGING_LEVEL

log_server = logging.getLogger('server')
server_formatter = logging.Formatter("%(asctime)s - %(levelname)8s - %(message)s  ")
server_path = os.path.dirname(os.path.abspath(__file__))
server_path = os.path.join(server_path, 'server.log')
file_hand = TimedRotatingFileHandler(server_path, encoding='utf8', interval=1, when='D')
file_hand.setFormatter(server_formatter)
log_server.addHandler(file_hand)
log_server.setLevel(LOGGING_LEVEL)

log_client = logging.getLogger('client')
client_path = os.path.dirname(os.path.abspath(__file__))
client_path = os.path.join(client_path, 'client.log')
file_hand = logging.FileHandler(client_path, encoding='utf8')
file_hand.setFormatter(server_formatter)
log_client.addHandler(file_hand)
log_client.setLevel(LOGGING_LEVEL)

