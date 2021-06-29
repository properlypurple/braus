# window.py
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

from gi.repository import Gdk, Gio, GLib, Gtk, Pango


class BrausWindow(Gtk.ApplicationWindow):
    __gtype_name__ = 'BrausWindow'
    browsers = []
    entry = Gtk.Entry()

    def __init__(self, app):
        super().__init__(title="Braus", application=app)

        # Set it to open in center
        self.set_position(Gtk.WindowPosition.CENTER_ALWAYS)

        # Set to not be resizable
        self.set_resizable(False)

        self.connect('key-release-event', self.keyboard_handle, app)

        settings = Gtk.Settings.get_default()
        settings.set_property('gtk-application-prefer-dark-theme', True)

        # Putting some css in a string
        css = b"""
        * {
        }
        decoration {
            border: 1px solid rgba(0,0,0,0.8);
            box-shadow: none;
            outline: none;
        }
        window.background.csd {
            background: none;
            background-color: rgba(20,20,20,0.95);
            border: none;
        }
        #headerbar {
            background: none;
            background-color: rgba(20,20,20,0.95);
            box-shadow: none;
            border: none;
            padding: 5px 10px 0;
            border-bottom: 1px solid rgba(0,0,0,0.5);
        }
        #headerbar entry {
            background: rgba(0,0,0,0.4);
            color: #ffffff;
            font-size: 0.6em;
            border-radius: 10px;
            border: 1px solid rgba(0,0,0, 0.4);
            outline: none;
            margin:10px 0;
        }
        #headerbar entry:focus {
            border: 1px solid rgba(255,255,255, 0.4);
            outline: none;
            box-shadow: none;
        }

        button decoration {
            border-radius: initial;
            border: initial;
        }

        #mainbox {
            background: none;
            padding: 10px;
        }

        #mainbox button {
            background: none;
            border: 1px solid rgba(255,255,255, 0.4);
        }

        #mainbox button:hover {
            background-color: rgba(255,255,255,0.1);
        }

        #browser-btn {
            padding: 18px 12px;
            font-size: 0.8rem;
        }

        #hotkey-btn {
            margin-top: 10px;
            font-size: 0.8rem;
        }

        #browsericon {
            margin-bottom: 6px;
        }
        """
        # Applying the custom css to the app
        style_provider = Gtk.CssProvider()
        style_provider.load_from_data(css)

        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            style_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )


        #Create headerbar and add to window as titlebar
        hb = Gtk.HeaderBar()
        hb.set_show_close_button(True)
        hb.set_name("headerbar")
        hb.props.title = ""
        self.set_titlebar(hb)

        Gtk.StyleContext.add_class(hb.get_style_context(), Gtk.STYLE_CLASS_FLAT)

        # Create a entry, put the url argument in the entry, and add to headerbar
        self.entry.set_icon_from_icon_name(Gtk.EntryIconPosition.PRIMARY, "system-search-symbolic")
        try:
            self.entry.set_text(sys.argv[1])
        except IndexError:
            print("No url provided")

        self.entry.set_width_chars(35)
        hb.add(self.entry)

        # Create an options button
        optionsbutton = Gtk.MenuButton.new()
        try:
            optionsbutton.add(Gtk.Image.new_from_icon_name('settings-symbolic', Gtk.IconSize.LARGE_TOOLBAR))
        except:
            optionsbutton.add(Gtk.Image.new_from_icon_name('preferences-system', Gtk.IconSize.LARGE_TOOLBAR))
        hb.pack_end(optionsbutton)

        optionsmenu = Gtk.Menu.new()
        optionsmenu.set_name("optionsmenu")
        optionsbutton.set_popup(optionsmenu)

        aboutmenuitem = Gtk.MenuItem.new()
        aboutmenuitem.set_label("About")
        aboutmenuitem.connect("activate", app.on_about)
        optionsmenu.append(aboutmenuitem)

        quitmenuitem = Gtk.MenuItem.new()
        quitmenuitem.set_label("Quit")
        quitmenuitem.connect("activate", self.quitApp, app)
        optionsmenu.append(quitmenuitem)

        optionsmenu.show_all()

        # outerbox
        outerbox = Gtk.Box()
        outerbox.set_orientation(Gtk.Orientation.VERTICAL)

        self.add(outerbox)


        # create a horizontal box to hold browser buttons
        hbox = Gtk.Box()
        hbox.set_name("mainbox")
        hbox.set_orientation(Gtk.Orientation.HORIZONTAL)
        hbox.set_spacing(10)
        hbox.set_homogeneous(True)

        outerbox.add(hbox)

        # Create an infobar to help the user set Braus as default
        infobar = Gtk.InfoBar()
        infobar.set_message_type(Gtk.MessageType.QUESTION)
        infobar.set_show_close_button(True)
        infobar.connect("response", self.on_infobar_response, app)

        infolabel = Gtk.Label("Set Braus as your default browser")
        content = infobar.get_content_area()
        content.add(infolabel)

        infobuttonnever = Gtk.Button.new_with_label(_("Never ask again"))
        Gtk.StyleContext.add_class(infobuttonnever.get_style_context(), Gtk.STYLE_CLASS_FLAT)
        
        infobar.add_action_widget(infobuttonnever, Gtk.ResponseType.REJECT)
        infobar.add_button (_("Set as Default"), Gtk.ResponseType.ACCEPT)
        
        

        if app.settings.get_boolean("ask-default") == True and Gio.AppInfo.get_default_for_type(app.content_types[1], True).get_id() != Gio.Application.get_application_id(app) + '.desktop' :
            outerbox.add(infobar)
        

        # Get all apps which are registered as browsers
        browsers = Gio.AppInfo.get_all_for_type(app.content_types[1])

        # The Gio.AppInfo.launch_uris method takes a list object, so let's make a list and put our url in there
        uris = []
        uris.append(self.entry.get_text())

        #create an empty dict to use later
        appslist = {}

        self.do_checkUrlMappings(app, self.entry.get_text(), browsers)

        # Remove Braus from the list of browsers
        self.browsers = list(filter(lambda b: Gio.Application.get_application_id(app) not in b.get_id(), browsers))
        
        # Loop over the apps in the list of browsers
        for index, browser in enumerate(self.browsers):
            #Get the icon and label, and put them in a button
            try:
                icon = Gtk.Image.new_from_gicon(browser.get_icon(), Gtk.IconSize.DIALOG)
            except:
                icon = Gtk.Image.new_from_icon_name('applications-internet', Gtk.IconSize.DIALOG)

            icon.set_name("browsericon")
            label= Gtk.Label.new(browser.get_display_name())
            label.set_max_width_chars(10)
            label.set_width_chars(10)
            label.set_line_wrap(True)
            label.set_ellipsize(Pango.EllipsizeMode.END)
            label.set_justify(Gtk.Justification.LEFT)

            # Every button has a vertical Gtk.Box inside
            browserBtn = Gtk.Button()
            browserBtnBox = Gtk.Box()
            browserBtnBox.set_name('browser-btn')
            browserBtnBox.set_orientation(Gtk.Orientation.VERTICAL)
            browserBtnBox.set_spacing(0)
            browserBtnBox.pack_start(icon,True, True, 0)
            browserBtnBox.pack_start(label,True, True, 0)

            browserBtn.add(browserBtnBox)
            #Connect the click signal, passing on all relevant data(browser and url)
            browserBtn.connect("clicked", self.browser_click_handle, index, app)

            # Browser entry box
            browserEntryBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
            browserEntryBox.pack_start(browserBtn, True, True, 0)

            # Hotkey recorder/indicator
            if index < 10:
                hotkeyBtn = Gtk.Label(label=str(index + 1))
                hotkeyBtn.set_name('hotkey-btn')
                hotkeyBtn.set_hexpand(False)
                hotkeyBtn.set_halign(Gtk.Align.CENTER)
                browserEntryBox.pack_end(hotkeyBtn, True, True, 0)

            # Add our button to the horizontal box we made earlier
            hbox.pack_start(browserEntryBox, True, True, 0)

    def do_checkUrlMappings(self, app, url, browsers):
        browser = app.browser_mappings.do_determinebrowser(app, url, browsers)
        if(browser):
            uris = []
            uris.append(url)
            browser.launch_uris(uris)
            self.quitApp(self,app)
                        
    def keyboard_handle(self, widget, event, app):
        index = int(Gdk.keyval_name(event.keyval)) - 1
        self.launch_browser(index, app)

    def do_checkUrlMappings(self, app, url, browsers):
        browser = app.browser_mappings.do_determinebrowser(app, url, browsers)
        if(browser):
            uris = []
            uris.append(url)
            browser.launch_uris(uris)
            self.quitApp(self,app)
                        
    # Function to actually launch the browser
    def browser_click_handle(self, target, index, app):
        self.launch_browser(index, app)

    def launch_browser(self, index, app):
        # The Gio.AppInfo.launch_uris method takes a list object, so let's make a list and put our url in there
        uris = [self.entry.get_text()]
        browser = self.browsers[index]
        browser.launch_uris(uris)
        print("Opening " + browser.get_display_name())
        self.quitApp(self, app)

    # Quit app action
    def quitApp(self, *args):
        app = args[1]
        print("Bye…")
        app.quit()

    def on_about(self, action, param):
        about_dialog = Gtk.AboutDialog(transient_for=self, modal=True)
        about_dialog.present()

    def on_infobar_response(self, infobar, response_id, app):
        infobar.hide()
        appinfo = Gio.DesktopAppInfo.new(Gio.Application.get_application_id(app) + '.desktop')

        if response_id == Gtk.ResponseType.ACCEPT:
            #set as default
            try:
                #loop through content types, and set Braus as default for those
                for content_type in app.content_types:
                    appinfo.set_as_default_for_type(content_type)

            except GLib.Error:
                print("error")
        
        elif response_id == Gtk.ResponseType.REJECT:
            #don't ask again
            app.settings.set_boolean("ask-default", False)
    