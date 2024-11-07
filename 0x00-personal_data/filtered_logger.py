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
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """ Filters values in incoming log records using filter_datum """
        record.msg = filter_datum(self.fields, self.REDACTION,
                                  record.getMessage(), self.SEPARATOR)
        return super(RedactingFormatter, self).format(record)


def get_logger() -> logging.Logger:
    """Configures and returns a logger for enabled."""
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    handler = logging.StreamHandler()
    handler.setFormatter(RedactingFormatter(fields=PII_FIELDS))
    logger.addHandler(handler)

    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """Creates and returns a connection to the personal data MySQL database."""
    return mysql.connector.connect(
        user=environ.get("PERSONAL_DATA_DB_USERNAME", "root"),
        password=environ.get("PERSONAL_DATA_DB_PASSWORD", ""),
        host=environ.get("PERSONAL_DATA_DB_HOST", "localhost"),
        database=environ.get("PERSONAL_DATA_DB_NAME")
    )


def main():
    """Connects to the database, retrieves and logs."""
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users;")
    column_names = [col[0] for col in cursor.description]
    logger = get_logger()

    for row in cursor:
        row_data = "; ".join(f"{name}={value}" for name,
                             value in zip(column_names, row))
        logger.info(row_data + ";")

    cursor.close()
    db.close()


if __name__ == '__main__':
    main()
