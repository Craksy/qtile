#!/usr/bin/env python3
from dataclasses import dataclass



@dataclass
class Style:
    palette: dict
    background: str
    foreground: str
    primary: str
    secondary: str
    tetriary:str
    emacs_theme:str

    def __getitem__(self, item):
        if hasattr(self, item):
            return self.palette[getattr(self, item)]
        return self.palette[item]


monokai = dict(
    white='#DDDDDD',
    black='#272822',
    pink='#F92672',
    gray ='#93a1a1',
    cyan='#66D9EF',
    green='#A6E22E',
    orange='#FD971F',
    name2='#272822',
    name3='#F92672',
    name4='#66D9EF'
)

solarized = dict(
    base03 = '#002b36',
    black = '#073642',
    base01 = '#586e75',
    base00 = '#657b83',
    base0 = '#839496',
    gray = '#93a1a1',
    white = '#eee8d5',
    base3 = '#fdf6e3',
    yellow = '#b58900',
    orange = '#cb4b16',
    red = '#dc322f',
    magenta = '#d33682',
    violet = '#6c71c4',
    blue = '#268bd2',
    cyan = '#2aa198',
    green = '#859900'
)


dracula = dict(
    black ='#282a36',
    white ='#f8f8f2',
    gray = '#44475a',
    red = '#FF5555',
    green = '#50fa7b',
    yellow='#f1fa8c',
    blue = '#6272a4',
    purple = '#bd93f9',
    pink = '#ff79c6',
    cyan = '#8be9fd',
    orange = '#ffb86c'
)

gruvbox = dict(
    black = '#282828',
    white = '#ebdbb2',
    gray = '#928374',
    red =      '#cc241d',
    green =    '#98971a',
    yellow =   '#d77921',
    blue =     '#458588',
    purple =   '#b16286',
    aqua =     '#689d6a',
    orange =   '#d65d0e',
    red2 =     '#fb4934',
    green2 =   '#b8bb26',
    yellow2 =  '#fabd2f',
    blue2 =    '#83a598',
    purple2 =  '#d3869b',
    aqua2 =    '#8ec07c',
    orange2 =  '#fe8019'
)
