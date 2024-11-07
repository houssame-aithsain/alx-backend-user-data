#!/usr/bin/env python3
"""Module for managing and logging sensitive personal data with redaction."""

import re
import logging
import mysql.connector
from os import environ
from typing import List


PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def filter_datum(fields: List[str],
                 redaction: str, message: str, separator: str) -> str:
    """Replaces sensitive data fields in a log."""
    pattern = f"({'|'.join(fields)})=.*?{separator}"
    return re.sub(pattern,
                  lambda x: f"{x.group(1)}={redaction}{separator}", message)


class RedactingFormatter(logging.Formatter):
    """Formatter that redacts specified fields in log messages."""

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super().__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        record.msg = filter_datum(self.fields, self.REDACTION,
                                  record.getMessage(), self.SEPARATOR)
        return super().format(record)
