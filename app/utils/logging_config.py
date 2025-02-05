from loguru import logger

logger.add('app/utils/logging/main_logger.log', rotation='20 mb', level='DEBUG', format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}")