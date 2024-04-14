"""
This is the gunicorn config file!

We define some parameters that gunicorn needs to operate.
This configuration file is intended for production environments.
You can use this for local development, but it is not recommended!
"""

# Name of the gunicorn application:
name = "petqs"

# The location of our asgi application
wsgi_app = "main:app"

# Log level
loglevel = "debug"

# Number of worker processes:
# (Should be 2 per core)
workers = 2

# The socket to bind:
bind = "10.8.0.2:4455"  # If running on Owen Machine
#bind = "127.0.0.1:4455"  # If running locally/on production
#bind = "unix:/var/www/html/cardiB/cardiB.sock"

# Write access and error info to /var/log
# accesslog = errorlog = "/var/log/gunicorn/dev.log"

# Redirect stdout/stdin to log file:
capture_output = True

# Save PID to file:
# pidfile = "/var/run/gunicorn/dev.pid"

# Daemonize the Gunicorn process:
# daemon = True

# Preload the app
preload_app = True

# Get around slow operations
timeout = 600
