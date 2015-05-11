import json
from google.appengine.ext import ndb

from helpers.model_json_converter import ModelJSONConverter


class CachedQueryResult(ndb.Model):
    """
    A CachedQueryResult stores a JSON serialized model or list of models of a single type.
    """
    result_json = ndb.TextProperty(required=True)  # not indexed by default
    additional_results = ndb.KeyProperty(kind='CachedQueryResult')  # if too large for one db entry

    created = ndb.DateTimeProperty(auto_now_add=True)
    updated = ndb.DateTimeProperty(auto_now=True)

    def __init__(self, *args, **kw):
        self._result = None
        super(CachedQueryResult, self).__init__(*args, **kw)

    @property
    def result(self):
        """
        Lazy load result_json
        """
        if self._result is None:
            result = json.loads(self.result_json)
            if isinstance(result, list):
                self._result = [ModelJSONConverter.to_model(r) for r in result]
            else:
                self._result = ModelJSONConverter.to_model(result)
        return self._result
