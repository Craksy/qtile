# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import glob
from typing import List  # noqa: F401
from itertools import chain
from libqtile import window, bar, layout, widget, extension, hook
from libqtile.config import Click, Drag, Group, Key, Screen, Match, ScratchPad, DropDown, KeyChord
from libqtile.lazy import lazy
from libqtile.log_utils import logger
# from libqtile.utils import guess_terminal
import subprocess
from subprocess import call
import os
import pynvim
import datetime
from bitstring import BitString
from pynput import keyboard
from whichkey import WhichKey

interface = None
current_chord = {}
mod = "mod4"
terminal = "konsole"
wkwidget = None

kboard = keyboard.Controller()

gruvbux = {
    'bg': '#282828',
    'red':      '#cc241d',
    'green':    '#98971a',
    'yellow':   '#d77921',
    'blue':     '#458588',
    'purple':   '#b16286',
    'aqua':     '#689d6a',
    'orange':   '#d65d0e',
    'red2':     '#fb4934',
    'green2':   '#b8bb26',
    'yellow2':  '#fabd2f',
    'blue2':    '#83a598',
    'purple2':  '#d3869b',
    'aqua2':    '#8ec07c',
    'orange2':  '#fe8019'
}


def smart_move(direction=None):
    def __inner__(qtile):
        cur_win = qtile.current_window
        cur_lay = qtile.current_layout
        dchars = {
            'left': 'h',
            'right': 'l',
            'up'   : 'k',
            'down' : 'j',
        }

        if "nvim" in cur_win.name:
            kboard.press(keyboard.Key.alt)
            kboard.press(dchars[direction])
            kboard.release(keyboard.Key.alt)
            kboard.release(dchars[direction])
        else:
            fname = "cmd_"+direction
            if hasattr(cur_lay, fname):
                mov_fun = getattr(cur_lay, fname)
                mov_fun()
    return __inner__




@hook.subscribe.startup
def init():
    startup_script_path = os.path.expanduser('~/.config/qtile/startup.sh')
    subprocess.call([startup_script_path])


resize_commands = [
    Key([], 'l', lazy.layout.grow_main(), desc='Grow main'),
    Key([], 'h', lazy.layout.shrink_main(), desc='Shrink main'),
    Key([], 'space', lazy.function(lambda q: ...)),
]

win_move_commands = [
    Key([], 'j', lazy.layout.shuffle_down(), desc='shuffle up'),
    Key([], 'k', lazy.layout.shuffle_up(), desc='shuffle down'),
]

w_commands = [
    Key([], 'q', lazy.window.kill(), desc='Kill'),
    Key([], 'space', lazy.window.toggle_fullscreen(), desc='Toggle fullscreen'),
    Key([], 'w', lazy.spawn('rofi -show window'), desc='$Rofi windows'),
    KeyChord([mod], 'r', resize_commands, mode='Resize'),
    KeyChord([], 'r', resize_commands, desc='Resize', mode='Resize'),
    KeyChord([mod], 'm', win_move_commands, mode='Win Move'),
    KeyChord([], 'm', win_move_commands, desc='Move', mode='Win Move'),
]

r_commands = [
    Key([], 'd', lazy.spawn('rofi -show drun'), desc='$Rofi drun'),
    Key([], 'e', lazy.spawn('emacs'), desc='Spawn Emacs'),
    Key([], 'r', lazy.spawn('konsole -e ranger'), desc='Spawn ranger'),
    Key([], 'v', lazy.spawn('konsole -e nvim'), desc='Spawn nvim'),
    Key([], 'w', lazy.spawn('konsole -e weechat'), desc='Spawn weechat'),
    Key([], 'q', lazy.spawn('qutebrowser'), desc='Spawn Qutebrowser'),

]

l_commands = [
    Key([], 'm', lazy.group.setlayout('monadtall'), desc='MonadTall'),
    Key([], 'w', lazy.group.setlayout('monadwide'), desc='MonadWide'),
    Key([], 'z', lazy.group.setlayout('max'), desc='Zoom (max)'),
    Key([], 's', lazy.group.setlayout('stack'), desc='Stack'),
]

