print("""
  ___        _       _
 / _ \ _ __ | |_   _| |    ___  __ _ ___
| | | | '_ \| | | | | |   / _ \/ _` / __|
| |_| | | | | | |_| | |__|  __/ (_| \__ \ 
 \___/|_| |_|_|\__, |_____\___|\__, |___/
               |___/           |___/
Created by Fluffy Bean - Version 23.03.11
""")


import argparse


parser = argparse.ArgumentParser(description='Run the OnlyLegs gallery')
parser.add_argument('-p', '--port', type=int, default=5000, help='Port to run on')
parser.add_argument('-a', '--address', type=str, default='0.0.0.0', help='Address to run on')
parser.add_argument('-w', '--workers', type=int, default=4, help='Number of workers to run')
parser.add_argument('-d', '--debug', type=bool, default=False, help='Run as Flask app in debug mode')
args = parser.parse_args()

PORT = args.port
ADDRESS = args.address
WORKERS = args.workers


if args.debug:
    from gallery import create_app
    create_app().run(host=ADDRESS, port=PORT, debug=True)
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
            return util.import_app('gallery:create_app()')

    OnlyLegs({'bind': f'{ADDRESS}:{PORT}', 'workers': WORKERS}).run()

# uwu
