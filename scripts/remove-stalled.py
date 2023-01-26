#!/usr/bin/python3 -u

import logging

import click
from qbittorrentapi import Client

STALLED_STATES = ('stalledDL', 'metaDL')

def is_stalled(torrent) -> bool:
    return torrent.state in STALLED_STATES and torrent.time_active > 86400

@click.command()
@click.option(
    "--qb-host", envvar="QB_HOST",
    required=True,
    help="qBittorrent host"
)
@click.option(
    "--qb-username", envvar="QB_USERNAME",
    required=False,
    help="qBittorrent username"
)
@click.option(
    "--qb-password", envvar="QB_PASSWORD",
    required=False,
    help="qBittorrent password"
)

@click.pass_context
def cli(ctx, qb_host, qb_username, qb_password):
    ctx.obj = {
        "qb_host": qb_host,
        "qb_username": qb_username,
        "qb_password": qb_password,
    }

    # pylint: disable=no-value-for-parameter
    log = logger()

    client = Client(host=qb_host, username=qb_username, password=qb_password)

    for torrent in client.torrents.info():
        if is_stalled(torrent):
            log.info(f"Removing stalled torrent {torrent.name}")
            torrent.delete(delete_files=True)

@click.pass_context
def logger(ctx):
    """Set up logging
    """
    logging.basicConfig(
        level=logging.INFO ,
        format="%(asctime)s %(name)s %(levelname)-8s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    return logging.getLogger("Tag Tracker Errors")

if __name__ == "__main__":
    # pylint: disable=no-value-for-parameter
    cli()
