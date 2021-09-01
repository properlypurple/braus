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

from gi.repository import Gtk, Gio, GLib, Pango, Gdk
import sys

class BrausWindow(Gtk.ApplicationWindow):
    __gtype_name__ = 'BrausWindow'

    def __init__(self, app):
        super().__init__(title="Braus", application=app)

        # Set it to open in center
        self.set_position(Gtk.WindowPosition.CENTER_ALWAYS)

        # Set to not be resizable
        self.set_resizable(False)

        settings = Gtk.Settings.get_default()
        settings.set_property('gtk-application-prefer-dark-theme', True)

        # Applying the custom css to the app
        style_provider = Gtk.CssProvider()
        style_provider.load_from_data(app.resources.lookup_data('/ui/application-window.css', 0).get_data())

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
        entry = Gtk.Entry()
        entry.set_icon_from_icon_name(Gtk.EntryIconPosition.PRIMARY, "system-search-symbolic")
        try:
            entry.set_text(sys.argv[1])
        except IndexError:
            print("No url provided")

        entry.set_width_chars(35)
        hb.add(entry)

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
        
        

        if app.settings.get_boolean("ask-default") == True or (Gio.AppInfo.get_default_for_type(app.content_types[1], True).get_id() != Gio.Application.get_application_id(app) + '.desktop') :
            outerbox.add(infobar)
        

        # Get all apps which are registered as browsers
        browsers = Gio.AppInfo.get_all_for_type(app.content_types[1])

        # The Gio.AppInfo.launch_uris method takes a list object, so let's make a list and put our url in there
        uris = []
        uris.append(entry.get_text())

        #create an empty dict to use later
        appslist = {}

        # Loop over the apps in the list of browsers
        for browser in browsers:

            #print(Gio.Application.get_application_id(app))
            #print(browser.get_id())

            # Remove Braus from the list of browsers
            if Gio.Application.get_application_id(app) + '.desktop' == browser.get_id() :
                continue
            

            #put the current one in the loop, in a dict
            appslist.update({browser.get_id() : browser})

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

            #Every button has a vertical Gtk.Box inside
            vbox = Gtk.Box()
            vbox.set_orientation(Gtk.Orientation.VERTICAL)
            vbox.set_spacing(0)

            vbox.pack_start(icon,True, True, 0)
            vbox.pack_start(label,True, True, 0)

            button = Gtk.Button(name='browser-btn')

            button.add(vbox)

            # Add our button to the horizontal box we made earlier
            hbox.pack_end(button, True, True, 0)

            #Connect the click signal, passing on all relevant data(browser and url)
            button.connect("clicked", self.launch_browser, appslist.get(browser.get_id()), uris, app)



    # Function to actually launch the browser
    def launch_browser(self, button, browser, uris, app):
        browser.launch_uris(uris)
        print("Opening " + browser.get_display_name())
        self.quitApp(self,app)

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
    