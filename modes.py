from time_utils import Counter
import pygame as backend
import colors
import random
from config import (
    W,
    H,
    BPM,
    CYRILLIC_FONT,
    CHINESE_FONT,
)
from controls import KeyboardChainModel
from colors import white, hex_to_rgb
import colors
from text_morfer import textMorfer
import re

backend.init()

morfer = textMorfer()
base_font_hz = backend.font.Font(CHINESE_FONT, 50)
base_font_reg = backend.font.Font(CYRILLIC_FONT, 50)
minor_font_hz = backend.font.Font(CYRILLIC_FONT, 25)
minor_font_reg = backend.font.Font(CYRILLIC_FONT, 25)


def place_text(
    text,
    display,
    x,
    y,
    transparent=False,
    renderer=None,
    base_col=(80, 80, 80),
    forbid_morf=True,
):
    if not forbid_morf:
        text = morfer.morf_text(text)
    if renderer is None:
        renderer = (
            base_font_reg
            if not re.findall(r"[\u4e00-\u9fff]+", text)
            else base_font_hz,
        )

    if isinstance(renderer, tuple) or isinstance(renderer, list):
        renderer = renderer[0]
    if not transparent:
        text = renderer.render(text, True, base_col, (150, 150, 151))
    else:
        text = renderer.render(text, True, base_col)
    textRect = text.get_rect()
    textRect.center = (x, y)
    display.blit(text, textRect)


