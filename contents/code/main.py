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
from PyKDE4.plasma import Plasma
from PyKDE4 import plasmascript
from PyKDE4.kparts import KParts
from configuration import MainOptions

class KonsoleMainPart(QGraphicsWidget):
    
    def __init__(self,parent,args=None):
        QGraphicsWidget.__init__(self)
        self.applet = parent.applet
        self.setMinimumSize(parent.sizeMin)
        self.parent = parent
        
    def init(self,x,y,width,height):
        self.applet.setGeometry(x,y,width,height)
        self.factory = KPluginLoader("libkonsolepart").factory()
        self.layout = QGraphicsLinearLayout(Qt.Vertical, self)
        self.createKonsole()
    
    def createKonsole(self):
        self.konsole = self.factory.create()
        if self.konsole:
            self.setAutoFillBackground(False)
            self.centralWidget = QGraphicsProxyWidget(self)
            self.konsole.openUrl(KUrl.fromPath(os.environ['HOME']))
            self.consoleWidget = self.konsole.widget()
            self.consoleWidget.setAutoFillBackground(False)
            self.centralWidget.setWidget(self.consoleWidget)
            self.consoleWidget.setFocus()
            self.layout.addItem(self.centralWidget)
            self.layout.setAlignment(self.centralWidget, Qt.AlignLeft)
            self.connect(self.konsole,SIGNAL("destroyed()"),self.createKonsole)
            self.parent.setGraphicsWidget(self)
            self.parent.addAssociatedWidget(self.consoleWidget)
            self.consoleWidget.setFocus()
            actionCollection = self.actions
            #self.pasteAction = actionCollection.addAction(KStandardAction.Paste,self,SLOT(edit_paste()))
            #self.pasteAction.setShortcut(Qt.CTRL + Qt.SHIFT + Qt.Key_P)
            #self.connect(self.pasteAction, SIGNAL("triggered"), self, SLOT(edit_paste()))
            #pasteAction = KAction(  KIcon("stock_paste"), i18n("&Paste"), self.parent )
            #KStandardShortcut.shortcut(KStandardShortcut.Paste), self.consoleWidget, SLOT(edit_paste()), KActionCollection.allCollections() ) 
            pasteAction = KStandardAction.paste(self) 
            pasteShortcut = pasteAction.shortcut()
            pasteShortcut.setAlternate(Qt.CTRL + Qt.SHIFT + Qt.Key_V)

class KonsoleWidget(plasmascript.Applet):

    def __init__(self, parent, args=None):
        plasmascript.Applet.__init__(self, parent)
        self.setApplet(Plasma.Applet(parent, []))
        self.parent = parent
        self.sizeMin = QSizeF(200, 100)
    
    def debugHandler(self, type, msg):
        if str(msg).find("plasma-desktop") < 0:
            print str(type)+" "+str(msg)
    
    def saveGeometry(self):
        changed = False
        width = self.applet.geometry().width()
        height = self.applet.geometry().height()
        fc = self.extConfig.group("settings")
        if width >= self.sizeMin.width() and height >= self.sizeMin.height() and self.savesize:
            fc.writeEntry("width", QVariant(int(width)))
            fc.writeEntry("height", QVariant(int(height)))
            changed = True
        if self.saveposition:
            fc.writeEntry("x", QVariant(int(self.applet.geometry().x())))
            fc.writeEntry("y", QVariant(int(self.applet.geometry().y())))
            changed = True
        if changed:
            self.extConfig.sync()
    
    def init(self):
        qInstallMsgHandler(self.debugHandler)
        qDebug("Test")
        
        self.setHasConfigurationInterface(True)
        self.extConfig = KConfig(KStandardDirs.locateLocal("config", "konsolewidget_rc"))
        fc = self.extConfig.group("settings")
        width = 640
        height = 400
        self.savesize = True
        self.saveposition = True
        self.autohide = True
        try:
            height = int(fc.readEntry("height"))
        except ValueError, e:
            fc.writeEntry("width", QVariant(width))
        try: 
            width = int(fc.readEntry("width"))
        except ValueError, e:
            fc.writeEntry("height", QVariant(height))
        try:
            self.savesize = fc.readEntry("savesize")=="true"
        except ValueError, e:
            fc.writeEntry("savesize", QVariant(self.savesize))
        try:
            self.autohide = fc.readEntry("autohide")=="true"
        except ValueError, e:
            fc.writeEntry("autohide", QVariant(self.autohide))
        try:
            self.saveposition = fc.readEntry("saveposition")=="true"
        except ValueError, e:
            fc.writeEntry("saveposition", QVariant(self.saveposition))
        try:
            x=int(fc.readEntry("x"))
            y=int(fc.readEntry("y"))
            self.applet.setGeometry(x,y,width,height)
        except ValueError, e:
            x=0
            y=0
        
        self.setAspectRatioMode(Plasma.IgnoreAspectRatio)
        self.setBackgroundHints(Plasma.Applet.DefaultBackground)
        self.setOpacity(.98)
        self.setPassivePopup(self.autohide)
        self.widget=KonsoleMainPart(self)
        self.widget.init(x,y,width,height)
        self.applet.setPopupIcon(KIcon("utilities-terminal"))
        self.setGraphicsWidget(self.widget)    
        self.extConfig.sync()
        self.connect(self.applet, SIGNAL("geometryChanged()"), self.saveGeometry)
        #self.addAssociatedWidget(self.widget)
        
    def configAccepted(self):
        self.savesize = self.mainOptions.savesize
        self.saveposition = self.mainOptions.saveposition
        self.autohide = self.mainOptions.autohide
        self.setPassivePopup(self.mainOptions.autohide)
        fc = self.extConfig.group("settings")
        fc.writeEntry("savesize", QVariant(self.savesize))
        fc.writeEntry("saveposition", QVariant(self.savesize))
        fc.writeEntry("autohide", QVariant(self.autohide))
        self.extConfig.sync()
    
    def createConfigurationInterface(self, parent):
        self.mainOptions = MainOptions(self.savesize,self.saveposition,self.autohide)
        p = parent.addPage(self.mainOptions, ki18n("Misc Options").toString())
        p.setIcon( KIcon("utilities-terminal") )
        #parent.addPage(General(0, "General"), i18n("General"))
        self.connect(parent, SIGNAL("okClicked()"), self.configAccepted)
        self.connect(parent, SIGNAL("cancelClicked()"), self.mainOptions.deleteLater)

    def showConfigurationInterface(self):
        dialog = KConfigDialog(self.parent, "Konsole Widget Settings",)
        dialog.setFaceType(KPageDialog.List)
        dialog.setButtons(KDialog.ButtonCode(KDialog.Ok | KDialog.Cancel))
        self.createConfigurationInterface(dialog)
        #dialog.resize(300,200)
        dialog.exec_()

class KonsoleWidgetIcon(Plasma.IconWidget):
    def __init__(self, parent):
        Plasma.IconWidget.__init__(self,KIcon("utilities-terminal"),"Popup Konsole")
        self.setToolTip("Click to open a popup Konsole window")
        self.setMinimumIconSize(QSizeF(31,31))        

def CreateApplet(parent):
    return KonsoleWidget(parent)

