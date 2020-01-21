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

import click
from flask.cli import with_appcontext
from flask_sqlalchemy import SQLAlchemy  # type: ignore


db = SQLAlchemy()


@click.command("init-db")
@with_appcontext
def init_db_command() -> None:
    """CLI command to recreate the database from its schema."""
    db.create_all()
    click.echo("Initialized database.")
