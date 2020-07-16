#!/usr/bin/env python3


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
