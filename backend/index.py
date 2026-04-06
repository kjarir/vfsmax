import os
import sys

# Add the backend directory to sys.path so we can import the app
sys.path.append(os.path.dirname(__file__))

# Import the FastAPI instance
from app.main import app as handler
