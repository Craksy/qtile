#!/usr/bin/env python3
from libqtile.log_utils import logger
from libqtile.widget.base import _Widget
from libqtile.config import Key, KeyChord
from libqtile import window, drawer, hook
from color_themes import gruvbox, Style
from whichkey import VSep
import boxlayout
from boxlayout import HBLayout, VBLayout

def clamp(value, minimum, maximum):
    return min((max(value, minimum), maximum))

class DesktopWidget(_Widget):
    def __init__(self):
        super().__init__(1)
        self.winwidth = 200
        self.winheight = 200
        self.winx = 0
        self.winy = 0
        self.length = 0
        self.margin = 5
        self.layout = HBLayout(0,0,0)
        self.style = None

    def calculate_length(self):
        return 1

    def draw(self):
        self.drawer.clear(self.style['background'])
        self.layout.draw(0,0)
        self.drawer.draw()

    def _configure(self, qtile, bar):
        _Widget._configure(self, qtile, bar)
        self.winx = self.bar.screen.width - self.winwidth - self.margin
        self.winy = self.bar.height+self.margin
        self.add_defaults(bar.defaults)
        self.qtile = qtile
        self.bar = bar
        self.window = window.Internal.create(qtile,
                                             self.winx,
                                             self.winy,
                                             self.winwidth,
                                             self.winheight)

        self.drawer = drawer.Drawer(self.qtile,
                                    self.window.window.wid,
                                    800, 400)

        self.drawer.clear(self.background) #is this actually used?
        self.layout._configure(qtile, bar, self.window, self.drawer)

        self.window.handle_Expose = self.handle_Expose
        self.window.handle_ButtonPress = self.handle_ButtonPress
        self.window.handle_ButtonRelease = self.handle_ButtonRelease
        qtile.windows_map[self.window.window.wid] = self.window


    def handle_Expose(self, arg):
        self.draw()
    def handle_ButtonPress(self): ...
    def handle_ButtonRelease(self): ...

class WkWidget(DesktopWidget):
    def __init__(self, style):
       DesktopWidget.__init__(self)
       self.layout = HBLayout(15, 10, 0)
       self.style = style

    def _configure(self, qtile, bar):
        DesktopWidget._configure(self, qtile, bar)
        self.margin = 5
        self.setup_hooks()

    def create_collumns(self, chord:KeyChord):
        self.layout.clear()
        mappings = [k for k in chord.submapings if k.desc != '']
        cur_row = 0
        min_width = 0
        nrows = 7
        columns = [mappings[x:x+nrows] for x in range(0, len(mappings), nrows)]
        for i,c in enumerate(columns):
            cur_column = VBLayout(10,0,20)
            self.layout.add_child(cur_column)
            hw = 0
            for m in c:
                label_text = m.key
                if 'shift' in m.modifiers:
                    label_text = label_text.upper()
                if 'ctrl' in m.modifiers:
                    label_text = '^'+label_text
                key_label = self.drawer.textlayout(label_text,
                                                   self.style['primary'],
                                                   'sans', 12,
                                                   None, True)
                if isinstance(m, KeyChord):
                    dcolor = self.style['secondary']
                    dtext = '﬌ ' + m.desc
                elif m.desc.startswith('$'):
                    dcolor = self.style['tetriary']
                    dtext = ' ' + m.desc[1:]
                else:
                    dcolor = self.style['foreground']
                    dtext = '⇒ ' + m.desc

                desc_label = self.drawer.textlayout(dtext,
                                                    dcolor,
                                                    'sans', 12,
                                                    None, True)
                if key_label.width > hw:
                    hw = key_label.width
                row = HBLayout(10, 0, 10)
                row.add_child(key_label)
                row.add_child(desc_label)
                cur_column.add_child(row)
            for r in cur_column.children:
                r.min_width = hw
            if i < len(columns)-1:
                self.layout.add_child(VSep(self.drawer,
                                        self.style['gray'],
                                        cur_column.height, 2))

        self.winwidth = self.layout.width
        self.winheight = self.layout.height
        self.winx = self.bar.screen.width - self.winwidth - self.margin

    def setup_hooks(self):
        @hook.subscribe.enter_chord
        def on_enter_chord(mode:str, chord=None):
            if chord is not None:
                self.create_collumns(chord)
            self.window.place(self.winx, self.winy,
                              self.winwidth, self.winheight,
                              0, 0xFF0000, above=True)
            self.draw()
            self.window.unhide()

        @hook.subscribe.leave_chord
        def on_leave_chord(mode:str, chord=None):
            self.window.hide()
