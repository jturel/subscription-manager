
import sys
import gtk

from firstboot.config import *
from firstboot.constants import *
from firstboot.functions import *
from firstboot.module import *
from firstboot.module import Module

import gettext
_ = lambda x: gettext.ldgettext("firstboot", x)
N_ = lambda x: x

sys.path.append("/usr/share/rhsm")
from gui import managergui


class moduleClass(Module, managergui.MainWindow):

    def __init__(self):
        Module.__init__(self)
        managergui.MainWindow.__init__(self)
        self.main_window.hide()
        #this value is relative to when you want to load the screen
        # so check other modules before setting
        self.priority = 200.2
        self.sidebarTitle = _("RHSM Subscriptions Management")
        self.title = _("Subscription Manager")

        #hide the subscribe/unsubscribe sidebar button
        self.glade.get_widget("")

    def apply(self, interface, testing=False):
        return RESULT_SUCCESS

    def createScreen(self):
        self.vbox = gtk.VBox(spacing=10)
        self.main_window.get_child().reparent(self.vbox)
        self.main_window.destroy()

    def initializeUI(self):
        self.refresh()

    def shouldAppear(self):
        return True

    def _get_window(self):
        return self.vbox.get_parent_window().get_user_data()
