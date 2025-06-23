#Imports of high level services and be wired up to menus
#thin loop that calls all data models

import json, sys, os
from models import LoginData, Pokemon
import users


users.app()

