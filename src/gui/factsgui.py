#
# GUI Module for standalone subscription-manager - System Facts Dialog
#
# Copyright (c) 2010 Red Hat, Inc.
#
# Authors: Justin Harris <jharris@redhat.com>
#
# This software is licensed to you under the GNU General Public License,
# version 2 (GPLv2). There is NO WARRANTY for this software, express or
# implied, including the implied warranties of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. You should have received a copy of GPLv2
# along with this software; if not, see
# http://www.gnu.org/licenses/old-licenses/gpl-2.0.txt.
#
# Red Hat trademarks are not licensed under GPLv2. No permission is
# granted to use or replicate Red Hat trademarks that are incorporated
# in this software or its documentation.
#

import os
import gtk

import connection
import facts
import managergui

import logutil
log = logutil.getLogger(__name__)

DIR = os.path.dirname(__file__)
GLADE_XML = os.path.join(DIR, "data/factsdialog.glade")

class SystemFactsDialog:
    """GTK dialog for displaying the current system facts, as well as
    providing functionality to update the UEP server with the current
    system facts.
    """

    def __init__(self):
        glade = gtk.glade.XML(GLADE_XML)
        glade.signal_autoconnect({
                "on_system_facts_dialog_delete_event" : self.__hide_callback,
                "on_close_button_clicked" : self.__hide_callback,
                "on_facts_update_button_clicked" : self.__update_facts_callback
                })

        self.dialog = glade.get_widget("system_facts_dialog")
        self.facts_view = glade.get_widget("system_facts_view")
        self.update_button = glade.get_widget("update_facts_button")

        # Set up the model
        self.facts_store = gtk.ListStore(str, str)
        self.facts_view.set_model(self.facts_store)

        # Set up columns on the view
        self.__add_column("Fact", 0)
        self.__add_column("Value", 1)

        # Update the displayed facts
        self.display_facts()

        # Set sorting by fact name
        self.facts_store.set_sort_column_id(0, gtk.SORT_ASCENDING)

    def show(self):
        """Make this dialog visible."""
        # Disable the 'Update' button if there is
        # no registered consumer to update
        self.update_button.set_sensitive(bool(managergui.consumer))
        self.dialog.present()

    def hide(self):
        """Make this dialog invisible."""
        self.dialog.hide()

    def display_facts(self):
        """Updates the list store with the current system facts."""
        self.facts_store.clear()

        system_facts = facts.getFacts().get_facts()
        for fact, value in system_facts.items():
            self.facts_store.append([fact, value])

    def update_facts(self):
        """Sends the current system facts to the UEP server."""
        system_facts = facts.getFacts().get_facts()
        consumer_uuid = managergui.consumer['uuid']

        try:
            managergui.UEP.updateConsumerFacts(consumer_uuid, system_facts)
        except connection.RestlibException, e:
            log.error("Could not update system facts:  error %s" % e)
            managergui.errorWindow(managergui.linkify(str(e)))
        except Exception, e:
            log.error("Could not update system facts \nError: %s" % e)
            managergui.errorWindow(managergui.linkify(str(e)))

    # GTK callback function for hiding this dialog.
    def __hide_callback(self, button, event=None):
        self.hide()

        # Stop the gtk signal from propogating
        return True

    # GTK callback function for sending system facts to the server
    def __update_facts_callback(self, button):
        self.update_facts()

    def __add_column(self, name, order):
        """Adds a gtk.TreeViewColumn suitable for displaying text to
        the facts gtk.TreeView.

        @type   name: string
        @param  name: The name of the created column
        @type  order: integer
        @param order: The 0-based index of the created column
        (in relation to other columns)
        """
        column = gtk.TreeViewColumn(name, gtk.CellRendererText(), text=order)
        self.facts_view.append_column(column)


