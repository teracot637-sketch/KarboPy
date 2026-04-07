import logging

logger = logging.getLogger("karboai")
_logger_init = False


def setup_logging(enabled: bool = False) -> None:
    global _logger_init
    if _logger_init:
        return
    _logger_init = True

    logger.disabled = not enabled
    if enabled:
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        ))
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
