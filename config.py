import os
import random
from time import time
from collections import OrderedDict

TEST = True
TEST = False

META_ACTION = os.path.join(
    "/home/gloryi/Documents/SpecialFiles", "action_affirmations.csv"
)
META_ACTION_STACK = OrderedDict()
META_ACTION_STACK["*** 1XBACK ***"] = []
META_ACTION_STACK["*** 1XKEYS ***"] = []
META_ACTION_STACK["*** 1XTEXT ***"] = []
META_ACTION_STACK["*** IBACK ***"] = []
META_ACTION_STACK["*** PERM ***"] = []
META_ACTION_STACK["*** OUT ***"] = []

HAPTIC_FEEDBACK_CMD = os.path.join(os.getcwd(), "controller_features", "example.sh")
HAPTIC_ERROR_CMD = os.path.join(os.getcwd(), "controller_features", "error.sh")
HAPTIC_CORRECT_CMD = os.path.join(os.getcwd(), "controller_features", "correct.sh")

CHINESE_FONT = os.path.join(os.getcwd(), "fonts", "simhei.ttf")
CYRILLIC_FONT = os.path.join(os.getcwd(), "fonts", "NotoSans-SemiBold.ttf")

INDIR = os.path.join(os.getcwd(), "IN")
OUTDIR = os.path.join(os.getcwd(), "OUT")

BPM = 5

W_OFFSET = 200
H_OFFSET = 100

W = 2400 + W_OFFSET * 2
H = 1240 + H_OFFSET * 2 - 11
