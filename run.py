"""
Run script for OnlyLegs
"""
from setup.args import PORT, ADDRESS, WORKERS, DEBUG
from setup.configuration import Configuration


print("""
 ::::::::  ::::    ::: :::     :::   ::: :::        ::::::::: :::::::::   ::::::::
:+:    :+: :+:+:   :+: :+:     :+:   :+: :+:        :+:       :+:    :+: :+:    :+:
+:+    +:+ :+:+:+  +:+ +:+      +:+ +:+  +:+        +:+       +:+        +:+
+#+    +:+ +#+ +:+ +#+ +#+       +#++:   +#+        +#++:++#  :#:        +#++:++#++
+#+    +#+ +#+  +#+#+# +#+        +#+    +#+        +#+       +#+   +#+#        +#+
#+#    #+# #+#   #+#+# #+#        #+#    #+#        #+#       #+#    #+# #+#    #+#
 ########  ###    #### ########## ###    ########## ######### #########   ########
 
                     Created by Fluffy Bean - Version 23.03.30
""")


# Run pre-startup checks and load configuration
Configuration()


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
