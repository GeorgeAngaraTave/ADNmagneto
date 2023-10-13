#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
import logging
import os
import sys
import time

import click
import firebase_admin
from firebase_admin import credentials
from google.cloud import firestore

SDK_ENV = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS', None)

if not SDK_ENV:
    print("Could not automatically determine credentials.")
    print("Please set GOOGLE_APPLICATION_CREDENTIALS or explicitly create credentials and re-run the application.")
    print("For more information, please see https://cloud.google.com/docs/authentication/getting-started")
    sys.exit()

cred = credentials.ApplicationDefault()
firebase_admin.initialize_app(cred)

try:
    db = firestore.Client()
except Exception as e:
    print("Firestore Client Exception:", e)
    raise e
    sys.exit()

def total_file_lines(filename):
    with open(filename) as f:
        return sum(1 for line in f)

@click.command(context_settings=dict(
    ignore_unknown_options=True,
))

@click.option('-f', '--file', default=None, required=True, type=click.Path(exists=True, readable=True), help='file to import.')
@click.option('-c', '--collection', default=None, required=True, help='Collection name')
@click.option('-a', '--auto', default=True, help='Specifying auto generated Document ID. (default: yes)')
@click.option('-p', '--prefix', default=None, help='Collection prefix (default: None)')
@click.option('-d', '--delimiter', default=',', help='default file delimiter (default: ;)')

def command_line(file, collection, auto, prefix, delimiter):
    """allow import data to Firestore."""
    click.clear()
    click.echo()
    click.echo('firebase-import: import data to Firestore')
    click.echo('file path: %s' % file)
    click.echo('Collection name: %s' % collection)
    click.echo('prefix: %s' % prefix)
    click.echo('Document ID: %s' % auto)
    click.echo('default delimiter for the file: %s' % delimiter)
    click.echo()
    click.echo('Continue? [Yy/Nn]', nl=False)
    c = click.getchar()

    click.echo()

    if c == 'y' or c == 'Y':
        click.echo('checking...')
    elif c == 'n' or c == 'N':
        click.echo('Abort!')
        sys.exit()
    else:
        click.echo('Invalid input :( press [Yy/Nn]')
        sys.exit()

    try:
        total_lines = (total_file_lines(file) -1)
        click.echo('Loading %s records...' % total_lines)

        with click.progressbar(length=total_lines, label='Loading data...') as bar:
            j = 0
            with open(file, newline='') as csvfile:
                file_to_read = csv.reader(csvfile, delimiter=delimiter)
                headers = next(file_to_read, None)  # returns the headers or `None` if the input is empty
                _headers = [item.strip() for item in headers]
                coll_name = None

                if prefix is None:
                    coll_name = collection
                else:
                    coll_name = "{0}{1}".format(prefix, collection)

                batch = db.batch()
                doc_ref = db.collection(coll_name).document()
                i = 0

                for row in file_to_read:
                    i = i + 1
                    j = j + 1
                    data_doc = dict(zip(headers, row))
                    batch.set(db.collection(coll_name).document(), data_doc)

                    if i >= 450:
                        batch.commit()
                        time.sleep(1)
                        i = 0
                    bar.update(j)

                batch.commit()


    except Exception as e:
        click.echo()
        print("an error occurred while loading the data:", e)
        sys.exit()

    click.echo()
    print("the process has been successfully completed!.")
    click.pause()


if __name__ == '__main__':
    command_line()
