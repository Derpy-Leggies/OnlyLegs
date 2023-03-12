print("""
  ___        _       _
 / _ \ _ __ | |_   _| |    ___  __ _ ___
| | | | '_ \| | | | | |   / _ \/ _` / __|
| |_| | | | | | |_| | |__|  __/ (_| \__ \ 
 \___/|_| |_|_|\__, |_____\___|\__, |___/
               |___/           |___/
Created by Fluffy Bean - Version 23.03.12
""")

from setup.args import PORT, ADDRESS, WORKERS, DEBUG, VERBOSE
from setup.configuration import Configuration


# Run prechecks
Configuration(verbose=VERBOSE)


if DEBUG:
    from gallery import create_app
    create_app(verbose=VERBOSE).run(host=ADDRESS, port=PORT, debug=True, threaded=True)
else:
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
            return util.import_app(f'gallery:create_app(verbose={VERBOSE})')
    
    options = {
        'bind': f'{ADDRESS}:{PORT}',
        'workers': WORKERS,
    }
    
    OnlyLegs(options).run()