g_commands = [
    Key([], 'd', lazy.group['Dev'].toscreen(), desc='Open Dev group'),
    Key([], 'h', lazy.group['Home'].toscreen(), desc='Open Home group'),
    Key([], 'w', lazy.group['Web'].toscreen(), desc='Open Web group'),
    Key([], 'p', lazy.group['Python'].toscreen(), desc='Open Python group'),
    Key([], 'i', lazy.group['IM'].toscreen(), desc='Open IM group'),
    Key([], 's', lazy.group['System'].toscreen(), desc='Open System group'),
]

chain_root = [
    KeyChord([mod], 'w', w_commands),
    KeyChord([], 'w', w_commands, desc='Windows'),
    KeyChord([mod], 'r', r_commands),
    KeyChord([], 'r', r_commands, desc='Run programs'),
    KeyChord([mod], 'm', l_commands),
    KeyChord([], 'm', l_commands, desc='Layouts'),
    KeyChord([mod], 'g', g_commands),
    KeyChord([], 'g', g_commands, desc='Groups'),
    Key([mod], 'Tab', lazy.layout.next()),
    Key([], 'Tab', lazy.layout.next(), desc='Next win'),

    Key([mod], "c", lazy.spawn('dmenu_configs')),
    Key([mod], "p", lazy.spawn('wallpaper-dmenu.sh')),
    Key([], "c", lazy.spawn('dmenu_configs'), desc='$Configs'),
    Key([], "p", lazy.spawn('wallpaper-dmenu.sh'), desc='$Wallpapers'),
    Key([], 'Return', lazy.spawn(terminal), desc='Launch terminal'),
    Key([mod], 'Return', lazy.spawn(terminal), desc='Launch terminal'),

    Key([], "j", lazy.function(smart_move('down')),
        desc="Move down"),
    Key([], "k", lazy.function(smart_move('up')),
        desc="Move up"),
    Key([], "h", lazy.function(smart_move("left")),
        desc="Move left"),
    Key([], "l", lazy.function(smart_move("right")),
        desc="Move right"),
    Key([mod], "j", lazy.function(smart_move('down')),
        desc="Move down"),
    Key([mod], "k", lazy.function(smart_move('up')),
        desc="Move up"),
    Key([mod], "h", lazy.function(smart_move("left")),
        desc="Move left"),
    Key([mod], "l", lazy.function(smart_move("right")),
        desc="Move right")
]

