import os, sys
from datetime import datetime



ROOT_DIR = os.path.join(os.path.dirname(__file__), '../')
SCRIPTS_DIR = os.path.join(ROOT_DIR, 'scripts')
GYM_DIR = os.path.join(ROOT_DIR, 'Raas_gym')

sys.path.append(GYM_DIR)


def get_raas_gym_dir():
    return GYM_DIR
