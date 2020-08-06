#!/usr/bin/env python3
from dataclasses import dataclass



@dataclass
class Style:
    palette: dict
    background: str
    foreground: str
    primary: str
    secondary: str

    def __getitem__(self, item):
        if hasattr(self, item):
            return self.palette[getattr(self, item)]
        return self.palette[item]

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
