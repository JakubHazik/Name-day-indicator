#!/usr/bin/env python3
import signal
import gi
import datetime
import time


gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')
from gi.repository import Gtk, AppIndicator3, GObject
from threading import Thread

#from pythonzenity import Message


class Indicator(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="MessageDialog")

        self.names = Names("/home/jakub/Dropbox/Projects/Meniny_v_liste/Name-day-indicator/src/sk-meniny.csv")

        self.app = 'Name\'s day'
        iconpath = "/home/jakub/Dropbox/Projects/Meniny_v_liste/Name-day-indicator/src/icon.ico"
        self.indicator = AppIndicator3.Indicator.new(
            self.app, iconpath,
            AppIndicator3.IndicatorCategory.OTHER)
        self.indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
        self.indicator.set_menu(self.create_menu())
        self.indicator.set_label(self.names.name_day(), self.app)
        # the thread:
        self.update = Thread(target=self.refresh)
        # daemonize the thread to make the indicator stopable
        self.update.setDaemon(True)
        self.update.start()

    def refresh(self):
        while True:
            time.sleep(60 * 10)  # 10 minutes
            # apply the interface update using  GObject.idle_add()
            GObject.idle_add(
                self.indicator.set_label,
                self.names.name_day(),
                self.app,
                priority=GObject.PRIORITY_DEFAULT
            )
            self.indicator.set_menu(self.create_menu())

    def about_message(self, widget):
        #dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.INFO,Gtk.ButtonsType.OK, "Name day widget")
        #Gtk.AboutDialog()
        #dialog.format_secondary_text("You mustn\'t forget to friends and their name day! This widget help you with it.\n"
        #                             u"\u00A9" + "Created by HAZman")
        #dialog.run()
        #dialog.destroy()
        about = Gtk.AboutDialog()
        about.set_program_name("Battery")
        about.set_version("0.1")
        about.set_copyright(u"\u00A9"+" Jan Bodnar")
        about.set_comments("Battery is a simple tool for battery checking")
        about.set_website("http://www.zetcode.com")
        #about.set_logo(Gtk.Window.set_icon("/home/jakub/Dropbox/Projects/Meniny_v_liste/Name-day-indicator/src/calendar.png"))
        about.set_logo(gtk.gdk.pixbuf_new_from_file( "calendar.png"))
        about.run()
        about.destroy()

    def create_menu(self):
        menu = Gtk.Menu()
        #today name
        item_1_name=datetime.date.today().day.__str__() + '. ' + self.names.name_day()
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
        item_search.connect('activate', self.search_dialog)
        menu.append(item_search)

        # separator
        menu_sep = Gtk.SeparatorMenuItem()
        menu.append(menu_sep)
        #about dialog
        item_about = Gtk.MenuItem('About')
        item_about.connect('activate', self.about_message)
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

    def search_dialog(self, widget):
        self.set_title("Search name in calendar")
        self.set_default_size(250, 95)
        #self.set_position()
        self.label = Gtk.Label("Enter name")
        self.entry = Gtk.Entry()
        self.btn_search = Gtk.Button("Search")
        self.btn_search.connect("clicked",self.search)
        self.btn_cancel = Gtk.Button(stock= Gtk.STOCK_CANCEL)
        self.btn_cancel.connect("clicked", )

        fixed = Gtk.Fixed()
        fixed.put(self.label, 85, 5)
        fixed.put(self.entry, 43, 20)
        fixed.put(self.btn_search, 185, 60)
        fixed.put(self.btn_cancel, 5, 60)

        self.add(fixed)
        self.show_all()
        #time.sleep(10)
        #self.destroy()



    def search(self, widget):
        print self.names.search_name(self.entry.get_text())
        #print "hello", self.entry.get_text()

    def stop(self, source):
        Gtk.main_quit()

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

    def name_day(self, date=datetime.date.today()):
        thisYear = datetime.date(date.year, 1, 1)
        delta = date - thisYear
        if self.gap_year(date.year) | delta.days <= 59:
            days = delta.days
        else:
            days = delta.days + 1
        return str(Names.listNames[days]).decode('string-escape')

    def search_name(self,name):
        year= datetime.date(datetime.date.today().year,1,1)
        delta= datetime.timedelta(days=self.listNames.index(name)-1)
        return year+delta

    def gap_year(self, year):
        return (((year % 4 == 0) & (year % 100 != 0)) | (year % 400 == 0))


indicator=Indicator()
signal.signal(signal.SIGINT, signal.SIG_DFL)
Gtk.main()




names=Names("/home/jakub/Dropbox/Projects/Meniny_v_liste/Name-day-indicator/src/sk-meniny.csv")
#print names.search_name("Jo")
# print names.today_name().strip('"\'')
