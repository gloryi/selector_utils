import pygame as backend
import time
import random
import csv
import re
import subprocess
import pyautogui

from time_utils import global_timer, Counter, Progression
from config import (
        # /mnt/X/ARCH_META/Pictures
    W,
    H,
    BPM,
    CYRILLIC_FONT,
    CHINESE_FONT,
)
from config import HAPTIC_CORRECT_CMD, HAPTIC_ERROR_CMD, TEST
from colors import white, hex_to_rgb
import colors
from text_morfer import textMorfer
from filesutils import prepare_arg_parser, read_input
from filesutils import write_output, resolve_cli_arg
from visualisers import FsVisualiser
from controls import KeyboardChainModel
from modes import SwipeMode, SortMode

SCREEN_X_0 = 3400
SCREEN_Y_0 = 0

cli_args = prepare_arg_parser().parse_args()
data_prepared = resolve_cli_arg(cli_args)

if data_prepared == "DONE":
    raise ("Data generated as it' supposed to do")
    a = 0 / 0
    exit()


def clip_color(_):
    return 0 if _ <= 0 else 255 if _ >= 255 else int(_)


def inter_color(v1, v2, p):
    return clip_color(v1 + (v2 - v1) * p)


def interpolate(col1, col2, percent):
    return (
        inter_color(col1[0], col2[0], percent),
        inter_color(col1[1], col2[1], percent),
        inter_color(col1[2], col2[2], percent),
    )


feature_bg = hex_to_rgb("#2E849E")
col_bt_pressed = hex_to_rgb("#4E52AF")
red2 = hex_to_rgb("#700F3C")
option_fg = hex_to_rgb("#68A834")
quadra_col_1 = feature_bg
quadra_col_2 = col_bt_pressed

display_surface = backend.display.set_mode((W, H))
time_to_appear = 4000
beat_time = 0
paused = True
paused_manually = True
is_pause_displayed = False
burner_casted = False

# INIT
keyboard_processor = KeyboardChainModel()
visualiser_type = FsVisualiser
model = SwipeMode

if data_prepared["datatype"] == "files":
    visualiser_type = FsVisualiser
elif data_prepared["datatype"] == "text":
    visualiser_type = FsVisualiser
#  elif data_prepared["datatype"] == "pdf":
#      visualiser_type = PdfVisualiser
#  elif data_prepared["datatype"] == "weblinks":
#      visualiser_type = WebLinksVisualiser
#  elif data_prepared["datatype"] == "webrecursive"]:
#      visualiser_type == WebResursiveVisualiser
#
if cli_args.mode == "groupping":
    model = SwipeMode
elif cli_args.mode == "sorting":
    model = SortMode
#  elif cli_args.model == "connecting":
#      model = ConnectModel
#


data_prepared["decisions"] = data_prepared["modes"][cli_args.mode][cli_args.submode]
del data_prepared["modes"]

model_in_work = model(visualiser_type, display_surface, data_prepared)


backend.init()

quadra_r = 0
quadra_phase = "INHALE"
trans_surface = backend.Surface((H, H))
trans_surface_2 = backend.Surface((W, H))
trans_surface.set_alpha(15)
trans_surface_2.set_alpha(70)
trans_surface.fill((40, 0, 40))
trans_surface_2.fill((40, 0, 40))

delta_timer = global_timer(backend)
quadra_timer = Counter(bpm=15)
morfer_timer = Counter(bpm=12)
pause_counter = Counter(bpm=1 / 5)
#pause_counter = Counter(bpm=1)
wait_extra_time = False

#timer_1m = Counter(bpm=1)
timer_1m = Counter(bpm=1 / 2)
haptic_timer = Counter(bpm=15)
disable_haptic = False
timer_dropped = False

tokens_1m = []
tokens_key = backend.K_k


font = backend.font.Font(CYRILLIC_FONT, 200)
backend.event.set_allowed([backend.QUIT, backend.KEYDOWN, backend.KEYUP])
backend.mouse.set_visible(False)
fpsClock = backend.time.Clock()
morfer = textMorfer()

meta = ""
meta_minor = []

