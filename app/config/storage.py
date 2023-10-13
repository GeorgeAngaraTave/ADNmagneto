# -*- coding: utf-8 -*-

# Storage Settings
# For more information, see app.ext.storage module

# information for files
# Maximum file size: 30Mb default
MAX_FILE_SIZE = 29 * 1024 * 1024

# file extensions allowed
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif', 'bmp', 'txt', 'csv', 'xls', 'xlsx', 'doc', 'docx', 'pdf', 'zip', 'shp'])
ALLOWED_IMG_EXTS = set(['png', 'jpg', 'jpeg', 'gif', 'bmp'])
ALLOWED_CATEGORY_FILE = set(['VISIT_POINT'])
ALLOWED_STATUS = [["CARGADO","LOADED"],["EN PROCESO","IN PROCESS"],["FINALIZADO","FINALIZED"],["ERROR","ERROR"]]

# folder name for gae
DEFAULT_BUCKET = "invertible-eye-316323.uc.r.appspot.com"
PUBLIC_URI = 'https://storage.googleapis.com'
