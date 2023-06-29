from gi.repository import Gtk, Gio, GLib, Pango, Gdk

class BrowserMappings():
    def __init__(self, settings):
        self.settings = settings

    def do_setbrowser(self, url, browser):
        mappingsDict = self.do_loadUrlMappings()
        mappingsDict[url] = browser

        mappingsArr = []
        for url, browser in mappingsDict.items():
            mappingsArr.append(url + " " + browser)

        tmpVariant = GLib.Variant('aas', mappingsArr)
        self.settings.set_value("url-mapping", tmpVariant)

    def do_clearbrowsermappings(self):
        emptyVariant = GLib.Variant('aas', [])
        self.settings.set_value("url-mapping", emptyVariant)

    def do_loadUrlMappings(self):
        urlMappings = self.settings.get_value("url-mapping")
        mappingsDict = {}

        for mapping in urlMappings:
            pathToMatch = "".join(mapping).split(" ")
            mappingsDict[pathToMatch[0]] = pathToMatch[1]

        return mappingsDict
    
    def do_determinebrowser(self, app, url, browsers):
        mappingsDict = self.do_loadUrlMappings()

        for urlPattern, browserID in mappingsDict.items():
            if(not url.startswith(urlPattern)):
                continue

            for b in browsers:
                if(b.get_id() != browserID):
                    continue
                return b
                        