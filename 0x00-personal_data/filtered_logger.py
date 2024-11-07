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
