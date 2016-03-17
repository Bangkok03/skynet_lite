from flask import Flask

app = Flask(__name__)

from .views import historic
from .views import index
from .views import live