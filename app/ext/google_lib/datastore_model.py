# -*- coding: utf-8 -*-

"""Python module for Google Datastore."""

try:
    from google.appengine.ext import ndb
except ImportError:
    print("Warning: datastore_model module only is allowed on GAE Server")


class NDBModel(ndb.Model):

    def json(obj, key=False):
        data = dict([(p, unicode(getattr(obj, p))) for p in obj._properties])
        if key:
            dict_key = {'Key': unicode(obj.key.id())}
            data.update(dict_key)
        return data

    @classmethod
    def get_all(cls):
        resp = cls.query()
        if resp is None:
            return None
        else:
            return resp

    def get_key(cls):
        try:
            return cls.key
        except Exception as e:
            print(e)
            return None

    @classmethod
    def get_by(cls, _name, _value, result_fetch='one'):

        if _name is None:
            return None

        if _value is None:
            return None

        try:
            _query = "where {0} = '{1}'".format(_name, str(_value))

            if result_fetch is 'one':
                return cls.gql(_query).get()
            elif result_fetch is 'all':
                return cls.gql(_query).fetch()

        except Exception as e:
            print("get_by Exception: {0}".format(str(e)))
            return None

    @classmethod
    def get_by_key(cls, key_value):
        if key_value is None:
            return None

        try:
            obj = cls.get_by_id(int(key_value))
            return obj
        except Exception as e:
            print(e)
            return None

    @classmethod
    def get_by_name(cls, value):
        if value is None:
            return None
        else:
            return cls.gql("where name = :1", value).get()

    @classmethod
    def delete(cls, id=None):
        if id is not None:
            obj = cls.get_by_id(int(id))
            if obj is not None:
                obj.key.delete()
            else:
                return None
        else:
            obj = cls
            if obj is not None:
                obj.key.delete()
                return None
            else:
                return None

    def to_geo_point(cls, lat=None, lng=None):
        if lat is None:
            return None

        if lng is None:
            return None

        try:
            return ndb.GeoPt(lat, lng)
        except Exception as e:
            print(e)
            return None