MODES = ["groupping", "sorting"]
DATA_POSITIONS = {}
DATA_POSITIONS[1] = []
DATA_POSITIONS[1].append([W // 2, 5 * H // 6 - H // 6])
DATA_POSITIONS[2] = []
DATA_POSITIONS[2].append([W // 6 + W // 6, H // 6 + H // 6])
DATA_POSITIONS[2].append([5 * W // 6 - W // 6, 5 * H // 6 - H // 6])
DATA_POSITIONS[3] = []
DATA_POSITIONS[3].append([W // 6 + W // 6, H // 6 + H // 6])
DATA_POSITIONS[3].append([W // 2, 5 * H // 6 - H // 6])
DATA_POSITIONS[3].append([5 * W // 6 - W // 6, H // 6 + H // 6])
DATA_POSITIONS[4] = []
DATA_POSITIONS[4].append([W // 6 + W // 6, H // 6 + H // 6])
DATA_POSITIONS[4].append([W // 6 + W // 6, 5 * H // 6 - H // 6])
DATA_POSITIONS[4].append([5 * W // 6 - W // 6, 5 * H // 6 - H // 6])
DATA_POSITIONS[4].append([5 * W // 6 - W // 6, H // 6 + H // 6])
DATA_POSITIONS[5] = []
DATA_POSITIONS[5].append([W // 6, H // 6 + H // 12])
DATA_POSITIONS[5].append([W // 6, 5 * H // 6 - H // 12])
DATA_POSITIONS[5].append([W // 2, 5 * H // 6 - H // 12])
DATA_POSITIONS[5].append([5 * W // 6, 5 * H // 6 - H // 12])
DATA_POSITIONS[5].append([5 * W // 6, H // 6 + H // 12])
DATA_POSITIONS[6] = []
DATA_POSITIONS[6].append([W // 2, H // 6 + H // 12])
DATA_POSITIONS[6].append([W // 6, H // 6 + H // 12])
DATA_POSITIONS[6].append([W // 6, 5 * H // 6 - H // 12])
DATA_POSITIONS[6].append([W // 2, 5 * H // 6 - H // 12])
DATA_POSITIONS[6].append([5 * W // 6, 5 * H // 6 - H // 12])
DATA_POSITIONS[6].append([5 * W // 6, H // 6 + H // 12])

KEYS_POSITIONS = {}
KEYS_POSITIONS[1] = []
KEYS_POSITIONS[1].append([W // 2, H - H // 16])
KEYS_POSITIONS[2] = []
KEYS_POSITIONS[2].append([W // 16, H // 2 ])
KEYS_POSITIONS[2].append([W - W // 16 , H // 2])
KEYS_POSITIONS[3] = []
KEYS_POSITIONS[3].append([W // 16, H // 2 ])
KEYS_POSITIONS[3].append([W - W // 16 , H // 2 ])
KEYS_POSITIONS[3].append([W // 2, H - H//32 ])
KEYS_POSITIONS[4] = []
KEYS_POSITIONS[4].append([W // 16, H // 2 ])
KEYS_POSITIONS[4].append([W - W // 16 , H // 2 ])
KEYS_POSITIONS[4].append([W // 2, H//32 ])
KEYS_POSITIONS[4].append([W // 2, H  - H//16 ])

KEY_SETS = {}
KEY_SETS[1] = ["b"]
KEY_SETS[2] = ["f", "j"]
KEY_SETS[3] = ["f", "b", "j"]
KEY_SETS[4] = ["f", "j", "y", "b"]

class SwipeMode:
    def __init__(S, visualiser_type, display_surface, data):
        S.cooldown = False
        S.cooldown_timer = Counter(bpm=20)
        S.data = data
        S.decision_points = data["decisions"]
        #print(S.decision_points)
        S.display = display_surface
        S.visualiser = visualiser_type(
            display_surface,
            W // 2,
            H // 2,
            W // 2 - W // 3,
            H // 8,
            W // 2 + W // 3,
            H - H // 8,
        )
        S.keys_poses = KEYS_POSITIONS[len(S.decision_points)]
        S.keys_set = KEY_SETS[len(S.decision_points)]
        S.keys_mapping = [[_,S.keys_set[i]] for (i,_) in enumerate(S.decision_points)]
        S.data_swiped = [] 
        S.data_unswiped = data["payload"] 
        random.shuffle(S.data_unswiped)
        S.active_element = S.data_unswiped.pop()
        S.visualiser.add_entity(S.active_element)
        S.keyboard_processor = KeyboardChainModel()

    def tick(S, time_delta):
        if not S.data_unswiped:
            return
        S.visualiser.tick(time_delta)

        if S.cooldown_timer.is_tick(time_delta):
            S.cooldown = False

        keys_pressed = S.keyboard_processor.get_pressed()

        for group, key in S.keys_mapping:
            if key in keys_pressed and not S.cooldown:
                S.data_swiped.append([group, S.active_element])
                S.active_element = S.data_unswiped.pop()
                S.visualiser.add_entity(S.active_element)
                S.cooldown = True
                S.cooldown_timer.drop_elapsed()

        for position, decision_point in zip(S.keys_poses, S.decision_points):
            place_text(
                decision_point,
                S.display, 
                position[0],
                position[1],
                base_col=colors.col_bt_text if S.cooldown else colors.col_active_darker,
            )

    def completed(S):
        return len(S.data_unswiped) == 0

    def prodce_results(S):
        return S.data_swiped

class SortMode:
    def __init__(S, visualiser_type, display_surface, data):
        S.cooldown = False
        S.cooldown_timer = Counter(bpm=20)
        S.data = data

        S.decision_points = ["left", "right", 'parity']

        S.display = display_surface
        S.visualiser = visualiser_type(
            display_surface,
            W // 2,
            H // 2,
            W // 2 - W // 3,
            H // 8,
            W // 2 + W // 3,
            H - H // 8,
        )

        S.keys_poses = KEYS_POSITIONS[len(S.decision_points)]
        S.keys_set = KEY_SETS[len(S.decision_points)]
        S.keys_mapping = [[_,S.keys_set[i]] for (i,_) in enumerate(S.decision_points)]
        S.keyboard_processor = KeyboardChainModel()

        S.comparing_pair = []
        S.data_unswiped = data["payload"] 
        random.shuffle(S.data_unswiped)

        #  S.sorter = S.sorting(S.data_unswiped)
        #  S.sorter = S.cocktail_sort(S.data_unswiped)
        S.sorter = S.quickSortIterative(S.data_unswiped)
        S.comparator_val = "parity"

        next(S.sorter)
        print("init gen", S.active_element)
        

        if not S.active_element:
            next(S.sorter)

        S.visualiser.add_entity(S.active_element)

    def cocktail_sort(S, array):
        swap = True
        start = 0 #first
        end = len(array) - 1 #last
        while (swap == True):
            swap = False
            for a in range(start, end):

                pair = [array[a], array[a+1]]
                S.active_element = pair
                yield None
                compared = S.comparator_val

                if compared == "greater":
                    array[a], array[a+1] = array[a+1], array[a]
                    swap = True
            if(swap == False):
                end = end-1
            for a in range(end-1, start-1, -1):

                pair = [array[a], array[a+1]]
                S.active_element = pair
                yield None
                compared = S.comparator_val

                if compared == "greater":
                    array[a], array[a+1] = array[a+1], array[a]
                    swap = True
            start = start+1

        array = [[i,_] for (i,_) in enumerate(array)]
        S.data_unswiped = array
        S.active_element = "Finished"
        yield "Finished"

    def sorting(S, new_list):
        for l in range(len(new_list)):
            for m in range(0, len(new_list) - l - 1):

                pair = [new_list[m], new_list[m+1]]
                S.active_element = pair

                yield None

                compared = S.comparator_val

                print(compared)
                if compared == "greater":
                    temp = new_list[m]
                    new_list[m] = new_list[m+1]
                    new_list[m+1] = temp

        new_list = [[i,_] for (i,_) in enumerate(new_list)]
        S.data_unswiped = new_list

        S.active_element = "Finished"
        yield "Finished"

    def quickSortIterative(S, arr):

        l = 0
        h = len(arr)-1

        size = h - l + 1
        stack = [0] * (size)

        top = -1

        top = top + 1
        stack[top] = l
        top = top + 1
        stack[top] = h

        while top >= 0:

            h = stack[top]
            top = top - 1
            l = stack[top]
            top = top - 1

            # p = partition( arr, l, h )
            _i = ( l - 1 )
            _x = arr[h]

            for _j in range(l , h):

                pair = [arr[_j], _x]
                S.active_element = pair
                yield None
                compared = S.comparator_val

                if compared == "less" or compared == "parity":

                    _i = _i+1
                    arr[_i],arr[_j] = arr[_j],arr[_i]

            arr[_i+1],arr[h] = arr[h],arr[_i+1]
            p = (_i+1)

            if p-1 > l:
                top = top + 1
                stack[top] = l
                top = top + 1
                stack[top] = p - 1

            if p+1 < h:
                top = top + 1
                stack[top] = p + 1
                top = top + 1
                stack[top] = h

        new_list = [[i,_] for (i,_) in enumerate(arr)]
        S.data_unswiped = new_list

        S.active_element = "Finished"
        yield "Finished"


    def tick(S, time_delta):
        if not S.data_unswiped:
            return
        S.visualiser.tick(time_delta)

        if S.cooldown_timer.is_tick(time_delta):
            S.cooldown = False

        keys_pressed = S.keyboard_processor.get_pressed()

        for group, key in S.keys_mapping:
            if key in keys_pressed and not S.cooldown:

                if group == "left":
                    S.comparator_val = "greater"
                elif group == "right":
                    S.comparator_val = "less"
                else:
                    S.comparator_val = "parity"

                next(S.sorter)
                if S.active_element == "Finished":
                    S.data_swiped = S.data_unswiped
                    S.data_unswiped = []

                S.cooldown = True
                S.cooldown_timer.drop_elapsed()

                S.visualiser.add_entity(S.active_element, drop_queue = True)


        for position, decision_point in zip(S.keys_poses, S.decision_points):
            place_text(
                decision_point,
                S.display, 
                position[0],
                position[1],
                base_col=colors.col_bt_text if S.cooldown else colors.col_active_darker,
            )

    def completed(S):
        return len(S.data_unswiped) == 0

    def prodce_results(S):
        return S.data_swiped
