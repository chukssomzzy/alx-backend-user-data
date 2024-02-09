#!/usr/bin/env python3
"""
implemented filtered_logger
"""
import re
from typing import List, Tuple, Union
import logging

PII_FIELDS = ('email', 'phone', 'ssn', 'password', 'ip',)


def filter_datum(fields: List[str], redaction: str, message: str,
                 seperator: Union[str, None] = ';') -> str:
    """returns the log message obfuscated
    Args:
        fields (list of str): a list of strings representing all fields to
        obfuscate
        redaction (str): a string representing by what the field will be
        obfucated
        message (str): a string representing by which character is seperating
        all fields in the log line message
        seperator (str): a string representing by which character is separating
        all fields in the log line(message)
    Returns:
        obfuscated str
    """
    for field in fields:
        message = re.sub('({}=).*?{}'.format(field, seperator),
                         r'\1{}{}'.format(redaction, seperator), message)
    return message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """Initialize formatter
        Args:
            fields (list of string): a list of filter fields
        """
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """filters values in incoming log records using filter_datum
        Args:
            record (loggingrecord): A log record
        """
        message = super().format(record)
        message = filter_datum(self.fields, self.REDACTION, message,
                               self.SEPARATOR)
        return message


def get_logger() -> logging.Logger:
    """
    takes no arguments and returns a 'logging.Logger' object
    """
    logger = logging.Logger('user_data')
    logger.setLevel(logging.DEBUG)
    sh = logging.StreamHandler()
    sh.setLevel(logging.INFO)
    fh = RedactingFormatter(fields=PII_FIELDS)
    sh.setFormatter(fh)
    logger.addHandler(sh)
    return logger
