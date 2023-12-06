import logging


class IgnoreUnwantedLogs(logging.Filter):
    def filter(self, record):
        if "ALLOWED_HOSTS" in record.msg:
            return False
        return True
