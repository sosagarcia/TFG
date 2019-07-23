#! /usr/bin/python3

from index import app as application
import logging
import sys
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, '/var/www/html/TFG/')
application.secret_key = 'anything you wish'
