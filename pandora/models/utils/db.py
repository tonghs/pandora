import MySQLdb

from pandora import config
from pandora.extensions import db
from pandora.models.api_key.dao.api_key import ApiKeyDAO


tables = [
    ApiKeyDAO,
]


def create_tables():
    db.create_tables(tables)
    print("create tables done.")


def drop_tables(force=False):
    if not force and not config.DEBUG:
        print("❌ Only for DEBUG mode ❌")
        return
    db.drop_tables(tables)
    print("drop tables done.")


conn = MySQLdb.connect(
    host=config.DB_HOST,
    user=config.DB_USER,
    passwd=config.DB_PASSWORD,
)


def create_database():
    conn.cursor().execute(
        f'CREATE DATABASE IF NOT EXISTS {config.DB_NAME} '
        'DEFAULT CHARACTER SET utf8mb4 '
        'DEFAULT COLLATE utf8mb4_unicode_ci;',
    )
    print("create database done.")


def drop_database(force=False):
    if not force and not config.DEBUG:
        print("❌ Only for DEBUG mode ❌")
        return
    conn.cursor().execute(
        f'DROP DATABASE IF EXISTS {config.DB_NAME};')
    print("drop database done.")
