#!/home2/johnfel1/venv/mlsXcite/bin/python

from flup.server.fcgi import WSGIServer
from myBus import app as application

WSGIServer(application).run()
