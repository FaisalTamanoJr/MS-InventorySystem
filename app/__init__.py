'''
This file defines what symbols are made available outside and also creates the app package.
'''

from flask import Flask

app = Flask(__name__) # Flask instance. The "__name__" argument is used by Flask as a starting point for loading
# resources.

from app import routes # Although it seems odd, the import was placed here to deal with the circular import issue.