import logging

def log(msg: str, name: str | None = None):
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s: %(message)s"
    )
    logger = logging.getLogger(name)

    return logger.info(msg)