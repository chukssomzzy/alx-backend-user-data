#!/usr/bin/env python3
"""filtered_logger"""
import re
from typing import List


def filter_datum(fields: List[str], redaction: str, message: str,
                 seperator: str) -> str:
    """returns the log message obfuscated"""
    for field in fields:
        message = re.sub(f'({field}=).*?{seperator}', r'\1{}'.
                         format(redaction), message)
    return message
