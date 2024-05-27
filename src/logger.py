import logging

# Create a logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.WARNING)
console_format = logging.Formatter("%(name)s - %(levelname)s - %(message)s")
console_handler.setFormatter(console_format)
logger.addHandler(console_handler)
