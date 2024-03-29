#!/usr/bin/env python3
"""
implemented filtered_logger
"""
import re
from typing import List, Union
import logging
from mysql.connector import connection
import mysql.connector
from os import getenv

PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')


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
    logger = logging.getLogger('user_data')
    logger.propagate = False
    logger.setLevel(logging.INFO)
    sh = logging.StreamHandler()
    sh.setLevel(logging.INFO)
    fh = RedactingFormatter(fields=PII_FIELDS)
    sh.setFormatter(fh)
    logger.addHandler(sh)
    return logger


def get_db() -> connection.MySQLConnection:
    """
    Returns a connection to a database
    Returns:
        mysql connection
    """
    conn = None
    try:
        conn = connection.MySQLConnection(
            username=getenv('PERSONAL_DATA_DB_USERNAME', 'root'),
            password=getenv('PERSONAL_DATA_DB_PASSWORD', ''),
            host=getenv('PERSONAL_DATA_DB_HOST', 'localhost'),
            database=getenv('PERSONAL_DATA_DB_NAME')
        )
    except (mysql.connector.Error, IOError):
        return connection.MySQLConnection()
    return conn


def main():
    """
    Starting point for program execution
    """
    db = get_db()
    logger = get_logger()
    if db and db.is_connected():
        with db.cursor() as cursor:
            cursor.execute("SELECT * FROM users")
            rows = cursor.fetchall()
            fields = cursor.column_names
            for row in rows:
                logger.info(";".join("{}={}".format(field, val)
                                     for field, val in zip(fields, row)))
    db.close()


if __name__ == "__main__":
    main()
