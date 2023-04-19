"""
Gunicorn configuration file
"""
from gunicorn.app.base import Application
from gunicorn import util


class OnlyLegs(Application):
    """
    Gunicorn application
    """

    # TODO: Make this not shit, thanks
    def __init__(self, options={}):  # skipcq: PYL-W0231 # pylint: disable=W0231
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
    def prog():  # skipcq: PYL-E0202 # pylint: disable=E0202, C0116
        return "OnlyLegs"

    def load(self):
        return util.import_app("onlylegs:create_app()")