base_font_hz = backend.font.Font(CHINESE_FONT, 50)
base_font_reg = backend.font.Font(CYRILLIC_FONT, 50)
minor_font_hz = backend.font.Font(CYRILLIC_FONT, 25)
minor_font_reg = backend.font.Font(CYRILLIC_FONT, 25)


def place_text(
    text,
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
    display_surface.blit(text, textRect)


for time_delta in delta_timer:
    fpsClock.tick(27)
    if morfer_timer.is_tick(time_delta):
        morfer.update_seed()

    if paused and not is_pause_displayed:
        display_surface.fill(colors.white)

        timer_expired = timer_1m.is_tick(time_delta)

        if timer_expired and not timer_dropped:
            timer_dropped = True

        if timer_dropped:
            if haptic_timer.is_tick(time_delta):
                pass
                #  if HAPTIC_ERROR_CMD and not disable_haptic:
                #      subprocess.Popen(["bash", HAPTIC_ERROR_CMD])

        if quadra_timer.is_tick(time_delta):
            if quadra_phase == "INHALE":
                quadra_phase = "HOLD_IN"
                quadra_col_1 = colors.col_bt_pressed
                quadra_col_2 = colors.red2
            elif quadra_phase == "HOLD_IN":
                quadra_phase = "EXHALE"
                quadra_col_1 = colors.red2
                quadra_col_2 = colors.option_fg
            elif quadra_phase == "EXHALE":
                quadra_phase = "HOLD_OUT"
                quadra_col_1 = colors.option_fg
                quadra_col_2 = colors.feature_bg
            else:
                quadra_phase = "INHALE"
                quadra_col_1 = colors.feature_bg
                quadra_col_2 = colors.col_bt_pressed

        if quadra_phase == "INHALE":
            quadra_w_perce1 = quadra_timer.get_percent()
            quadra_w_perce2 = 1.0
        elif quadra_phase == "HOLD_IN":
            quadra_w_perce1 = 1.0
            quadra_w_perce2 = 1 - quadra_timer.get_percent()
        elif quadra_phase == "EXHALE":
            quadra_w_perce1 = 1 - quadra_timer.get_percent()
            quadra_w_perce2 = 0.0
        else:
            quadra_w_perce1 = 0.0
            quadra_w_perce2 = quadra_timer.get_percent()

        trans_surface_2.fill(
            interpolate(
                quadra_col_1, quadra_col_2, (1.0 - quadra_timer.get_percent()) ** 3
            )
        )

        backend.draw.circle(
            trans_surface_2,
            interpolate(quadra_col_1, quadra_col_2, quadra_timer.get_percent()),
            (W // 2, H // 2),
            (H // 2 - 100) * quadra_w_perce1 + 100,
        )
        backend.draw.circle(
            trans_surface_2,
            interpolate(quadra_col_1, quadra_col_2, quadra_timer.get_percent() ** 2),
            (W // 2, H // 2),
            (H // 2 - 50) * quadra_w_perce2 + 50,
            width=3,
        )

        display_surface.blit(trans_surface_2, (0, 0))

        if meta_minor:
            back_t_found = False

            for i, line in enumerate(meta_minor):

                if "*** 1XTEXT ***" in line:
                    back_t_found = True

                if not back_t_found and not "#" in line:
                    continue

                place_text(
                    line,
                    W // 2,
                    H // 8 + 25 * (i + 1),
                    transparent=True,
                    renderer=minor_font_reg
                    if not re.findall(r"[\u4e00-\u9fff]+", line)
                    else minor_font_hz,
                    base_col=(colors.col_bt_pressed),
                )

        if not timer_dropped:
            backend.draw.rect(
                display_surface,
                interpolate(quadra_col_1, quadra_col_2, timer_1m.get_percent() ** 2),
                (
                    (W // 2 - ((W // 2) * (1 - timer_1m.get_percent()))),
                    H // 2 - 40,
                    ((W) * (1 - timer_1m.get_percent())),
                    80,
                ),
            )

        tokens_repr = " ".join(
            str(i + 1) + random.choice("+!$*=") for i, _ in enumerate(tokens_1m)
        )
        place_text(
            tokens_repr,
            W // 2,
            H // 32,
            transparent=True,
            renderer=base_font_reg,
            base_col=interpolate(
                quadra_col_1, quadra_col_2, 1 - quadra_timer.get_percent()
            ),
        )

    if paused:
        backend.display.update()
        keys = backend.key.get_pressed()
        if keys[backend.K_SPACE]:
            if paused_manually or timer_dropped:
                paused = False
                is_pause_displayed = False
                burner_casted = False
                disable_haptic = False

        if keys[tokens_key] and not timer_dropped:
            if tokens_key == backend.K_k:
                tokens_key = backend.K_d
            else:
                tokens_key = backend.K_k
            tokens_1m.append("*")
            if HAPTIC_CORRECT_CMD and not disable_haptic:
                subprocess.Popen(["bash", HAPTIC_CORRECT_CMD])
            if len(tokens_1m) > 5:
                tokens_1m = []

        for event in backend.event.get():
            if event.type == backend.QUIT:
                backend.quit()
                quit()
        continue

    display_surface.fill(colors.white)

    pause_counter_ticked = pause_counter.is_tick(time_delta)

    if pause_counter_ticked:

        paused = True
        paused_manually = False
        tokens_1m = []
        timer_1m.drop_elapsed()
        timer_dropped = False
        pause_counter.overtime = 0

    if quadra_timer.is_tick(time_delta):
        if quadra_phase == "INHALE":
            quadra_phase = "HOLD_IN"
            quadra_col_1 = col_bt_pressed
            quadra_col_2 = red2
        elif quadra_phase == "HOLD_IN":
            quadra_phase = "EXHALE"
            quadra_col_1 = red2
            quadra_col_2 = option_fg
        elif quadra_phase == "EXHALE":
            quadra_phase = "HOLD_OUT"
            quadra_col_1 = option_fg
            quadra_col_2 = feature_bg
        else:
            quadra_phase = "INHALE"
            quadra_col_1 = feature_bg
            quadra_col_2 = col_bt_pressed

    if quadra_phase == "INHALE":
        quadra_w_perce1 = quadra_timer.get_percent()
        quadra_w_perce2 = 1.0
    elif quadra_phase == "HOLD_IN":
        quadra_w_perce1 = 1.0
        quadra_w_perce2 = 1 - quadra_timer.get_percent()
    elif quadra_phase == "EXHALE":
        quadra_w_perce1 = 1 - quadra_timer.get_percent()
        quadra_w_perce2 = 0.0
    else:
        quadra_w_perce1 = 0.0
        quadra_w_perce2 = quadra_timer.get_percent()

    # HORISONTAL
    backend.draw.rect(
        display_surface,
        interpolate(quadra_col_1, quadra_col_2, quadra_timer.get_percent()),
        (W // 2 - ((W // 2) * (quadra_w_perce1)), H - 20, (W) * quadra_w_perce1, 20),
    )
    backend.draw.rect(
        display_surface,
        interpolate(quadra_col_1, quadra_col_2, quadra_timer.get_percent()),
        (W // 2 - ((W // 2) * (quadra_w_perce1)), 0, (W) * quadra_w_perce1, 20),
    )

    # VERTICAL
    backend.draw.rect(
        display_surface,
        interpolate(quadra_col_1, quadra_col_2, quadra_timer.get_percent()),
        (W - 40, H // 2 - ((H // 2) * (quadra_w_perce1)), 40, (H) * quadra_w_perce1),
    )

    backend.draw.rect(
        display_surface,
        interpolate(quadra_col_1, quadra_col_2, quadra_timer.get_percent()),
        (0, H // 2 - ((H // 2) * (quadra_w_perce1)), 40, (H) * quadra_w_perce1),
    )

    model_in_work.tick(time_delta)
    if model_in_work.completed():
        write_output(
            cli_args.submode,
            cli_args.dataid,
            model_in_work.prodce_results()
        )
        backend.quit()
        quit()

    backend.display.update()

    keys = backend.key.get_pressed()

    if keys[backend.K_v]:
        paused = True
        paused_manually = True
        tokens_1m = []
        timer_1m.drop_elapsed()
        timer_dropped = False

    for event in backend.event.get():

        if event.type == backend.QUIT:
            backend.quit()

            quit()

backend.quit()
