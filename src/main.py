# main.py
#
# Copyright 2020 Kavya Gokul
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import sys

import gi

gi.require_version('Gtk', '3.0')

from gi.repository import Gdk, Gio, GLib, Gtk, Pango

from .browser_mappings import BrowserMappings
from .window import BrausWindow


class Application(Gtk.Application):

    content_types = ["x-scheme-handler/http",
        "x-scheme-handler/https",
        "text/html",
        "application/x-extension-htm",
        "application/x-extension-html",
        "application/x-extension-shtml",
        "application/xhtml+xml",
        "application/x-extension-xht"
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(
            *args,
            application_id='com.properlypurple.braus',
            flags=Gio.ApplicationFlags.HANDLES_COMMAND_LINE | Gio.ApplicationFlags.NON_UNIQUE,
            **kwargs
        )

        self.settings = Gio.Settings.new("com.properlypurple.braus")
        self.browser_mappings = BrowserMappings(self.settings)

        # self.add_main_option(
        #     "",
        #     ord("u"),
        #     GLib.OptionFlags.NONE,
        #     GLib.OptionArg.NONE,
        #     "URL to open",
        #     None,
        # )

    def do_activate(self):
        self.win = BrausWindow(self)
        self.win.show_all()

    def do_command_line(self, command_line):
        args = command_line.get_arguments()
        try:
            if(len(args)> 0):
                if(args[1] =='--set'):
                    url = args[2]
                    browser = args[3]
                    self.browser_mappings.do_setbrowser(url, browser)
                    return 0

                if(args[1] =='--clear'):
                    self.browser_mappings.do_clearbrowsermappings()
                    return 0
        except IndexError:
            print("No arguments provided")

        self.activate()
        return 0

    def do_startup(self):
        Gtk.Application.do_startup(self)

    def on_about(self, action):
        about_dialog = Gtk.AboutDialog(transient_for=self.win, modal=True)

        about_dialog.set_title(_("About"))
        about_dialog.set_program_name(_("Braus"))
        about_dialog.set_comments("A small app to choose a browser to open your links")
        about_dialog.set_website("https://braus.properlypurple.com")
        about_dialog.set_website_label("Braus website")
        about_dialog.set_authors(["Kavya Gokul"])
        about_dialog.connect('response', lambda dialog, data: dialog.destroy())
        about_dialog.set_logo_icon_name('applications-internet')
        about_dialog.present()

def main(version):
    app = Application()
    return app.run(sys.argv)
