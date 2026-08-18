import logging
import logging.handlers
from .config import app_data_dir

def setup_logging(verbose: bool = False, log_to_file: bool = True):
    """Configura el sistema de logging para GuardianX."""
    level = logging.DEBUG if verbose else logging.INFO
    logger = logging.getLogger("guardianx")
    logger.setLevel(level)
    
    if logger.hasHandlers():
        logger.handlers.clear()

    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', '%Y-%m-%d %H:%M:%S')
    
    ch = logging.StreamHandler()
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    
    if log_to_file:
        log_file = app_data_dir() / "guardianx.log"
        fh = logging.handlers.RotatingFileHandler(log_file, maxBytes=1_000_000, backupCount=3, encoding='utf-8')
        fh.setFormatter(formatter)
        logger.addHandler(fh)
        
    return logger
