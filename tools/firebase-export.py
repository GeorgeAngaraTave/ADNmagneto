#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import json
import time
from datetime import datetime, timedelta, date, time
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

class customEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        elif isinstance(obj, date):
            return obj.isoformat()
        elif isinstance(obj, time):
            return obj.isoformat()
        elif isinstance(obj, timedelta):
            return (datetime.min + obj).time().isoformat()
        else:
            return super(customEncoder, self).default(obj)

        return json.JSONEncoder.default(self, obj)

class OptionEatAll(click.Option):

    def __init__(self, *args, **kwargs):
        self.save_other_options = kwargs.pop('save_other_options', True)
        nargs = kwargs.pop('nargs', -1)
        assert nargs == -1, 'nargs, if set, must be -1 not {}'.format(nargs)
        super(OptionEatAll, self).__init__(*args, **kwargs)
        self._previous_parser_process = None
        self._eat_all_parser = None

    def add_to_parser(self, parser, ctx):

        def parser_process(value, state):
            # method to hook to the parser.process
            done = False
            value = [value]
            if self.save_other_options:
                # grab everything up to the next option
                while state.rargs and not done:
                    for prefix in self._eat_all_parser.prefixes:
                        if state.rargs[0].startswith(prefix):
                            done = True
                    if not done:
                        value.append(state.rargs.pop(0))
            else:
                # grab everything remaining
                value += state.rargs
                state.rargs[:] = []
            value = tuple(value)

            # call the actual process
            self._previous_parser_process(value, state)

        retval = super(OptionEatAll, self).add_to_parser(parser, ctx)
        for name in self.opts:
            our_parser = parser._long_opt.get(name) or parser._short_opt.get(name)
            if our_parser:
                self._eat_all_parser = our_parser
                self._previous_parser_process = our_parser.process
                our_parser.process = parser_process
                break
        return retval

def print_version(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    click.echo('firebase-export Version 1.0')
    ctx.exit()

def key_press():
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

def saving_collections(file, n_documents, dict4json):
    if n_documents > 0:
        ready = False
        try:
            jsonfromdict = json.dumps(dict4json, indent=4, sort_keys=True, default=str)
            # jsonfromdict = json.dumps(dict4json, indent=4, sort_keys=True, cls=customEncoder)
            ready = True
        except Exception as e:
            ready = False
            print("jsonfromdict Exception", e)

        if ready is True:
            path_filename = click.format_filename(file)

            click.echo()
            print("now writing {0} json records to {1}...".format( len(jsonfromdict), path_filename ))
            print("please wait...")

            with open(path_filename, 'w') as the_file:
                the_file.write(jsonfromdict)

            click.echo()
            print("the process has been successfully completed!.")
            click.pause()
        else:
            click.echo()
            print("the process has been aborted!.", "ready:", ready)
            click.pause()
    else:
        click.echo()
        print("the process has been aborted: {0} documents to save.".format(n_documents))
        click.pause()

@click.command(context_settings=dict(
    ignore_unknown_options=True,
    help_option_names=['-h', '--help']
))

@click.option('-f', '--file', default='./export.json', required=True, type=click.Path(), help='file to export.')
@click.option('-c', '--collection-list', required=True, cls=OptionEatAll, help='Collections list to export')
@click.option('-e', '--exclude-list', cls=OptionEatAll, help='Collection list to exclude (default: None)')
@click.option('-v', '--version', is_flag=True, callback=print_version, expose_value=False, is_eager=True, help='show current version and exit.')

def command_line(file, collection_list, exclude_list):
    collections = dict()
    dict4json = dict()
    n_documents = 0
    export_method = None

    list_collections = list(collection_list)
    list_exclude = list(exclude_list) if exclude_list is not None else []
    print("file name:", file)
    print("collections list:", list_collections)
    print("exclude collections list:", list_exclude)

    if len (list_collections) <= 0:
        click.echo()
        print("at least one Collection is required.")
        click.pause()
        sys.exit()

    if len (list_collections) == 1:
        print("list_collections es uno")
        if list_collections[0] == 'all':
            click.echo()
            print("export all collections")
            export_method = 'all'
        else:
            export_method = 'custom'
    elif len (list_collections) > 1:
        print("list_collections > 0")
        export_method = 'custom'

    print('export_method', export_method)

    if export_method == 'custom':
        click.echo()
        print('se iniciara el export de las siguientes colecciones:')
        for collection in list_collections:
            print(">", collection)

        key_press()

        click.echo()
        print('Se iniciara el export de las colecciones...')
        print(">", list_collections)
        print('obteniendo listado de colecciones...')

        for collection in list_collections:
            print("downloading collection {0}...".format(collection))
            collections[collection] = db.collection(collection).stream()
            dict4json[collection] = {}
            for document in collections[collection]:
                docdict = document.to_dict()
                dict4json[collection][document.id] = docdict
                n_documents += 1

        click.echo()
        print("Downloaded {0} collections, {1} documents...".format( len(collections), n_documents))
        saving_collections(file, n_documents, dict4json)

    elif export_method == 'all':
        print('obteniendo listado de colecciones...')
        firestore_list = db.collections() # magic !!!!

        export_list = []
        final_export_list = []

        for collection in firestore_list:
            export_list.append(collection.id)

        if len(list_exclude) > 0:
            print('removiendo excepciones..')
            for key, collection in enumerate(export_list):
                if collection in list_exclude:
                    continue
                final_export_list.append(collection)
        else:
            final_export_list = export_list

        click.echo()
        print('Se iniciara el export de las colecciones...')
        print(">", final_export_list)

        if len(final_export_list) >0:
            key_press()

            for collection in final_export_list:
                print("downloading collection {0}...".format(collection))
                collections[collection] = db.collection(collection).stream()
                dict4json[collection] = {}
                for document in collections[collection]:
                    docdict = document.to_dict()
                    dict4json[collection][document.id] = docdict
                    n_documents += 1

            click.echo()
            print("Downloaded {0} collections, {1} documents...".format( len(collections), n_documents))
            saving_collections(file, n_documents, dict4json)
    else:
        click.echo()
        print("the process has been aborted (Fail to export method)!.")
        click.pause()

if __name__ == '__main__':
    command_line()
