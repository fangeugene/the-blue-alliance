import os

from google.appengine.api import memcache
from template_engine import jinja2_engine

from controllers.base_controller import LoggedInHandler
from helpers.memcache.memcache_webcast_flusher import MemcacheWebcastFlusher

# Main memcache view.


class AdminMemcacheMain(LoggedInHandler):
    def post(self):
        self._require_admin()
        flushed = list()

        if self.request.get("all_keys") == "all_keys":
            memcache.flush_all()
            flushed.append("all memcache values")

        if self.request.get("webcast_keys") == "webcast_keys":
            flushed.append(MemcacheWebcastFlusher.flush())

        if self.request.get('memcache_key') is not "":
            memcache.delete(self.request.get("memcache_key"))
            flushed.append(self.request.get("memcache_key"))

        self.template_values.update({
            "flushed": flushed,
            "memcache_stats": memcache.get_stats(),
        })

        self.response.out.write(jinja2_engine.render('admin/memcache_index.html', self.template_values))

    def get(self):
        self._require_admin()

        self.template_values.update({
            "memcache_stats": memcache.get_stats(),
        })

        self.response.out.write(jinja2_engine.render('admin/memcache_index.html', self.template_values))
