# -*- coding: utf-8 -*-

"""Python module for custom storage."""

import os
from app.config.storage import DEFAULT_BUCKET
from app.ext.utils import DateUtils
import logging as log


class StorageFile:
    @staticmethod
    def save_file(file_name=None, content_file_name=None, file_content_type=None, options=None):
        log.info("using custom_storage")

        if file_name is None:
            return None

        if content_file_name is None:
            return None

        ext = file_name.rsplit('.', 1)[1].lower()
        new_filename = "{0}_{1}.{2}".format(file_name, DateUtils.get_timestamp(), ext)
        store_file_path = os.path.join(DEFAULT_BUCKET, new_filename)

        try:
            if not os.path.exists(DEFAULT_BUCKET):
                print("StorageFile save_file: creating bucket...")
                os.makedirs(DEFAULT_BUCKET)
        except Exception as e:
            log.warning("StorageFile save_file Exception:", e)
            return None

        try:
            newFileByteArray = bytearray(content_file_name)

            with open(store_file_path, 'wb') as file:
                file.write(newFileByteArray)

            print("The file has been saved successfully")

            return {
                'url': store_file_path
            }
        except Exception as e:
            log.warning("An error occurred while saving the file")
            log.warning("StorageFile save_file Exception:", e)

            return {
                'error': str(e)
            }

    @classmethod
    def create_file(self, filename):
        pass
