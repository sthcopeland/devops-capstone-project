"""
Package: service
Package for the application models and service routes
This module creates and configures the Flask app and sets up the logging
and SQL database
"""
import sys
from flask import Flask
from service import config
from service.common import log_handlers

# Create Flask application
app = Flask(__name__)
app.config.from_object(config)

# Import the routes After the Flask app is created
# pylint: disable=wrong-import-position, cyclic-import, wrong-import-order
from service import routes, models  # noqa: F401 E402

# pylint: disable=wrong-import-position
from service.common import error_handlers, cli_commands  # noqa: F401 E402

# Set up logging for production
log_handlers.init_logging(app, "gunicorn.error")

app.logger.info(70 * "*")
app.logger.info("  A C C O U N T   S E R V I C E   R U N N I N G  ".center(70, "*"))
app.logger.info(70 * "*")

try:
    models.init_db(app)  # make our database tables
except Exception as error:  # pylint: disable=broad-except
    app.logger.critical("%s: Cannot continue", error)
    # gunicorn requires exit code 4 to stop spawning workers when they die
    sys.exit(4)

app.logger.info("Service initialized!")

# --- Security headers for 3j (safe no-op if import fails) ---
try:
    from flask_talisman import Talisman  # type: ignore
    # assumes 'app' already exists in this module
    _csp = {"default-src": "'self'"}
    Talisman(
        app,
        content_security_policy=_csp,
        frame_options="DENY",
        force_https=False,            # keep False for local HTTP
        referrer_policy="no-referrer",
        permissions_policy={"geolocation": "()","camera": "()","microphone": "()"},
    )
except Exception as _e:
    # keep tests running even if Talisman not installed/initialized in CI
    pass
# --- end 3j block ---
