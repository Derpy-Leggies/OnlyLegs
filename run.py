"""
Run script for OnlyLegs
"""
from setup.args import PORT, ADDRESS, WORKERS, DEBUG
from setup.configuration import Configuration


print("""
  ___        _       _
 / _ \ _ __ | |_   _| |    ___  __ _ ___
| | | | '_ \| | | | | |   / _ \/ _` / __|
| |_| | | | | | |_| | |__|  __/ (_| \__ \ 
 \___/|_| |_|_|\__, |_____\___|\__, |___/
               |___/           |___/
Created by Fluffy Bean - Version 23.03.23
""")


Configuration()  # Run pre-checks


if DEBUG:
    from gallery import create_app

    # If no address is specified, use localhost
    if not ADDRESS:
        ADDRESS = 'localhost'

    create_app().run(host=ADDRESS, port=PORT, debug=True, threaded=True)
else:
    from setup.runner import OnlyLegs  # pylint: disable=C0412

    # If no address is specified, bind the server to all interfaces
    if not ADDRESS:
        ADDRESS = '0.0.0.0'

    options = {
        'bind': f'{ADDRESS}:{PORT}',
        'workers': WORKERS,
    }

    OnlyLegs(options).run()
