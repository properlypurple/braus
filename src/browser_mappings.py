from gi.repository import Gtk, Gio, GLib, Pango, Gdk

class BrowserMappings():
    def __init__(self, settings):
        self.settings = settings

    def do_setbrowser(self, url, browser):
        mappingsArr = self.do_loadUrlMappings()
        mappingsArr.append(url + " " + browser)

        tmpVariant = GLib.Variant('aas', mappingsArr)
        self.settings.set_value("url-mapping", tmpVariant)

    def do_clearbrowsermappings(self):
        mappingsArr=[]
        tmpVariant = GLib.Variant('aas', mappingsArr)
        self.settings.set_value("url-mapping", tmpVariant)
    
    def do_loadUrlMappings(self):
        urlMappings = self.settings.get_value("url-mapping")
        mappingsArr = []
        for mapping in urlMappings:
            pathToMatch = "".join(mapping)
            mappingsArr.append(pathToMatch)

        return mappingsArr
    
    def do_determinebrowser(self, app, url, browsers):
        mappingsArr = self.do_loadUrlMappings()

        for mapping in mappingsArr:
            matcher = mapping.split(" ")

            if(not url.startswith(matcher[0])):
                continue

            for browser in browsers:
                if(browser.get_id() != matcher[1]):
                    continue
                return browser
                        