# This is a test
from libqtile import window, bar, layout, widget, extension, hook
from libqtile.config import (
    Click,
    Drag,
    Group,
    Key,
    Screen,
    Match,
    ScratchPad,
    DropDown,
    KeyChord)
from libqtile.lazy import lazy
from libqtile.log_utils import logger
from libqtile.utils import guess_terminal

from typing import List
import subprocess
from subprocess import call
import os
import pynvim
import datetime
from bitstring import BitString
from pynput import keyboard
from itertools import chain
from color_themes import gruvbux
from desktop_widget import WkWidget

dgroups_key_binder = None
dgroups_app_rules = []  # type: List
main = None
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
auto_fullscreen = True
focus_on_window_activation = "smart"
wmname = "LG3D"

interface = None
current_chord = {}
mod = "mod4"
terminal = "konsole"
wkwidget = None
kboard = keyboard.Controller()

widget_defaults = dict(
    font='FiraCode NF',
    fontsize=12,
    padding=3,
)
extension_defaults = widget_defaults.copy()

group_table=[["Dev", "✎", "max"], ["Home", "", "monadtall"], ["Web", "爵", "max"], ["Python", "", "stack"], ["IM", "", "max"], ["Sys", "", "monadtall"], ["Misc", "", "monadtall"]]
groups = [
    Group(name=n, label = f'{ic} {n}', layout=la) for n, ic, la in group_table
]

resize_commands = [
    Key([], 'l', lazy.layout.grow_main(), desc='Grow main'),
    Key([], 'h', lazy.layout.shrink_main(), desc='Shrink main'),
    Key([], 'space', lazy.function(lambda q: ...)),
]

win_move_commands = [
    Key([], 'j', lazy.layout.shuffle_down(), desc='shuffle up'),
    Key([], 'k', lazy.layout.shuffle_up(), desc='shuffle down'),
]

to_group_commands = [
    Key([], '1', lazy.window.togroup('Dev', switch_group=True)),
    Key([], '2', lazy.window.togroup('Home', switch_group=True)),
    Key([], '3', lazy.window.togroup('Web', switch_group=True)),
    Key([], '4', lazy.window.togroup('Python', switch_group=True)),
    Key([], '5', lazy.window.togroup('IM', switch_group=True)),
    Key([], '6', lazy.window.togroup('Sys', switch_group=True)),
    Key([], '7', lazy.window.togroup('Misc', switch_group=True)),
    Key([], 'd', lazy.window.togroup('Dev', switch_group=True)),
    Key([], 'h', lazy.window.togroup('Home', switch_group=True)),
    Key([], 'w', lazy.window.togroup('Web', switch_group=True)),
    Key([], 'p', lazy.window.togroup('Python', switch_group=True)),
    Key([], 'i', lazy.window.togroup('IM', switch_group=True)),
    Key([], 's', lazy.window.togroup('Sys', switch_group=True)),
    Key([], 'm', lazy.window.togroup('Misc', switch_group=True)),
]

w_commands = [
    Key([], 'q', lazy.window.kill(), desc='Kill'),
    Key([], 'space', lazy.window.toggle_fullscreen(), desc='Toggle fullscreen'),
    Key([], 'w', lazy.spawn('rofi -show window'), desc='$Rofi windows'),
    KeyChord([mod], 'r', resize_commands, mode='Resize'),
    KeyChord([], 'r', resize_commands, desc='Resize', mode='Resize'),
    KeyChord([mod], 'm', win_move_commands, mode='Win Move'),
    KeyChord([], 'm', win_move_commands, desc='Move', mode='Win Move'),
    KeyChord([mod], 's', to_group_commands),
    KeyChord([], 's', to_group_commands, desc='Send to Group'),
]

r_commands = [
    Key([], 'd', lazy.spawn('rofi -show drun'), desc='$Rofi drun'),
    Key([], 'e', lazy.spawn('emacs'), desc='Emacs'),
    Key([], 'r', lazy.spawn('konsole -e ranger'), desc='Ranger'),
    Key([], 'v', lazy.spawn('konsole -e nvim'), desc='Nvim'),
    Key([], 'w', lazy.spawn('konsole -e weechat'), desc='Weechat'),
    Key([], 'q', lazy.spawn('qutebrowser'), desc='Qutebrowser'),
]

l_commands = [
    Key([], 'm',   lazy.group.setlayout('monadtall'), desc='MonadTall'),
    Key([], 'w',   lazy.group.setlayout('monadwide'), desc='MonadWide'),
    Key([], 'z',   lazy.group.setlayout('max'), desc='Zoom (max)'),
    Key([], 's',   lazy.group.setlayout('stack'), desc='Stack'),
    Key([], 'Tab', lazy.next_layout(), desc='Next layout'),
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

    Key([], "j", lazy.layout.down(),
        desc="Move down"),
    Key([], "k", lazy.layout.up(),
        desc="Move up"),
    Key([], "h", lazy.layout.left(),
        desc="Move left"),
    Key([], "l", lazy.layout.right(),
        desc="Move right"),
    Key([mod], "j", lazy.layout.down(),
        desc="Move down"),
    Key([mod], "k", lazy.layout.up(),
        desc="Move up"),
    Key([mod], "h", lazy.layout.left(),
        desc="Move left"),
    Key([mod], "l", lazy.layout.right(),
        desc="Move right"),
    Key(['control'], 'r', lazy.restart()),
    Key([mod], 'colon', lazy.qtilecmd(), desc='Qtile Cmd'),
    Key([], 'colon', lazy.qtilecmd(), desc='Qtile Cmd'),
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

keys = [
    KeyChord([], 'Super_L', chain_root),
    KeyChord([], 'Super_R', chain_root),
]

mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]

layouts = [
    layout.Max(),
    layout.Stack(border_width=2, num_stacks=2, border_focus=gruvbux['blue']),
    # Try more layouts by unleashing below layouts.
    layout.Bsp(),
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
                WkWidget(),
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
                widget.TextBox('', fontsize=22),
                widget.KeyboardLayout(configured_keyboards=['us_custom', 'dk', 'us'], display_map={'us': 'US', 'us_custom': 'code', 'dk': 'DK'}),
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

@hook.subscribe.client_new
def client_new(client: window.Window):
    global wkwidget
    if client.name == 'qutebrowser':
        client.togroup('Web')

@hook.subscribe.startup
def init():
    startup_script_path = os.path.expanduser('~/.config/qtile/startup.sh')
    subprocess.call([startup_script_path])
