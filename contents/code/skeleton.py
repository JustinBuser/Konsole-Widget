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

from PyQt4.QtGui import *
from PyKDE4.kdeui import *
from PyKDE4.kio import *

class Bones(KConfigSkeleton):
    def __init__(self):
        KConfigSkeleton.__init__(self)
        self.setCurrentGroup("settings")
        self.saveSize = self.addItemBool("saveSize", True, True)
        self.savePosition = self.addItemBool("savePosition", True, True)
        self.autoHide = self.addItemBool("autoHide", False, False)
        self.readConfig()