keys = [
    # Move windows up or down in current stack
    Key([mod, "control"], "j", lazy.layout.shuffle_down(),
        desc="Move window down in current stack"),
    Key([mod, "control"], "k", lazy.layout.shuffle_up(),
        desc="Move window up in current stack "),

    Key([mod, "shift"], "l", lazy.layout.grow_main()),
    Key([mod, "shift"], "h", lazy.layout.shrink_main()),

    # Switch window focus to other pane(s) of stack
    Key([mod], "Tab", lazy.layout.next(),
        desc="Switch window focus to other pane(s) of stack"),
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key([mod, "shift"], "Return", lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack"),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),

    Key([mod, "control"], "r", lazy.restart(), desc="Restart qtile"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown qtile"),

    KeyChord([], 'Super_L', chain_root),
    KeyChord([], 'Super_R', chain_root),
]

# dc = Match(title='Discord')

groups = [

    Group(name="Dev", label="✎ Dev", layout='max'),
    Group(name="Home", label=" Home", layout='monadtall'),
    Group(name="Web", label="爵 Web", layout='max'),
    Group(name="Python", label=" Python", layout="stack"),
    Group(name="IM", label=" IM"),
    Group(name="System", label=" Sys", layout='monadtall'),
    Group(name="Misc", label=" Misc")
]

group_keys = []
for i,g in enumerate(groups):
    group_keys.extend([
        # mod1 + letter of group = switch to group
        Key([], str(i+1), lazy.group[g.name].toscreen(),
            desc="go to {}".format(g.label)),

        # mod1 + shift + letter of group = switch to & move focused window to group
        Key([mod, "shift"], str(i+1), lazy.window.togroup(g.name, switch_group=True),
            desc="Switch to & move focused window to group {}".format(g.name)),
        Key([mod], str(i+1), lazy.group[g.name].toscreen(),
            desc="go to {}".format(g.label)),
        # Or, use below if you prefer not to switch to that group.
        # # mod1 + shift + letter of group = move focused window to group
        # Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
        #     desc="move focused window to group {}".format(i.name)),
    ])
chain_root[0:0] = group_keys

layouts = [
    layout.Max(),
    layout.Stack(border_width=2, num_stacks=2, border_focus=gruvbux['orange']),
    # Try more layouts by unleashing below layouts.
    # layout.Bsp(),
    # layout.Columns(),
    # layout.Matrix(),
    layout.MonadTall(border_width=2, margin=5, border_focus=gruvbux['orange']),
    layout.MonadWide(border_width=2, margin=10, border_focus=gruvbux['orange']),
    # layout.RatioTile(),
    # layout.Tile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]

widget_defaults = dict(
    font='FiraCode NF',
    fontsize=12,
    padding=3,
)
extension_defaults = widget_defaults.copy()


screens = [
    Screen(
        top=bar.Bar(
            [
                widget.GroupBox(font="FiraCode Nerd Font",
                                fontsize=17,
                                active=gruvbux['green'],
                                block_highlight_text_color='FFFFFF',
                                this_current_screen_border=gruvbux['green'],
                                highlight_method="block",
                                rounded=False),
                widget.Prompt(),
                # widget.Chord(),
                WhichKey(),
                # widget.Notify(),
                widget.Spacer(),
                # widget.TaskList(border=gruvbux['orange'], fontsize=16),
                # widget.MemoryGraph(border_color=gruvbux['purple'],
                # graph_color=gruvbux['purple'], fill_color='0eb070.0'),
                widget.CPUGraph(type='line'),
                widget.Clock(format='   %a %d-%m %H:%M   ',
                             foreground=gruvbux['green']),
                widget.Volume(emoji=False, mute_command=[
                            'amixer',
                            'q',
                            'set',
                            'Master',
                            'toggle']),
                widget.Systray(),
                # widget.Sep(),
                widget.QuickExit(default_text='  ⏻  ',
                                 foreground=gruvbux['red'],
                                 fontsize='15'),
            ],
            24, background="282828"
        ),
    ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]


dgroups_key_binder = None
dgroups_app_rules = []  # type: List
main = None
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(float_rules=[
    # Run the utility of `xprop` to see the wm class and name of an X client.
    {'wmclass': 'confirm'},
    {'wmclass': 'dialog'},
    {'wmclass': 'download'},
    {'wmclass': 'error'},
    {'wmclass': 'file_progress'},
    {'wmclass': 'notification'},
    {'wmclass': 'splash'},
    {'wmclass': 'toolbar'},
    {'wmclass': 'confirmreset'},  # gitk
    {'wmclass': 'makebranch'},  # gitk
    {'wmclass': 'maketag'},  # gitk
    {'wname': 'branchdialog'},  # gitk
    {'wname': 'pinentry'},  # GPG key password entry
    {'wmclass': 'ssh-askpass'},  # ssh-askpass
    {'wname': 'WhichKey Widget'},
    # {'wname': 'Execute D-Bus Method'},
])
auto_fullscreen = True
focus_on_window_activation = "smart"


@hook.subscribe.client_new
def client_new(client: window.Window):
    global wkwidget
    if client.name == "WhichKey Widget":
        wkwidget = client
        client.cmd_bring_to_front()
        client.static(0)
        client.update_state()
        client.update_hints()
        client.update_wm_net_icon()
        client.update_name()
        # client.place(300, 300, 200, 415, 0, 0, True)

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"


