"""
Gunicorn configuration file
"""
from gunicorn.app.base import Application
from gunicorn import util


class OnlyLegs(Application):
    """
    Gunicorn application
    """

    def __init__(self, options={}):  # pylint: disable=W0102  skipcq: PYL-W0231
        self.usage = None
        self.callable = None
        self.options = options
        self.do_load_config()

    def init(self, *args):
        """
        Initialize the application
        """
        cfg = {}
        for setting, value in self.options.items():
            if setting.lower() in self.cfg.settings and value is not None:
                cfg[setting.lower()] = value
        return cfg

    @staticmethod
    def prog():  # pylint: disable=C0116  skipcq: PYL-E0202
        return "OnlyLegs"

    def load(self):
        return util.import_app("onlylegs:create_app()")
