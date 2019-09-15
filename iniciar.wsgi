activate_this = '/home/pi/.local/share/virtualenvs/TFG-BHBmWcd9/bin/activate_this.py'
with open(activate_this) as file_:
    exec(file_.read(), dict(__file__=activate_this))

import sys

sys.path.insert(0,"/var/www/html/TFG/")

from index import app as application


