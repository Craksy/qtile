#!/usr/bin/env python3
from libqtile.log_utils import logger
class LayoutComponent:
    def __init__(self):
        self.drawer = None
        self.x = 0
        self.y = 0
        self._width = 0
        self._height = 0

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    def _configure(self, qtile, bar, window, drawer):
        self.qtile = qtile
        self.bar = bar
        self.window = window
        self.drawer = drawer

    def draw(self):
        raise NotImplementedError


class Container(LayoutComponent):
    def __init__(self, spacing = 0, margin = 0, padding = 0):
        super().__init__()
        self.children = []
        self.spacing = spacing
        self.margin = margin
        self.padding = padding

    def _configure(self, qtile, bar, window, drawer):
        super()._configure(qtile, bar, window, drawer)
        for c in self.children:
            if hasattr(c, '_configure'):
                c._configure(qtile, bar, window, drawer)

    def __len__(self):
        return len(self.children)

    def add_child(self, item):
        self.children.append(item)
        if isinstance(item, Container):
            item._configure(self.qtile, self.bar, self.window, self.drawer)

    def finalize(self):
        for c in self.children:
            if hasattr(c, 'finalize'):
                c.finalize()

    def clear(self):
        for c in self.children:
            if isinstance(c, Container):
                c.clear()
                del c
            else:
                del c
        self.children = []


class HBLayout(Container):
    def __init__(self, spacing, margin, padding):
        super().__init__(spacing, margin, padding)
        self.spacing = spacing
        self.margin = margin
        self.padding = padding
        self.min_width = 0

    @property
    def width(self):
        self._width = sum(c.width if c.width>self.min_width else self.min_width for c in self.children) + \
            (len(self.children)-1)*self.spacing + 2*self.margin
        return self._width

    @property
    def height(self):
        if not self.children:
            return 0
        self._height = max(c.height for c in self.children)+2*self.margin
        return self._height

    def draw(self, offsetx, offsety):
        offsetx += self.margin
        offsety += self.margin
        for c in self.children:
            c.draw(self.x + offsetx, self.y + offsety)
            delta_offset = c.width
            if delta_offset < self.min_width:
                delta_offset = self.min_width
            delta_offset += self.spacing
            offsetx+=delta_offset

class VBLayout(Container):
    def __init__(self, spacing, margin, padding):
        super().__init__(spacing, margin, padding)
        self.spacing = spacing
        self.margin = margin
        self.padding = padding
        self.min_height = 0

    @property
    def height(self):
        self._height = sum(c.height if c.height>self.min_height else self.min_height for c in self.children) + \
            (len(self.children)-1)*self.spacing + 2*self.margin
        return self._height

    @property
    def width(self):
        if not self.children:
            return 0
        self._width = max(c.width for c in self.children)+2*self.margin
        return self._width

    def draw(self, offsetx, offsety):
        offsetx += self.margin
        offsety += self.margin
        logger.debug('drawing vblayout at %d,%d', offsetx, offsety)
        for c in self.children:
            c.draw(self.x + offsetx, self.y + offsety)
            delta_offset = c.height
            if delta_offset < self.min_height:
                delta_offset = self.min_height
            delta_offset += self.spacing
            offsety+=delta_offset







# DEPRECATED:
# these are the old classes for the whichkey widget.
# i keep them for a while just in case.
class Spacer:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def draw(self):
        pass

class BoxLayout:
    def __init__(self, drawer,
                 xpos = 0, ypos = 0,
                 spacing = 0, margin= 0):
        self.drawer = drawer
        self.x = xpos
        self.y = ypos
        self._width = 0
        self._height = 0
        self.children = []
        self.spacing = spacing
        self.margin = margin

    def __len__(self):
        return len(self.children)

    def add_child(self, item):
        self.children.append(item)

    def clear(self):
        for c in self.children:
            if isinstance(c, BoxLayout):
                c.clear()
                del c
            else:
                del c
                self.children = []

class HBoxLayout(BoxLayout):
    def __init__(self, drawer, xpos=0, ypos=0, spacing=None, margin=0):
        super().__init__(drawer,xpos,ypos,spacing,margin)
        self.min_width = 0

    @property
    def width(self):
        self._width = sum(c.width if c.width>self.min_width else self.min_width for c in self.children) + \
            (len(self.children)-1)*self.spacing + 2*self.margin

        return self._width


    @property
    def height(self):
        if not self.children:
            return 0
        self._height = max(c.height for c in self.children)+2*self.margin
        return self._height


    def draw(self, offsetx, offsety):
        offsetx += self.margin
        offsety += self.margin
        for c in self.children:
            c.draw(self.x + offsetx, self.y + offsety)
            delta_offset = c.width
            if delta_offset < self.min_width:
                delta_offset = self.min_width
                delta_offset += self.spacing
                offsetx+=delta_offset

class VBoxLayout(BoxLayout):
    def __init__(self, drawer, xpos=0, ypos=0, spacing=None, margin=0):
        super().__init__(drawer,xpos,ypos,spacing,margin)

    @property
    def width(self):
        if not self.children:
            return 0
        self._width = max(self.children, key=lambda k: k.width).width
        return self._width

    @property
    def height(self):
        self._height = sum(c.height for c in self.children) +\
            (len(self.children)-1)*self.spacing
        return self._height

    def draw(self, offsetx, offsety):
        for c in self.children:
            c.draw(self.x + offsetx, self.y + offsety)
            offsety += c.height+self.spacing
