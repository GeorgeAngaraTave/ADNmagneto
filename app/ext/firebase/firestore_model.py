# -*- coding: utf-8 -*-

"""Python module for Google Cloud Firestore."""

import firebase_admin
from firebase_admin import credentials
from google.cloud import firestore
from google.cloud.firestore_v1 import Increment

from app.config.local_settings import DATABASE_PREFIX
from app.ext.utils import Commons, DateUtils

cred = credentials.ApplicationDefault()
firebase_admin.initialize_app(cred)

try:
    db = firestore.Client()
except Exception as e:
    print("Firestore Client Exception:", e)
    raise e


class Query:
    """ A class representing a query on a collection """

    def __init__(self, query_params, to_json=True):
        self.cls = self
        self.result = None
        self.q = None

    @staticmethod
    def and_(self, query_params, to_json=True, limit=None, select_fields=None, order_by=None):
        if query_params is None:
            return None

        self.result = None

        collection = self.__tablename__

        if DATABASE_PREFIX:
            collection = "{0}{1}".format(DATABASE_PREFIX, collection)

        self.q = db.collection(collection)

        if Commons.is_iterable(query_params):
            try:
                # parse the params
                for param in query_params:
                    if len(param) == 2:
                        self.q = self.q.where(param[0], '==', param[1])
                    if len(param) == 3:
                        self.q = self.q.where(*param)

                if Commons.is_iterable(select_fields):
                    if len(select_fields) > 0:
                        if limit is not None and int(limit) > 0:
                            self.q = self.q.select(select_fields).limit(limit)
                        else:
                            self.q = self.q.select(select_fields)
                    else:
                        print("FirestoreModel and_ Exception: At least one field is required, from the list of fields.")
                        return None
                elif limit is not None and int(limit) > 0:
                    self.q = self.q.limit(limit)

                if order_by is not None:
                    self.q = self.q.order_by(order_by)

            except Exception as e:
                print("FirestoreModel and_ Exception:", e)
                return None
        else:
            print("FirestoreModel and_ Exception: query_params is not iterable.")
            return None

        result = self.q.stream()

        try:
            if result is None:
                return None
            else:
                if to_json is True:
                    resp = self.to_json(result, True)
                    return resp
                else:
                    return result
        except Exception as e:
            print("FirestoreModel and_ Exception:", e)
            return None

    @staticmethod
    def or_(self, query_params=None, to_json=True):
        self.result = None
        self.q = db.collection(self.__tablename__)

        try:
            collection = self.__tablename__

            if DATABASE_PREFIX:
                collection = "{0}{1}".format(DATABASE_PREFIX, collection)

            doc_ref = db.collection(collection)

            for param in query_params:
                if len(param) == 2:
                    doc_ref.where(param[0], '==', param[1])
                if len(param) == 3:
                    doc_ref.where(*param)

            result = doc_ref.get()

            if to_json is True:
                resp = self.to_json(result, True)
                return resp
            else:
                return result

        except Exception as e:
            print('FirestoreModel or_ Exception', e)
            return e

    def get(self):
        """ Executes the query
            @return Generator object that yields hydrated instances of the class supplied __init__
        """
        self.result = self.q.get()
        try:
            for r in self.result:
                yield r
        except Exception as e:
            print('FirestoreModel get Exception', e)
            raise e


