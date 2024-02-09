#!/usr/bin/env python3
"""
implemented filtered_logger
"""
import re
from typing import List


def filter_datum(fields: List[str], redaction: str, message: str, seperator: str) -> str:
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
