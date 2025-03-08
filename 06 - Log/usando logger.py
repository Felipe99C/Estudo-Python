
from loguru import logger

logger.add(r"D:\Estudos\Python\Estudo-Python\06 - Log\meus_logs.log", format="{time} {level} {message} {file} {line}", level="CRITICAL")

logger.debug("Um aviso para o desenvolvedor")
logger.info("Apenas uma informação importante sobre um processo")
logger.warning("Um aviso para o usuário, de algo que vai parar no futuro")
logger.error("Um erro que não para a aplicação, uma falha")
logger.critical("Um erro que para a aplicação, uma falha crítica")