class FirestoreModel:
    BATCH_LIMIT = int(400)
    MAX_BATCH_LOAD = int(500000)

    @classmethod
    def get_all_properties(self):
        all_properties = self.__dict__.keys()

        forbidden_keys = ['__module__', '__tablename__', '__doc__']
        list_properties = []

        try:
            for item in all_properties:
                if item not in forbidden_keys:
                    list_properties.append(item)

            return list_properties
        except Exception as e:
            print('FirestoreModel get_all_properties Exception', e)
            return None

    @classmethod
    def get_prefix(cls, collection_name):
        if collection_name is None:
            return None

        prefix = collection_name

        if DATABASE_PREFIX:
            prefix = "{0}{1}".format(DATABASE_PREFIX, collection_name)

        return prefix

    @classmethod
    def dict_to_obj(cls, _dict=None, _name='from_dict'):
        if _dict is None:
            return None

        try:
            new_obj = type(_name, (object,), _dict)
            return new_obj
        except Exception as e:
            print('FirestoreModel dict_to_obj Exception', e)
            return None

    @staticmethod
    def to_json(docs, key=False):
        try:
            obj = {}
            array_result = []

            for item in docs:
                obj = item.to_dict()

                if 'coords' in obj:
                    obj['coords'] = FirestoreModel.from_geo_point(obj['coords'])

                if key is True:
                    obj['key'] = item.id

                array_result.append(obj)
            return array_result
        except Exception as e:
            print('FirestoreModel to_json Exception', e)
            return None

    @classmethod
    def save(self, data=None):
        if data is None:
            return None

        try:
            collection = self.get_prefix(self.__tablename__)
            data.created_at = DateUtils.get_timestamp()

            doc_ref = db.collection(collection)
            time_stamp, obj_ref = doc_ref.add(data.__dict__)

            return obj_ref
        except Exception as e:
            print('Firestore save Exception', e)
            return e

    @classmethod
    def save_and_set(self, key, data=None):
        if key is None:
            return None

        if data is None:
            return None

        try:
            collection = self.get_prefix(self.__tablename__)

            data['created_at'] = DateUtils.get_timestamp()
            doc_ref = db.collection(collection).document(str(key)).set(data)

            return None
        except Exception as e:
            print('Firestore save_and_set Exception', e)
            return e

    @classmethod
    def save_notifications(self, key, data=None):
        if key is None:
            return None

        if data is None:
            return None

        try:
            collection = self.__tablename__
            data['created_at'] = DateUtils.get_timestamp()
            doc_ref = db.collection(collection).document(str(key)).set(data)
            return doc_ref
        except Exception as e:
            print('Firestore save_and_set Exception', e)
            return e

    @classmethod
    def multi_save(self, data=None, is_dict=False):
        if data is None:
            return None

        try:
            collection = self.get_prefix(self.__tablename__)

            if Commons.is_iterable(data):
                total_record = len(data)

                if total_record > 0:

                    if total_record <= self.MAX_BATCH_LOAD:
                        try:
                            cicle = int(( total_record / self.BATCH_LIMIT) + 1)
                            k = 0

                            for r in range(0, cicle):
                                batch = db.batch()

                                for a in range((r * self.BATCH_LIMIT), (r * self.BATCH_LIMIT) + self.BATCH_LIMIT):
                                    if a >= total_record:
                                        break

                                    if is_dict is True:
                                        data[a]['created_at'] = DateUtils.get_timestamp()
                                    else:
                                        data[a].created_at = DateUtils.get_timestamp()

                                    doc_ref = db.collection(collection).document()

                                    if is_dict is True:
                                        batch.set(doc_ref, data[a])
                                    else:
                                        batch.set(doc_ref, data[a].__dict__)

                                    k = k + 1

                                batch.commit()

                            print("FirestoreModel multi_save, records saved:", k)
                            return None
                        except Exception as e:
                            print('Firestore multi_save Exception: an error has occurred while loading data', e)
                            return e
                    else:
                        reason = "FirestoreModel multi_save Exception: the maximum number of records to save has been exceeded"
                        print(reason)
                        return reason
                else:
                    reason = "FirestoreModel multi_save Exception: At least one record is required, from the list of records"
                    print(reason)
                    return reason
            else:
                reason = "FirestoreModel multi_save Exception: data is not Iterarable"
                print(reason)
                return reason
        except Exception as e:
            print('Firestore multi_save Exception:', e)
            return e

    @classmethod
    def get_subcollection_by_id(self, key, sub_col='versions', sub_col_id=1, as_object=False):

        try:
            collection = self.get_prefix(self.__tablename__)

            users_ref = db.collection(collection).document(str(key)).collection(sub_col).document(str(sub_col_id))
            docs = users_ref.get()
            result = docs.to_dict()

            if result is None:
                return None
            else:
                if as_object is True:
                    return self.dict_to_obj(result)
                if 'coords' in result:
                    result['coords'] = FirestoreModel.from_geo_point(result['coords'])

                return result
        except Exception as e:
            print('Firestore get_subcollection_by_id Exception', e)
            return e

    @classmethod
    def subcollection(self, id, data=None, sub_col='versions', sub_col_id=1, sub_col_data=None):
        if data is None:
            return None

        try:
            collection = self.get_prefix(self.__tablename__)

            data.created_at = DateUtils.get_timestamp()

            doc_ref = db.collection(collection)
            doc_sub_ref = doc_ref.document(id).collection(sub_col)
            doc_sub_ref.document(sub_col_id).set(sub_col_data)
            doc_ref.document(id).set(data.__dict__)

            return None
        except Exception as e:
            print('Firestore subcollection save Exception', e)
            return e

    @classmethod
    def update_subcol(self, id, sub_col='versions', sub_col_id=1, sub_col_data=None):
        if sub_col_data is None:
            return None

        try:
            collection = self.get_prefix(self.__tablename__)

            sub_col_data['updated_at'] = DateUtils.get_timestamp()

            doc_ref = db.collection(collection).document(id).collection(sub_col).document(sub_col_id).set(sub_col_data)

            return None
        except Exception as e:
            print('Firestore update_subcol update Exception', e)
            return e

    @classmethod
    def batch_counter(self, data=None, update_mode='increment', stats_ref='--stats--'):
        if data is None:
            return None

        batch_update_mode = Increment(1)

        if update_mode == 'increment':
            batch_update_mode = Increment(1)
        elif update_mode == 'decrement':
            batch_update_mode = Increment(-1)

        try:
            collection = self.get_prefix(self.__tablename__)

            data.created_at = DateUtils.get_timestamp()

            doc_ref = db.collection(collection).document()
            statsRef  = db.collection(collection).document(stats_ref)

            batch = db.batch()

            ref_exists = statsRef.get().exists

            if (ref_exists == True):
                batch.update(statsRef, { 'storyCount': batch_update_mode })
            else:
                batch.set(statsRef, { 'storyCount': batch_update_mode })

            batch.set(doc_ref, data.__dict__)
            batch.commit()

            return None
        except Exception as e:
            print('Firestore batch_counter Exception', e)
            return e

    @classmethod
    def get_all(self, limit=None, select_fields=None):
        try:
            the_coll = self.get_prefix(self.__tablename__)
            users_ref = db.collection(the_coll)
            docs = None

            if Commons.is_iterable(select_fields):
                if len(select_fields) > 0:
                    if limit is not None and int(limit) > 0:
                        docs = users_ref.select(select_fields).limit(limit).get()
                    else:
                        docs = users_ref.select(select_fields).get()
                else:
                    print("FirestoreModel get_all Exception: At least one field is required, from the list of fields.")
                    return None
            elif limit is not None and int(limit) > 0:
                docs = users_ref.limit(limit).get()
            else:
                docs = users_ref.get()

            result = self.to_json(docs, True)

            return result
        except Exception as e:
            print("FirestoreModel get_all Exception:", e)
            return e

    @classmethod
    def get_all_subcollections(self, id, sub_col=None, limit=None, select_fields=None):
        try:
            the_coll = self.get_prefix(self.__tablename__)
            coll_ref = db.collection(the_coll)
            doc_sub_ref = coll_ref.document(id).collection(sub_col)
            docs = None

            if Commons.is_iterable(select_fields):
                if len(select_fields) > 0:
                    if limit is not None and int(limit) > 0:
                        docs = doc_sub_ref.select(select_fields).limit(limit).get()
                    else:
                        docs = doc_sub_ref.select(select_fields).get()
                else:
                    print("FirestoreModel get_all_subcollections Exception: At least one field is required, from the list of fields.")
                    return None
            elif limit is not None and int(limit) > 0:
                docs = doc_sub_ref.limit(limit).get()
            else:
                docs = doc_sub_ref.get()

            result = self.to_json(docs, True)

            return result
        except Exception as e:
            print("FirestoreModel get_all_subcollections Exception:", e)
            return e

    @classmethod
    def get_all_collections(self):
        try:
            all_collections = db.collections()
            list_collection = []

            for collection in all_collections:
                list_collection.append(collection.id)

            if len(list_collection) > 0:
                return list_collection
            else:
                return []
        except Exception as e:
            print("FirestoreModel get_list_collection Exception:", e)
            return []

    @classmethod
    def get_by(self, key, value, limit=None, select_fields=None, value_format=True):
        if key is None:
            return None

        if value is None:
            return None

        if value_format:
            value = str(value)

        try:
            collection = self.get_prefix(self.__tablename__)
            doc_ref = db.collection(collection)
            docs = None

            if Commons.is_iterable(select_fields):
                if len(select_fields) > 0:
                    if limit is not None and int(limit) > 0:
                        docs = doc_ref.where(key, '==', value).select(select_fields).limit(limit).get()
                    else:
                        docs = doc_ref.where(key, '==', value).select(select_fields).get()
                else:
                    print("FirestoreModel get_by Exception: At least one field is required, from the list of fields.")
                    return None
            elif limit is not None and int(limit) > 0:
                docs = doc_ref.where(key, '==', value).limit(limit).get()
            else:
                docs = doc_ref.where(key, '==', value).get()

            result = self.to_json(docs, True)

            if Commons.is_iterable(result):
                if len(result) == 0:
                    return None
                else:
                    return result
            else:
                print("FirestoreModel get_by Exception: Result is not Iterarable")
                return None
        except Exception as e:
            print("FirestoreModel get_by Exception:", e)
            return e

    @classmethod
    def get_by_id(self, key, as_object=False, select_fields=None):
        if key is None:
            return None

        try:
            collection = self.get_prefix(self.__tablename__)
            users_ref = db.collection(collection).document(str(key))
            docs = None

            if Commons.is_iterable(select_fields):
                if len(select_fields) > 0:
                    docs = users_ref.select(select_fields).get()
                else:
                    print("FirestoreModel get_by_id Exception: At least one field is required, from the list of fields.")
                    return None
            else:
                docs = users_ref.get()

            result = docs.to_dict()

            if result is None:
                return None
            else:
                if as_object is True:
                    return self.dict_to_obj(result)
                if 'coords' in result:
                    result['coords'] = FirestoreModel.from_geo_point(result['coords'])

                return result
        except Exception as e:
            print('Firestore get_by_id Exception', e)
            return e

    @classmethod
    def get_ref(self):
        try:
            collection = self.get_prefix(self.__tablename__)
            doc_ref = db.collection(collection)
            return doc_ref
        except Exception as e:
            print('FirestoreModel query Exception', e)
            return e

    @classmethod
    def get_radius(self, coord=None, radio=10):
        pass

    @classmethod
    def geo_point(self, lat=None, lon=None):
        if lat is None:
            return None

        if lon is None:
            return None

        try:
            return firestore.GeoPoint(float(lat), float(lon))
        except Exception as e:
            print('FirestoreModel geo_point Exception', e)
            return e

    @classmethod
    def from_geo_point(self, coords=None):
        if coords is None:
            return None

        try:
            if isinstance(coords, (self)):
                return {
                    'latitude': coords.latitude,
                    'longitude': coords.longitude
                }
            elif isinstance(coords, (dict)):
                return {
                    'latitude': coords['latitude'],
                    'longitude': coords['longitude']
                }
            elif isinstance(coords, (firestore.GeoPoint)):
                return {
                    'latitude': coords.latitude,
                    'longitude': coords.longitude
                }
            else:
                # fall back
                return coords
        except Exception as e:
            print('FirestoreModel from_geo_point Exception', e)
            return coords

    @classmethod
    def raw_query(self, params=None, to_json=True, limit=None, select_fields=None):
        try:
            collection = self.get_prefix(self.__tablename__)
            doc_ref = db.collection(collection)

            for param in params:
                doc_ref.where(*param)

            result = None

            if Commons.is_iterable(select_fields):
                if len(select_fields) > 0:
                    if limit is not None and int(limit) > 0:
                        result = doc_ref.select(select_fields).limit(limit).get()
                    else:
                        result = doc_ref.select(select_fields).get()
                else:
                    print("FirestoreModel raw_query Exception: At least one field is required, from the list of fields.")
                    return None
            elif limit is not None and int(limit) > 0:
                result = doc_ref.limit(limit).get()
            else:
                result = doc_ref.get()

            if to_json is True:
                resp = self.to_json(result, True)
                return resp
            else:
                return result

        except Exception as e:
            print('FirestoreModel raw_query Exception', e)
            return e

    @classmethod
    def or_(cls, q=(), to_json=True):
        """ Get a handle to a query object (see Query or_ helper class above)
        @param cls The class of the instance calling make
        @param q A list of query key/value or key/operator/value pairs (
        """
        return Query.or_(cls, q, to_json)

    @classmethod
    def and_(cls, q=(), to_json=True, limit=None, select_fields=None, order_by=None):
        """ Get a handle to a query object (see Query and_ helper class above)
        @param cls The class of the instance calling make
        @param q A list of query key/value or key/operator/value pairs (
        """
        return Query.and_(cls, q, to_json, limit, select_fields, order_by)

    @classmethod
    def get(cls, doc_id, raise_exception=False):
        """ Get a single model instance
        @param cls The class of the instance calling make
        @param doc_id The id of the document to get
        @return A model instance of type class hydrated w/ data from the database
        """
        try:
            table_name = cls.get_prefix(cls.__tablename__)
            doc_ref = db.collection(table_name).document(doc_id).get()
            return cls(**doc_ref.to_dict())
        except Exception as e:
            print('FirestoreModel get Exception', e)
            if raise_exception:
                raise e
        return None

    @classmethod
    def update(self, key=None, data=None):
        if key is None:
            return None

        if data is None:
            return None

        try:
            collection = self.get_prefix(self.__tablename__)
            city_ref = db.collection(collection).document(key)
            data['updated_at'] = DateUtils.get_timestamp()
            city_ref.update(data)

            return None
        except Exception as e:
            print('Firestore update Exception', e)
            return e

    @classmethod
    def delete(self, key=None):
        try:
            collection = self.get_prefix(self.__tablename__)
            db.collection(collection).document(key).delete()

            return None
        except Exception as e:
            print('Firestore delete Exception', e)
            return e

    @classmethod
    def deleteFields(self, key=None, select_fields=None):
        if key is None:
            return None

        if select_fields is None:
            return None

        try:
            if Commons.is_iterable(select_fields):
                if len(select_fields) > 0:
                    try:
                        collection = self.get_prefix(self.__tablename__)
                        doc_ref = db.collection(collection).document(key)

                        field_obj = {}

                        for item in select_fields:

                            field_obj.update({
                                item[:]: firestore.DELETE_FIELD
                            })


                        if len(field_obj) > 0:
                            result = doc_ref.update(field_obj)
                            print("FirestoreModel deleteFields removed:", result)
                            return None
                        else:
                            print("FirestoreModel deleteFields Exception: field_obj is empty")
                            return None

                    except Exception as e:
                        print('Firestore deleteFields item Exception', e)
                        return e
                else:
                    print("FirestoreModel deleteFields Exception: At least one field is required, from the list of fields.")
                    return None
            else:
                print("FirestoreModel deleteFields Exception: select_fields is not iterable.")
                return None

            return None
        except Exception as e:
            print('Firestore deleteFields Exception', e)
            return e

    @classmethod
    def delete_collection(self):
        try:
            collection = self.get_prefix(self.__tablename__)

            coll_ref = db.collection(collection)
            docs = coll_ref.limit(self.BATCH_LIMIT).stream()

            batch = db.batch()
            deleted = 0

            for doc in docs:
                doc_ref = db.collection(collection).document(doc.id)
                batch.delete(doc_ref)
                deleted = deleted + 1

            batch.commit()
            print('Firestore delete_collection, current deleted records:', deleted)

            if deleted >= self.BATCH_LIMIT:
                return self.delete_collection()

            return None
        except Exception as e:
            print('Firestore delete_collection Exception:', e)
            return e
