#!/usr/bin/env python3
"""
implements a filtered_logger
"""
import re
from typing import List


def filter_datum(fields: List[str], redaction: str, message: str,
                 seperator: str) -> str:
    """returns the log message obfuscated
    Args:
        fields (list of str): a list of strings representing all fields to
            obfuscate
        message (str): a string representing the log line
        seperator (str): a string representing by which character is seperating
            all fields in the log line 'message'
    Return:
        obfuscated string
    """
    for field in fields:
        message = re.sub(f'({field}=).*?{seperator}', r'\1{}'.
                         format(redaction), message)
    return message
