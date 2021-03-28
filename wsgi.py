"""Application entry point."""

import sys
#sys.path.append('/usr/local/lib/python3.8/dist-packages')

from api import create_app 

#from api import create_app as application

app = create_app()

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug="True") #ssl_context='adhoc')

