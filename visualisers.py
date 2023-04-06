from config import W, H, CHINESE_FONT, CYRILLIC_FONT
from text_morfer import textMorfer
import os
import pygame as back
import colors
import re
import magic
from itertools import islice

back.init()

font = back.font.Font(CYRILLIC_FONT, 200)
base_font_hz = back.font.Font(CHINESE_FONT, 50)
base_font_reg = back.font.Font(CYRILLIC_FONT, 50)
minor_font_hz = back.font.Font(CYRILLIC_FONT, 25)
minor_font_reg = back.font.Font(CYRILLIC_FONT, 25)
morfer = textMorfer()


def place_text(
    text,
    display_surface,
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


IMG_FRMTS = (".png", ".jpg", ".jpeg", ".tiff", ".bmp", ".gif")
TEXT_FORMTS = (
    "text/cmd",
    "text/css",
    "text/csv",
    "text/html",
    "text/javascript (Obsolete)",
    "text/plain",
    "text/php",
    "text/xml",
    "text/markdown",
    "text/cache-manifest",
    "application/json",
)


class BaseRenderer:
    def __init__(self, entity, xc, yc):
        self.entity = entity
        self.xc = xc
        self.yc = yc

    def render(self, display):
        ...


class FilenameRenderer:
    def __init__(self, entity, xc, yc):
        self.entity = entity
        self.xc = xc
        self.yc = yc

    def render(self, display):
        chunks = [self.entity[i : i + 25] for i in range(0, len(self.entity), 25)]
        for i, chunk in enumerate(chunks):
            place_text(
                chunk,
                display,
                self.xc,
                self.yc + 90 + 50 * (i + 1),
                transparent=True,
                renderer=None,
                base_col=(colors.col_bt_pressed),
            )


class FileRenderer:
    def __init__(self, entity, xc, yc):
        self.entity = entity
        self.xc = xc
        self.yc = yc

    def render(self, display):
        chunks = [self.entity[i : i + 25] for i in range(0, len(self.entity), 25)]

        for i, chunk in enumerate(chunks):
            place_text(
                chunk,
                display,
                self.xc,
                self.yc + 90 + 50 * (i + 1),
                transparent=True,
                renderer=None,
                base_col=(colors.col_bt_pressed),
            )


class ImageRenderer:
    def __init__(self, image, xc, yc):
        self.image = image
        self.xc = xc
        self.yc = yc

    def render(self, display):
        display.blit(
            self.image,
            (
                self.xc - self.image.get_width() // 2,
                self.yc - self.image.get_height() // 2,
            ),
        )


class FsVisualiser:
    def __init__(self, display, xc, yc, x0, y0, x1, y1):
        self.display = display
        self.xc = xc
        self.xcb = xc
        self.yc = yc
        self.ycb = yc
        self.x0 = x0
        self.x0b = x0
        self.y0 = y0
        self.y0b = y0
        self.x1 = x1
        self.x1b = x1
        self.y1 = y1
        self.y1b = y1
        self.rendering_queue = [BaseRenderer("init", self.xc, self.yc)]

    def tick(self, time_elapsed):
        for renderer in self.rendering_queue:
            renderer.render(self.display)

    def add_entity(self, entity, replacing=True, drop_queue=False):

        if drop_queue:
            self.rendering_queue = []

        if isinstance(entity, list):
            # TODO
            self.xcb = self.xc
            self.yb = self.yc
            self.x0b = self.x0
            self.y0b = self.y0
            self.x1b = self.x1
            self.y1b = self.y1

            self.xc = (self.x0b+self.xcb)//2
            self.y = self.ycb

            self.x0 = self.x0b
            self.y0 = self.y0b

            self.x1 = self.xcb
            self.y1 = self.y1b

            self.add_entity(entity[0], replacing = False)

            self.xc = (self.x1b+self.xcb)//2
            self.y = self.ycb

            self.x0 = self.xcb
            self.y0 = self.y0b

            self.x1 = self.x1b
            self.y1 = self.y1b

            self.add_entity(entity[1], replacing = False)

            self.xc = self.xcb
            self.yc = self.yb
            self.x0 = self.x0b
            self.y0 = self.y0b
            self.x1 = self.x1b
            self.y1 = self.y1b
            return
        if replacing:
            if self.rendering_queue:
                self.rendering_queue[-1] = self.deduce_type(entity)
            else:
                self.rendering_queue.append(self.deduce_type(entity))
        else:
            self.rendering_queue.append(self.deduce_type(entity))

    def deduce_type(self, entity):
        if isinstance(entity, list):
            entity = entity[0]
        if os.path.isfile(entity):
            if entity.lower().endswith(IMG_FRMTS):

                image_converted = back.image.load(entity).convert()
                _h, _w = image_converted.get_height(), image_converted.get_width()

                scale_factor = 1.0
                if _h < _w:
                    scale_factor = (self.x1 - self.x0) / _w
                else:
                    scale_factor = (self.y1 - self.y0) / _h

                image_scaled = back.transform.scale(
                    image_converted, (int(_w * scale_factor), int(_h * scale_factor))
                )
                return ImageRenderer(image_scaled, self.xc, self.yc)

            elif magic.from_file(entity, mime=True) in TEXT_FORMTS:
                content = "".join(_ for _ in islice(open(entity, "r"), 0, 100))
                content = entity + " " + content
                return FileRenderer(content, self.xc, self.y0)
            else:
                return FilenameRenderer(entity, self.xc, self.yc)
        else:
            return FilenameRenderer(entity, self.xc, self.yc)
