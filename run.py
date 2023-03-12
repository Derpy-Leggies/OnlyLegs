print("""
  ___        _       _
 / _ \ _ __ | |_   _| |    ___  __ _ ___
| | | | '_ \| | | | | |   / _ \/ _` / __|
| |_| | | | | | |_| | |__|  __/ (_| \__ \ 
 \___/|_| |_|_|\__, |_____\___|\__, |___/
               |___/           |___/
Created by Fluffy Bean - Version 23.03.12
""")


from setup.args import PORT, ADDRESS, WORKERS, DEBUG
from setup.configuration import Configuration


Configuration()  # Run pre-checks


if DEBUG:
    from gallery import create_app
    
    create_app().run(host=ADDRESS, port=PORT, debug=True, threaded=True)
else:
    from setup.runner import OnlyLegs
    
    options = {
        'bind': f'{ADDRESS}:{PORT}',
        'workers': WORKERS,
    }
    
    OnlyLegs(options).run()

