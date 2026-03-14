import os
from pathlib import Path

# Load .env early so DJANGO_ENV is available
try:
    from dotenv import load_dotenv
    BASE_DIR = Path(__file__).resolve().parent.parent.parent
    env_path = BASE_DIR / '.env'
    if not env_path.exists() and (BASE_DIR / 'env').exists():
        env_path = BASE_DIR / 'env'
    load_dotenv(env_path)
except ImportError:
    pass

env = os.getenv('DJANGO_ENV', 'local').strip().lower()

if env == 'prod':
    from .prod import *
else:
    from .local import *
