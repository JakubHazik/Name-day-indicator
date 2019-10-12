#!/usr/bin/env python3
import signal
import gi
import datetime
import time

gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')
from gi.repository import Gtk, AppIndicator3, GObject
from threading import Thread
from gi.repository import GdkPixbuf

installationPath = "/usr/local/name-day-indicator"

class Indicator(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="MessageDialog")

        self.names = Names(installationPath + "/src/sk-meniny.csv")

        self.app = 'Name\'s day'
        self.indicator = AppIndicator3.Indicator.new(
            self.app, installationPath + "/src/calendar.png",
            AppIndicator3.IndicatorCategory.OTHER)
        self.indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
        self.indicator.set_menu(self.create_menu())
        self.indicator.set_label(self.names.name_day(datetime.date.today()), self.app)

        # the thread:
        self.update = Thread(target=self.refresh)
        # daemonize the thread to make the indicator stopable
        self.update.setDaemon(True)
        self.update.start()

    def refresh(self):
        while True:
            retazec = self.names.name_day(datetime.date.today())

            GObject.idle_add(
                self.indicator.set_label,
                retazec,
                self.app,
                priority=GObject.PRIORITY_DEFAULT
            )

            GObject.idle_add(
                self.indicator.set_menu,
                self.create_menu(),
                priority=GObject.PRIORITY_DEFAULT
            )

            time.sleep(60)  # 1 minute

    def create_menu(self):
        menu = Gtk.Menu()
        #today name
        item_1_name=datetime.date.today().day.__str__() + '. ' + self.names.name_day(datetime.date.today())
        item_1 = Gtk.MenuItem(item_1_name)
        menu.append(item_1)
        #tomorrow day name
        tomorrow=datetime.date.today() + datetime.timedelta(days=1)
        item_2_name = tomorrow.day.__str__() + '. ' + self.names.name_day(tomorrow)
        item_2 = Gtk.MenuItem(item_2_name)
        menu.append(item_2)
        #next day name
        tomorrow2 = datetime.date.today() + datetime.timedelta(days=2)
        item_3_name = tomorrow2.day.__str__() + '. ' + self.names.name_day(tomorrow2)
        item_3 = Gtk.MenuItem(item_3_name)
        menu.append(item_3)

        # separator
        menu_sep = Gtk.SeparatorMenuItem()
        menu.append(menu_sep)
        # about dialog
        item_search = Gtk.MenuItem('Search')
        item_search.connect('activate', self.dialog_search)
        menu.append(item_search)

        # separator
        menu_sep = Gtk.SeparatorMenuItem()
        menu.append(menu_sep)
        #about dialog
        item_about = Gtk.MenuItem('About')
        item_about.connect('activate', self.dialog_about)
        menu.append(item_about)

        # separator
        menu_sep = Gtk.SeparatorMenuItem()
        menu.append(menu_sep)
        # quit
        item_quit = Gtk.MenuItem('Quit')
        item_quit.connect('activate', self.stop)

        menu.append(item_quit)
        menu.show_all()
        return menu

    def stop(self, source):
        Gtk.main_quit()

    def dialog_about(self, widget):
        about = Gtk.AboutDialog()
        about.set_program_name("Name day widget")
        about.set_version("version v0.1")
        about.set_copyright(u"\u00A9"+" HAZman")
        about.set_comments("You mustn\'t forget to friends and their name day!\n This widget help you with it.\n")
        about.set_website("https://github.com/JakubHazik/Name-day-indicator")
        about.set_logo(GdkPixbuf.Pixbuf.new_from_file_at_size(installationPath + "/src/calendar.png", 64, 64))
        about.run()
        about.destroy()

    def dialog_search(self, widget):
        self.set_title("Search name in calendar")
        self.set_default_size(250, 95)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.label = Gtk.Label("Enter name")
        self.entry = Gtk.Entry()
        self.btn_search = Gtk.Button("Search")
        self.btn_search.connect("clicked",self.search)
        self.btn_cancel = Gtk.Button(stock= Gtk.STOCK_CANCEL)
        self.btn_cancel.connect("clicked", self.dialog_close)

        fixed = Gtk.Fixed()
        fixed.put(self.label, 85, 5)
        fixed.put(self.entry, 43, 20)
        fixed.put(self.btn_search, 185, 60)
        fixed.put(self.btn_cancel, 5, 60)

        self.add(fixed)
        self.show_all()

    def dialog_close(self,widget):
        self.destroy()

    def search(self, widget):
        text = self.names.search_name(self.entry.get_text())
        self.dialog_message("INFO", text)
        self.destroy()

    def dialog_message(self,type,text):
        if type=="INFO":
            md = Gtk.MessageDialog(self,
                                   0, Gtk.MessageType.INFO,
                                   Gtk.ButtonsType.OK, text)
            md.run()
            md.destroy()

class Names():
    listNames = []

    def __init__(self, filename):
        self.read_file(filename)

    def read_file(self, filename):
        f = open(filename, 'r')
        for line in f:
            line = line[6:len(line) - 1]
            self.listNames.append(line)
        f.close()

    def name_day(self, date):
        thisYear = datetime.date(date.year, 1, 1)
        delta = date - thisYear
        if self.gap_year(date.year) | delta.days <= 59:
            days = delta.days
        else:
            days = delta.days + 1
        return str(Names.listNames[days])

    def search_name(self,name):
        if name=="":
            return "Sorry, but you are noob"
        name=name.lower()
        name=name[0].upper()+name[1:]

        year= datetime.date(datetime.date.today().year,1,1)
        try:
            days = self.listNames.index(name) - 1
        except:
            return "Name didn\'t find."
        delta= datetime.timedelta(days)
        date = year+delta

        if date<datetime.date.today():
            date=date+datetime.timedelta(days=365)

        return date.strftime("The earliest date: \n%d. %B %Y \n%A")

    def gap_year(self, year):
        return (((year % 4 == 0) & (year % 100 != 0)) | (year % 400 == 0))

indicator=Indicator()
signal.signal(signal.SIGINT, signal.SIG_DFL)
Gtk.main()
