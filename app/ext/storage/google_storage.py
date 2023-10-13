# -*- coding: utf-8 -*-

"""Python module for Google Cloud Storage."""

import os
from google.cloud import storage, exceptions
from werkzeug.utils import secure_filename
from app.config.storage import DEFAULT_BUCKET
from app.ext.utils import DateUtils
from app.uploads.models.Upload import Upload
from io import BytesIO
import logging as log

DEFAULT_FOLDER = 'general'

try:
    # Instantiates a client
    storage_client = storage.Client()
except Exception as e:
    print("Google Storage Client Exception:", e)
    raise e


class StorageFile():

    @staticmethod
    def save_logs(data=None):

        if data is None:
            return None

        try:
            _new_data = Upload()
            _new_data.original_name = data['original_name']
            _new_data.generated_name = data['generated_name']
            _new_data.applications_id = data['applications_id']
            _new_data.user_id = data['user_id']
            _new_data.bucket_path = data['bucket_path']
            _new_data.is_public = data['is_public']
            _new_data.meta_data = data['meta_data']
            _new_data.origin = data['origin']

            Upload.save(_new_data)

            return {"id":_new_data.id}

        except Exception as e:
            log.warning("An error occurred while saving the info file to Firestore.")
            log.warning("StorageFile save_logs Exception:", e)

        return None

    @staticmethod
    def validate_meta_data(meta_data):
        if meta_data is None:
            return None

        try:
            list_meta_data = meta_data.split(',')
            obj_meta_data = {}

            if len(list_meta_data) > 0:

                for key, item in enumerate(list_meta_data):
                    if item == 'allow_public':
                        obj_meta_data.update({'allow_public': True})
                    else:
                        value = item.split('=')
                        if 'expire_time' in value:
                            obj_meta_data.update({'expire_time': value[1]})
                        elif 'language' in value:
                            obj_meta_data.update({'language': value[1]})

                if len(obj_meta_data) > 0:
                    return obj_meta_data
                else:
                    return None
            else:
                return None

        except Exception as e:
            print("StorageFile validate_meta_data Exception:", e)

        return None

    def get_default_bucket():
        try:
            default_bucket = storage_client.get_bucket(DEFAULT_BUCKET)
            return default_bucket
        except exceptions.NotFound as e:
            print("StorageFile get_default_bucket Exception:", e)
        return None

    @staticmethod
    def save_file(file_name=None, blob_content=None, file_content_type=None, meta_data=None, folder_path=None, make_public=False, from_origin=None, save_log=True, options=None):

        if file_name is None:
            return None

        if blob_content is None:
            return None

        if file_content_type is None:
            return None

        new_filename = None
        store_file_path = None

        try:
            filename, ext = os.path.splitext(file_name)
            #new_filename = "{0}_{1}{2}".format(filename, DateUtils.get_timestamp(), ext)
            new_filename = file_name
        except Exception as e:
            new_filename = "{0}_{1}".format(DateUtils.get_timestamp(), file_name)

        if folder_path is None:
            store_file_path = "{0}/{1}".format(DEFAULT_FOLDER, secure_filename(new_filename))
        else:
            store_file_path = "{0}/{1}".format(folder_path, secure_filename(new_filename))

        try:
            bucket = StorageFile.get_default_bucket()

            if bucket:
                blob = bucket.blob(store_file_path)
                blob.upload_from_string(blob_content, content_type=file_content_type)

                update_meta_data = None
                allow_public = False

                if meta_data is not None:
                    # blob.metadata = meta_data
                    update_meta_data = StorageFile.validate_meta_data(meta_data)
                    if update_meta_data is not None:
                        allow_public = True if 'allow_public' in update_meta_data else False
                        blob.metadata = update_meta_data
                        # update metadata
                        blob.patch()

                allow_make_public = False

                if make_public is True or allow_public is True:
                    allow_make_public = True
                    blob.make_public()

                result_log = ""
                if save_log is True:

                    applications_id = ""
                    user_id = ""
                    if options is not None:
                        applications_id = options['applications_id'] if 'applications_id' in options else None
                        user_id = options['user_id'] if 'user_id' in options else None

                    result_log = StorageFile.save_logs({
                        'original_name': file_name,
                        'generated_name': store_file_path,
                        'applications_id': applications_id,
                        'user_id': user_id,
                        'bucket_path': blob.public_url if allow_make_public is True else store_file_path,
                        'is_public': allow_make_public,
                        'meta_data': update_meta_data,
                        'origin': from_origin
                    })

                return {
                    'storage_id': blob.id,
                    'url': blob.public_url if allow_make_public is True else store_file_path,
                    'is_public': allow_make_public,
                    'meta_data': update_meta_data,
                    "id_upload": result_log['id']
                }
            else:
                return {
                    'error': "Unexpected Error: Bucket '{0}', Not Found".format(DEFAULT_BUCKET)
                }
        except Exception as e:
            log.warning("An error occurred while saving the file to gcs.")
            log.warning("StorageFile save_file Exception: {0}".format(str(e)))

            return {
                'error': str(e)
            }

    @staticmethod
    def get_file(filename):

        if filename is None:
            return None

        try:
            bucket = StorageFile.get_default_bucket()

            blob = bucket.blob(filename)

            string_buffer = BytesIO()
            blob.download_to_file(string_buffer)
            content = string_buffer.getvalue()

            return content

        except Exception as e:
            print("StorageFile get_file Exception: {0}".format(str(e)))
            return None
