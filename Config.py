import os
from dotenv import load_dotenv

load_dotenv()

# OR, the same with increased verbosity
load_dotenv(verbose=True)

# OR, explicitly providing path to '.env'
from pathlib import Path  # Python 3.6+ only

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)


def env(s):
    return os.getenv("headless.enable")


def envBool(s):
    return env(s) == 'true'


if __name__ == '__main__':
    SECRET_KEY = os.getenv("headless.enable")
    print(SECRET_KEY)
