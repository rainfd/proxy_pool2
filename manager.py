import logging

import click

from proxygetter.scheduler import beat
from proxygetter.ext import proxydb
from proxygetter.logger import logger
from app import app


@click.group()
def cli():
    pass


@click.command()
def dropdb():
    proxydb.clear()


@click.command()
def crawl():
    beat()


@click.command()
def runserver():
    app.run(host='0.0.0.0', port=8000, debug=app.debug, threaded=True)


cli.add_command(runserver)
cli.add_command(crawl)
cli.add_command(dropdb)


if __name__ == '__main__':
    cli()
