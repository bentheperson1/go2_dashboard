import logging

def get_logger():
    return logging.getLogger()


def setup_logging(verbose=False, include_dedup_filter=False,
                    always_print_logger_levels={logging.CRITICAL, logging.ERROR}):
    """Set up a basic streaming console handler at the root logger.

    Args:
        verbose (bool): if False (default) show messages at INFO level and above,
                        if True show messages at DEBUG level and above.
        include_dedup_filter (bool): If true, the logger includes a filter which
                                        will prevent repeated duplicated messages
                                        from being logged.
        always_print_logger_levels (set[logging.Level]): A set of logging levels which
                                                            any logged message at that level will
                                                            always be logged.
    """
    logger = get_logger()

    if verbose:
        level = logging.DEBUG
    else:
        level = logging.INFO

    if not logger.handlers:
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(level)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - [%(filename)s:%(funcName)s:%(lineno)d] - %(message)s')
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)

    logger.setLevel(level)

    if include_dedup_filter:
        class DeduplicationFilter(logging.Filter):
            def __init__(self):
                self.logged_messages = set()

            def filter(self, record):
                log_entry = (record.levelno, record.getMessage())
                if log_entry in self.logged_messages and record.levelno not in always_print_logger_levels:
                    return False
                self.logged_messages.add(log_entry)
                return True

        dedup_filter = DeduplicationFilter()
        logger.addFilter(dedup_filter)

