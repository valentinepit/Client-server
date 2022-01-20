import logging

log = logging.getLogger('app.main')

formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s  ")

file_hand = logging.FileHandler("client.log", encoding='utf-8')

file_hand.setFormatter(formatter)

log.addHandler(file_hand)

log.setLevel(logging.DEBUG)
