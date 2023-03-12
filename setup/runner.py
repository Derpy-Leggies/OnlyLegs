from gunicorn.app.base import Application
from gunicorn import util


class OnlyLegs(Application):
    def __init__(self, options={}):
        self.usage = None
        self.callable = None
        self.options = options
        self.do_load_config()
    
    def init(self, *args):
        cfg = {}
        for k, v in self.options.items():
            if k.lower() in self.cfg.settings and v is not None:
                cfg[k.lower()] = v
        return cfg
    
    def prog(self):
        return 'OnlyLegs'
    
    def load(self):
        return util.import_app('gallery:create_app()')
