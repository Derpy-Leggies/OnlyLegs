import logging
import os
from datetime import datetime

# Prevent werkzeug from logging
logging.getLogger('werkzeug').disabled = True


class logger:
    def innit_logger(app):
        filepath = os.path.join(app.root_path, 'user', 'logs')
        #filename = f'onlylogs_{datetime.now().strftime("%Y%m%d")}.log'
        filename = 'only.log'

        if not os.path.isdir(filepath):
            os.mkdir(filepath)

        logging.basicConfig(
            filename=os.path.join(filepath, filename),
            level=logging.INFO,
            datefmt='%Y-%m-%d %H:%M:%S',
            format=
            '%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s',
            encoding='utf-8')

    """
    Login and Auth error codes
    --------------------------
    100: Login
    101: Login attempt
    102: Login attempt (password error)
    103: Logout
    104: Registration
    105: Auth error

    Account error codes - User actions
    ----------------------------------
    200: Account password reset
    201: Account email change
    202: Account delete
    203: Account error

    Image error codes
    -----------------
    300: Image upload
    301: Image delete
    302: Image edit
    303: Image error

    Group error codes
    -----------------
    400: Group create
    401: Group delete
    402: Group edit
    403: Group error

    User error codes - Admin actions
    --------------------------------
    500: User delete
    501: User edit
    502: User ban
    503: User unban
    504: User permission change
    505: User error

    Server and Website errors - Internal
    ------------------------------------
    600: Server error
    601: Server crash
    602: Website error
    603: Website crash
    604: Maintenance
    605: Startup
    606: Other
    621: :3
    """

    def add(error, message):
        # Allowed error codes, as listed above
        log_levels = [
            100, 101, 102, 103, 104, 105, 200, 201, 202, 203, 300, 301, 302,
            303, 400, 401, 402, 403, 500, 501, 502, 503, 504, 505
        ]
        
        if error in log_levels:
            logging.log(logging.INFO, f'[{error}] {message}')
        else:
            logging.log(logging.WARN, f'[606] Improper use of error code {error}')

    def server(error, message):
        log_levels = {
            600: logging.ERROR,
            601: logging.CRITICAL,
            602: logging.ERROR,
            603: logging.CRITICAL,
            604: logging.DEBUG,
            605: logging.DEBUG,
            606: logging.INFO,
            621: logging.INFO,
        }

        if error in log_levels:
            logging.log(log_levels[error], f'[{error}] {message}')
        else:
            logging.log(logging.WARN, f'[606] Invalid error code {error}')
            
    def filename():
        handler = logging.getLogger().handlers[0]
        filename = handler.baseFilename
        
        return filename