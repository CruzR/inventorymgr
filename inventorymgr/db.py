"""
Database access module.

init_app()
    Install app-wide handlers for the database module.

init_db()
    Recreate the database.

init_db_command()
    Command line interface for recreating the database.

get_db()
    Return the DB connection for the current session, create it if necessary.

teardown_db()
    Close DB connection, called automatically when session ends.
"""

import sqlite3
from typing import cast, Optional

import click
from flask import current_app, Flask, g
from flask.cli import with_appcontext


def init_app(app: Flask) -> None:
    """Register necessary DB handlers on the application hooks."""
    app.teardown_appcontext(teardown_db)
    app.cli.add_command(init_db_command)


def init_db() -> None:
    """Recreate the database from its schema."""
    db = get_db()

    with current_app.open_resource('schema.sql') as schema_file:
        db.executescript(schema_file.read().decode('utf-8'))


@click.command('init-db')
@with_appcontext
def init_db_command() -> None:
    """CLI command to recreate the database from its schema."""
    init_db()
    click.echo('Initialized database.')


def get_db() -> sqlite3.Connection:
    """Return DB connection of the current session, create it if necessary."""
    db = g.get('db')
    if db is None:
        db = g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        db.row_factory = sqlite3.Row
    return cast(sqlite3.Connection, db)


def teardown_db(_: Optional[Exception]) -> None:
    """Close DB connection, called automatically at end of session."""
    db = g.pop('db', None)
    if db is not None:
        db.close()
