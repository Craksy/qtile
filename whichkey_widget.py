import sys
from pprint import pprint
from PySide2.QtCore import *
from PySide2.QtWidgets import (
    QApplication,
    QLabel,
    QMainWindow,
    QWidget,
    QPushButton,
    QBoxLayout,
    QVBoxLayout,
    QHBoxLayout,
    QSpacerItem,
    QFrame,
)

import dbus
import dbus.service
import dbus.mainloop.glib

from libqtile.config import Key, KeyChord

class DBusWindow(dbus.service.Object):
    def __init__(self, name, session):
        dbus.service.Object.__init__(self, name, session)
        self.win = MainWindow()

    @dbus.service.method("com.mytest.WhichKey",in_signature='', out_signature='')
    def Close(self):
        sys.exit()

    @dbus.service.method("com.mytest.WhichKey",in_signature='', out_signature='')
    def Show(self):
        self.win.show()

    @dbus.service.method("com.mytest.WhichKey",in_signature='', out_signature='')
    def Hide(self):
        self.win.hide()

    @dbus.service.method("com.mytest.WhichKey",in_signature='', out_signature='')
    def ToggleVisible(self):
        self.win.setVisible(not self.win.isVisible())

    @dbus.service.method("com.mytest.WhichKey",in_signature='a{ss}', out_signature='')
    def SetContent(self, content):
        self.win.set_content(content)

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_window()

    
    def init_window(self):
        self.setWindowTitle('WhichKey Widget')
        self.setWindowRole('Widget')
        flags = Qt.WindowFlags(
            #PySide2.QtCore.Qt.FramelessWindowHint
            # | PySide2.QtCore.Qt.WindowStaysOnTopHint
            Qt.CustomizeWindowHint
            # | PySide2.QtCore.Qt.X11BypassWindowManagerHint
        )
        self.setWindowFlags(flags)

        self.setStyleSheet('QWidget {background-color: #282828}\
                           QPushButton {background-color: #98971a}\
                           QLabel {color: #98971a}\
                           QFrame.VLine {color: #FF0000}')


        self.main_hbox = QHBoxLayout()
        self.layout = self.main_hbox
        self.layout.setSpacing(10)
        self.setLayout(self.layout)
        self.current_vbox = None
        self.current_row = 0
        self.num_columns = 0
        self.new_column()
        self.set_geometry()

    def set_geometry(self):
        screen_size = self.screen().geometry().size()
        ww, wh = screen_size.toTuple()
        margin = 5
        bar = 22
        pw = self.num_columns*200
        ph = 50*self.current_row +50 if self.num_columns == 1 else 400

        self.x = ww - (pw+margin)
        self.y = bar + margin
        self.width, self.height = pw, ph

        self.setMaximumWidth(pw)
        self.setGeometry(self.x, self.y, self.width, self.height)
        self.updateGeometry()
        self.move(self.x, self.y)


    def add_label(self, key, desc):
        hbox = QHBoxLayout()
        lbl1 = QLabel(key)

        lbl2 = QLabel('')
        if desc.startswith('@'):
            desc = '﬌ '+desc[1:]
            lbl2.setStyleSheet('QLabel {color: #d65d0e}')
        elif desc.startswith('$'):
            desc = ' '+desc[1:]
            lbl2.setStyleSheet('QLabel {color: #458588}')
        else:
            lbl2.setStyleSheet('QLabel {color: #ebdbb2}')
        f = lbl2.font()
        f.setBold(True)
        lbl2.setFont(f)
        lbl2.setText(desc)
        lbl1.setFixedWidth(50)
        lbl1.updateGeometry()
        hbox.addWidget(lbl1, alignment=Qt.AlignLeft, stretch=0)
        hbox.addWidget(lbl2, alignment=Qt.AlignLeft, stretch=1)
        self.current_vbox.addLayout(hbox)
        self.current_row += 1
                

    def clear_content(self, layout):
        for i in reversed(range(layout.count())):
            item = layout.takeAt(i)
            l = item.layout()
            if l is not None:
                self.clear_content(l)
                l.setParent(None)
            else:
                w = item.widget()
                w.setParent(None)
        self.num_columns = 0
        self.new_column()


    def set_content(self, content:dict):
        self.clear_content(self.layout)

        for key, desc in content.items():
            if self.current_row >= 7:
                self.new_column()
            self.add_label(key,desc)
        self.set_geometry()

    def new_column(self):
        if self.num_columns > 0:
            sep = QFrame()
            sep.setFrameShape(QFrame.VLine)
            sep.setLineWidth(2)
            sep.setStyleSheet('color: #ebdbb2')
            self.layout.addWidget(sep)

        nc = QVBoxLayout()
        self.layout.addLayout(nc)
        self.current_vbox = nc
        self.current_row = 0
        self.num_columns +=1



app = QApplication([])
dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
sbus = dbus.SessionBus()
name = dbus.service.BusName("com.mytest.WhichKeyService", sbus)
win = DBusWindow(name, '/DBusWindow')

app.exec_()
