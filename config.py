# API Configuration
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get API key from environment variable
apikey = os.getenv("XAI_API_KEY", "")

if not apikey:
    print("Warning: XAI_API_KEY not set in environment variables")
