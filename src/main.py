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

from gi.repository import Gtk, Gio, GLib, Pango, Gdk

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
            flags=Gio.ApplicationFlags.HANDLES_COMMAND_LINE,
            **kwargs
        )

        self.settings = Gio.Settings.new("com.properlypurple.braus")

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
        self.activate()
        return 0

    def do_startup(self):
        Gtk.Application.do_startup(self)


def main(version):
    app = Application()
    return app.run(sys.argv)
