#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from app.app.Environment import Environment, EnvironmentType

CURRENT_ENV = os.getenv('ENVIRONMENT', "DEVELOP")

# ENVIRONMENT = "DEVELOP"
ENVIRONMENT = CURRENT_ENV
# ENVIRONMENT = "PRODUCTION"

NO_DATABASE_CONNECTION = "NO_DATABASE_CONNECTION"

# APP
APP_ROUTE_PREFIX = "/api"

# Internationalization
TIME_ZONE = 'UTC -5'
STDR_UTC_HOUR = 5
LOCAL_UTC_HOUR = -5

CURRENT_ENVIRONMENT = Environment(EnvironmentType.get_by_name(ENVIRONMENT))

