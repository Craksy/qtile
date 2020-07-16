#!/usr/bin/env python3
from dataclasses import dataclass

@dataclass
class ColorTheme:
    #WIP
    background: str
    foreground: str

gruvbux = {
    'bg': '#282828',
    'fg': '#ebdbb2',
    'gray': '#928374',
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