from sys import stderr

from loguru import logger


logger.add(
    stderr, format="[{time}] [{level}] [{file.name}:{line}]  {message}", level="DEBUG"
)
