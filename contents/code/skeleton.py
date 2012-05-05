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

from PyQt4.QtCore import QRect
#from PyQt4.QtGui import *
from PyKDE4.kdecore import *
from PyKDE4.kdeui import *
#from PyKDE4.kio import *

class Bones(KConfigSkeleton):
    saveSize = bool(True)
    savePosition = bool(True)
    autoHide = bool(False)
    
    def __init__(configname,parent=0):
        KConfigSkeleton.__init__(KGlobal.config(),parent)
        setCurrentGroup("CoreConfig")
        
        addItemBool("saveSize", saveSize, True)
        addItemBool("savePosition", savePosition, True)
        addItemBool("autoHide", autoHide, False)
        addItemRect("storedGeometry",storedGeometry,QRect(0,0,600,400))
