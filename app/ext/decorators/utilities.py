#!/usr/bin/env python
# -*- coding: utf-8 -*-
import uuid


def new_uuid4() -> uuid.UUID:
    return uuid.uuid4()


def is_valid_uuid(val):
    try:
        uuid.UUID(str(val))
        return True
    except ValueError:
        return False
