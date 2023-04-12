"""
Run script for OnlyLegs
"""
from setup.args import PORT, ADDRESS, WORKERS, DEBUG
from setup.configuration import Configuration


print(
    """
 ::::::::  ::::    ::: :::     :::   ::: :::        ::::::::: :::::::::   ::::::::
:+:    :+: :+:+:   :+: :+:     :+:   :+: :+:        :+:       :+:    :+: :+:    :+:
+:+    +:+ :+:+:+  +:+ +:+      +:+ +:+  +:+        +:+       +:+        +:+
+#+    +:+ +#+ +:+ +#+ +#+       +#++:   +#+        +#++:++#  :#:        +#++:++#++
+#+    +#+ +#+  +#+#+# +#+        +#+    +#+        +#+       +#+   +#+#        +#+
#+#    #+# #+#   #+#+# #+#        #+#    #+#        #+#       #+#    #+# #+#    #+#
 ########  ###    #### ########## ###    ########## ######### #########   ########

                     Created by Fluffy Bean - Version 23.04.12
"""
)


# Run pre-startup checks and load configuration
Configuration()


if DEBUG:
    from onlylegs import create_app

    create_app().run(host=ADDRESS, port=PORT, debug=True, threaded=True)
else:
    from setup.runner import OnlyLegs  # pylint: disable=C0412
    import sys

    # Stop Gunicorn from reading the command line arguments as it causes errors
    sys.argv = [sys.argv[0]]

    options = {
        "bind": f"{ADDRESS}:{PORT}",
        "workers": WORKERS,
    }

    OnlyLegs(options).run()
