import os, sys
from datetime import datetime


ROOT_DIR = os.path.join(os.path.dirname(__file__), "../")
SCRIPTS_DIR = os.path.join(ROOT_DIR, "scripts")
GYM_DIR = os.path.join(ROOT_DIR, "raas-gym")
HARDWARE_DIR = os.path.join(ROOT_DIR, "hardware")

sys.path.append(GYM_DIR)
sys.path.append(HARDWARE_DIR)


def get_raas_gym_dir():
    return GYM_DIR


def get_hardware_dir():
    return HARDWARE_DIR
