#!/usr/bin/env python3
"""filtered_logger"""
import re


def filter_datum(fields: str, redaction: str, message: str,
                 seperator: str) -> str:
    """returns the log message obfuscated"""
    for field in fields:
        message = re.sub(f'({field}=).*?{seperator}', r'\1{}{}'.
                         format(redaction, seperator), message)
    return message
