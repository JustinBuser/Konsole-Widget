#   Copyright (C) 2011 Justin Buser <development@justinbuser.com>
#
#   This program is free software; you can redistribute it and/or modify
#   it under the terms of the GNU General Public License version 2,
#   or (at your option) any later version, as published by the Free
#   Software Foundation
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details
#
#   You should have received a copy of the GNU General Public
#   License along with this program; if not, write to the
#   Free Software Foundation, Inc.,
#   51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
#
import os

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyKDE4.kdecore import *
from PyKDE4.kdeui import *
from PyKDE4.kio import *

class MainOptions(QWidget):

    savesize = True
    saveposition = True
    autohide = True

    def __init__(self, savesize, saveposition, autohide, parent=None):

        super(MainOptions, self).__init__(parent)

        QWidget.__init__(self)
        self.savesize = savesize

        self.saveposition = saveposition
        self.autohide = autohide

        self.verticalLayout = QVBoxLayout(self)
        self.widget = QWidget(self)
        self.formLayout = QFormLayout(self.widget)
        self.saveSize = QCheckBox(self.widget)
        self.savePosition = QCheckBox(self.widget)
        self.autoHide = QCheckBox(self.widget)

        if savesize:
            self.saveSize.setCheckState(Qt.Checked)
        if saveposition:
            self.savePosition.setCheckState(Qt.Checked)
        if autohide:
            self.autoHide.setCheckState(Qt.Checked)

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.saveSize)
        self.formLayout.setWidget(2, QFormLayout.FieldRole,
                                  self.savePosition)
        self.formLayout.setWidget(3, QFormLayout.FieldRole, self.autoHide)
        self.verticalLayout.addWidget(self.widget)

        self.savesize.stateChanged[int].connect(self.checkboxStateChanged)
        self.savePosition.stateChanged[int].connect(
            self.checkboxStateChanged)
        self.autoHide.stateChanged[int].connect(
            self.checkboxStateChanged)

        self.retranslateUi()

    @pyqtSignature("int")
    def checkboxStateChanged(self, i):

        self.savesize = True if self.saveSize.checkState() else False
        self.saveposition = True if self.savePosition.checkState() else False
        self.autohide = True if self.autoHide.checkState() else False

    def retranslateUi(self):
        self.saveSize.setText(ki18n("Save size of Dashboard Plasmoid"
                                     " when resized (Uncheck after resizing "
                                      "to always use that size)").toString())
        self.savePosition.setText(ki18n("Save position of Dashboard Plasmoid"
                                         " when moved (Uncheck after moving"
                                         " to always use those coordinates)"
                                         ).toString())
        self.autoHide.setText(ki18n("Keep the popup Konsole open until its"
                                     " icon is clicked again, even if it"
                                     "loses focus").toString())
