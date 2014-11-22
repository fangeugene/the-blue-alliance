import datetime
import iso8601
import json
import logging

from google.appengine.ext import ndb

from consts.model_type import ModelType


class ModelJSONConverter(object):
    """
    Serializes and deserializes models
    """

    @classmethod
    def to_json(cls, model):
        """
        Converts an ndb model into a JSON dict
        """
        dic = cls._to_json_helper(model.to_dict())
        dic['key'] = cls._to_json_helper(model.key)
        dic['model_type'] = ModelType.to_type[type(model)]
        return json.dumps(dic)

    @classmethod
    def _to_json_helper(cls, obj):
        """
        Helper function that is recursively called
        """
        if isinstance(obj, ndb.Key):
            return {'type': ModelType.to_type_from_kind[obj.kind()],
                    'key': obj.id()}

        if isinstance(obj, list):
            return [cls._to_json_helper(i) for i in obj]

        if isinstance(obj, dict):
            dic = {}
            for i in obj:
                dic[i] = cls._to_json_helper(obj[i])
            return dic

        if isinstance(obj, datetime.datetime):
            return obj.isoformat()

        return obj

    @classmethod
    def to_model(cls, json_str):
        """
        Converts a JSON dict into an ndb model
        """
        dic = json.loads(json_str)
        model = ModelType.from_type[dic['model_type']]()
        for key, prop in model._properties.items():  # _properties is okay to use. see https://code.google.com/p/appengine-ndb-experiment/issues/detail?id=187
            if key in dic:  # check if model description has changed
                setattr(model, key, cls._to_model_helper(prop, dic[key], prop._repeated))
        setattr(model, 'key', ndb.Key(ModelType.from_type[dic['key']['type']], dic['key']['key']))
        return model

    @classmethod
    def _to_model_helper(cls, prop, data, is_repeated):
        """
        Helper function to deal with repeated properties
        """
        if is_repeated:
            return [cls._to_model_helper(prop, d, False) for d in data]
        else:
            if isinstance(prop, ndb.model.KeyProperty):
                return ndb.Key(ModelType.from_type[data['type']], data['key'])

            if isinstance(prop, ndb.model.DateTimeProperty):
                return iso8601.parse_date(data).replace(tzinfo=None)

            return data
