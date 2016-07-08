#!/usr/bin/env python
# -*- coding: utf-8 -*-
from settings import logging
from flask.ext.script import Manager

from app import app
from models import create_all
from specification import import_specification_by_name
from specification import select_all_from_specification
from importer import import_data_files

logger = logging.getLogger(__name__)

manager = Manager(app)


@manager.command
def init_database():
    """
    Init static database
    """
    logger.info("Setting up database start")
    create_all()
    logger.info("Setting up database done")


@manager.command
def import_files():
    """
    Import all txt data files located in data folder
    """
    logger.info("Import files start")
    import_data_files()
    logger.info("Import files done")


@manager.option('-f', '--file', dest='filename', help='Specification file name')
def import_specification(filename):
    """
    Import specification
    """
    logger.info("Import speficication start")
    import_specification_by_name(filename)
    logger.info("Import speficication done")


@manager.option('-f', '--file', dest='filename', help='Specification file name')
def select_all(filename):
    """
    Select all rows from given speficiation table like select * from
    """
    logger.info("Select All start")
    select_all_from_specification(filename)
    logger.info("Select All done")


if __name__ == "__main__":
    manager.run()
