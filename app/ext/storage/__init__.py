try:
    from .google_storage import StorageFile
except ImportError as e:
    import logging as log
    log.warning("Warning: google_storage ImportError", str(e))
    log.warning('Warning: now using custom_storage')
    from .custom_storage import StorageFile
