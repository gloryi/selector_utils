import pygame as BACK
from collections import OrderedDict


keys_mapping = {}

keys_mapping["q"] = BACK.K_q
keys_mapping["w"] = BACK.K_w
keys_mapping["e"] = BACK.K_e
keys_mapping["r"] = BACK.K_r
keys_mapping["t"] = BACK.K_t
keys_mapping["y"] = BACK.K_y
keys_mapping["u"] = BACK.K_u
keys_mapping["i"] = BACK.K_i
keys_mapping["o"] = BACK.K_o
keys_mapping["p"] = BACK.K_p
keys_mapping["a"] = BACK.K_a
keys_mapping["s"] = BACK.K_s
keys_mapping["d"] = BACK.K_d
keys_mapping["f"] = BACK.K_f
keys_mapping["g"] = BACK.K_g
keys_mapping["h"] = BACK.K_h
keys_mapping["j"] = BACK.K_j
keys_mapping["k"] = BACK.K_k
keys_mapping["l"] = BACK.K_l
keys_mapping["z"] = BACK.K_z
keys_mapping["x"] = BACK.K_x
keys_mapping["c"] = BACK.K_c
keys_mapping["v"] = BACK.K_v
keys_mapping["b"] = BACK.K_b
keys_mapping["n"] = BACK.K_n
keys_mapping["m"] = BACK.K_m
keys_mapping["select"] = BACK.K_SPACE


def get_key_code(key):
    if key in keys_mapping:
        return keys_mapping[key]
    else:
        print(f"key {key} is undefined")
        return keys_mapping["select"]


class KeyboardChainModel:
    def __init__(S):
        S.up = "up"
        S.down = "down"
        S.pressed = "pressed"
        S.mapping = OrderedDict()
        keys = [
            "q",
            "w",
            "e",
            "r",
            "t",
            "y",
            "u",
            "i",
            "o",
            "p",
            "a",
            "s",
            "d",
            "f",
            "g",
            "h",
            "j",
            "k",
            "l",
            "z",
            "x",
            "c",
            "v",
            "b",
            "n",
            "m",
            "select",
        ]
        for key in keys:
            S.mapping[get_key_code(key)] = [key, S.up]

        S.keys = [S.up for _ in range(27)]

    def process_button(S, current_state, new_state):
        if current_state == S.up and new_state == S.down:
            return S.down
        elif current_state == S.down and new_state == S.down:
            return S.down
        elif current_state == S.down and new_state == S.up:
            return S.pressed
        elif current_state == S.pressed and new_state == S.up:
            return S.up
        else:
            return S.up

    def prepare_inputs(S):
        S.keys = list(S.mapping.values())

    def get_inputs(S):
        keys = BACK.key.get_pressed()

        for control_key in S.mapping:
            if keys[control_key]:
                S.mapping[control_key][1] = S.process_button(
                    S.mapping[control_key][1], S.down
                )
            else:
                S.mapping[control_key][1] = S.process_button(
                    S.mapping[control_key][1], S.up
                )

    def get_keys(S):
        S.get_inputs()
        S.prepare_inputs()
        return S.keys

    def get_pressed(S):
        key_states = S.get_keys()
        mark_pressed = lambda _: _[0] if _[1] == "pressed" else ""
        return list(filter(lambda _ : _, [mark_pressed(_) for _ in key_states]))

    #
    #  def process_inputs(S, time_elapsed=0):
    #
    #      key_states = S.control.get_keys()
    #
    #      pressed_keys = S.get_pressed(key_states)
    #
    #      if S.active_entity and any(pressed_keys):
    #          S.active_entity.register_keys(
    #              pressed_keys, S.time_elapsed_cummulative / S.active_beat_time
    #          )
    #      elif S.active_entity:
    #          S.active_entity.register_keys(
    #              pressed_keys,
    #              S.time_elapsed_cummulative / S.active_beat_time,
    #              time_based=True,
    #          )
    #
    #      pressed_mouse = BACK.api().mouse.get_pressed()
    #      if S.active_entity and any(pressed_mouse):
    #          S.active_entity.register_mouse(pressed_mouse)
    #      elif S.active_entity:
    #          S.active_entity.register_idle_mouse()
    #
