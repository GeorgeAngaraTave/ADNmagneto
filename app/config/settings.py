# -*- coding: utf-8 -*-

"""
settings for Serviroutes project.

Using Flask 1.0.4.

For more information on this file, see
README.md
"""

# Application definition
APP_VERSION = '3.c'

INSTALLED_MODULES = [
    'home',
    'adn'
]

# Secret key for signing cookies
SECRET_KEY = '\xdf<\x90\xfd\xf9\xf1\x0f\xf1\x84ww\x18\x180\x12\xb81T\xac\x05\xd3\xc9\xb4\xda}y3R\x8a\x8c\xba\x16'

# Use a secure, unique and absolutely secret key for
# signing the data.
CSRF_SESSION_KEY = "PBqtIxGj5xhpTU9K3RSr4J2krKqtQV"

# Enable protection agains *Cross-site Request Forgery (CSRF)*
CSRF_ENABLED = True
