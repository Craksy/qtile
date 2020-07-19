import math
from time import sleep
from libqtile.log_utils import logger
from libqtile.widget.base import ThreadPoolText, _TextBox, _Widget
from libqtile import hook, window, bar, drawer, configurable
from libqtile.config import Screen, KeyChord, Key
from boxlayout import VBoxLayout, HBoxLayout
from color_themes import gruvbux

class VSep:
    def __init__(self, drawer, color, height, thickness):
        self.height = height
        self.thickness = thickness
        self.width = thickness
        self.drawer = drawer
        self.color = color

    def draw(self, offsetx, offsety):
        self.drawer.draw_vbar(self.color,
                              offsetx,
                              offsety, offsety+self.height,
                              self.thickness)

class WhichKey(_Widget):
    def __init__(self):
        super().__init__(1)
        self.winwidth = 200
        self.winheight = 200
        self.winx = 0
        self.winy = 0
        self.length = 0
        self.margin = 5
        self.layout = None

    def calculate_length(self):
        return 1

    def draw(self):
        self.drawer.clear(gruvbux['bg'])
        self.layout.draw(0,0)
        self.drawer.draw()

    def _configure(self, qtile, bar):
        logger.debug('%s\n%s\n%s', str(qtile), str(bar), 'lol')
        _Widget._configure(self, qtile, bar)
        self.winx = self.bar.screen.width - self.winwidth - self.margin
        self.winy = self.bar.height+self.margin
        self.add_defaults(bar.defaults)
        self.qtile = qtile
        self.bar = bar
        self.setup_hooks()
        self.window = window.Internal.create(qtile,
                                             self.winx,
                                             self.winy,
                                             self.winwidth,
                                             self.winheight)

        self.drawer = drawer.Drawer(self.qtile,
                                    self.window.window.wid,
                                    800, 400)

        self.drawer.clear(self.background)
        self.layout = HBoxLayout(self.drawer, 0,0,15, 10)

        self.window.handle_Expose = self.handle_Expose
        self.window.handle_ButtonPress = self.handle_ButtonPress
        self.window.handle_ButtonRelease = self.handle_ButtonRelease
        qtile.windows_map[self.window.window.wid] = self.window


    def handle_Expose(self, arg):
        self.draw()
    def handle_ButtonPress(self): ...
    def handle_ButtonRelease(self): ...

    def create_collumns(self, chord:KeyChord):
        self.layout.clear()
        mappings = [k for k in chord.submapings \
                    if not (k.modifiers or k.key=='Escape')]
        cur_row = 0
        min_width = 0
        nrows = 7
        columns = [mappings[x:x+nrows] for x in range(0, len(mappings), nrows)]
        for i,c in enumerate(columns):
            cur_column = VBoxLayout(self.drawer, 0,0,20)
            self.layout.add_child(cur_column)
            hw = 0
            for m in c:
                key_label = self.drawer.textlayout(m.key,
                                                   gruvbux['green'],
                                                   'sans', 12,
                                                   None, True)
                if isinstance(m, KeyChord):
                    dcolor = gruvbux['orange']
                    dtext = '﬌ ' + m.desc
                elif m.desc.startswith('$'):
                    dcolor = gruvbux['blue']
                    dtext = ' ' + m.desc[1:]
                else:
                    dcolor = gruvbux['fg']
                    dtext = '⇒ ' + m.desc

                desc_label = self.drawer.textlayout(dtext,
                                                    dcolor,
                                                    'sans', 12,
                                                    None, True)
                if key_label.width > hw:
                    hw = key_label.width
                row = HBoxLayout(self.drawer, 0, 0, 10)
                row.add_child(key_label)
                row.add_child(desc_label)
                cur_column.add_child(row)
            for r in cur_column.children:
                r.min_width = hw
            if i < len(columns)-1:
                self.layout.add_child(VSep(self.drawer,
                                        gruvbux['gray'],
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
            logger.debug('enter chord from whichkey')
            self.window.unhide()

        @hook.subscribe.leave_chord
        def on_leave_chord(mode:str, chord=None):
            self.window.hide()
