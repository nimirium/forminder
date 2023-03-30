from IPython import embed
from dotenv import load_dotenv
from src.models.connect import connect_to_mongo

from src.models.form import *
from src.models.schedule import *

load_dotenv()

connect_to_mongo()

# Create an Interactive Console with the local variables
embed(colors='Linux')
