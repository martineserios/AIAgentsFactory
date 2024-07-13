import sys

from loguru import logger


def setup_logger():
    # Remove the default logger
    logger.remove()
    
    # Add a new sink to stdout with a custom format
    logger.add(
        sys.stdout,
        colorize=True,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        level="INFO"
    )
    
    # Add a new sink to a file
    logger.add(
        "logs/app.log",
        rotation="500 MB",
        retention="10 days",
        compression="zip",
        level="DEBUG"
    )

    return logger

# Create a global logger instance
logger = setup_logger()