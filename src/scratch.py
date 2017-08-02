#!/usr/bin/env python3
import signal
import gi
import datetime
import time

gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')
from gi.repository import Gtk, AppIndicator3,GObject
from threading import Thread


class Indicator:
    def __init__(self):
        self.names = Names("/home/jakub/Dropbox/Projects/Meniny v liste/Name-day-indicator/sk-meniny.csv")

        self.app = 'Name\'s day'
        iconpath = "/home/jakub/Dropbox/Projects/Meniny v liste/Name-day-indicator/icon.ico"
        self.indicator = AppIndicator3.Indicator.new(
            self.app, iconpath,
            AppIndicator3.IndicatorCategory.OTHER)
        self.indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
        self.indicator.set_menu(self.create_menu())
        self.indicator.set_label(self.names.today_name().strip('"\''), self.app)
        # the thread:
        self.update = Thread(target=self.refresh)
        # daemonize the thread to make the indicator stopable
        self.update.setDaemon(True)
        self.update.start()

    def refresh(self):
        while True:
            time.sleep(60*10) #10 minutes
            # apply the interface update using  GObject.idle_add()
            GObject.idle_add(
                self.indicator.set_label,
                self.names.today_name().strip('"\''),
                self.app,
                priority=GObject.PRIORITY_DEFAULT
            )

    def create_menu(self):
        menu = Gtk.Menu()
        # menu item 1
        item_1 = Gtk.MenuItem('Menu item')
        # item_about.connect('activate', self.about)
        menu.append(item_1)
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

class Names():
    listNames = []

    def __init__(self,filename):
        self.read_file(filename)

    def read_file(self, filename):
        f=open(filename,'r')
        for line in f:
            line=line[6:len(line)-1]
            self.listNames.append(line)
        f.close()

    def today_name(self,):
        today = datetime.date.today()
        thisYear = datetime.date(today.year, 1, 1)
        delta = today - thisYear
        if self.gap_year(today.year) | delta.days<=59:
            days = delta.days
        else:
            days = delta.days + 1
        return repr(Names.listNames[days]).decode('string-escape')

    def gap_year(self,year):
        return (((year % 4 == 0) & (year % 100 != 0)) | (year % 400 == 0))


Indicator()
signal.signal(signal.SIGINT, signal.SIG_DFL)
Gtk.main()

#names=Names("/home/jakub/PycharmProjects/NamesDayBar/sk-meniny.csv")
#print names.today_name().strip('"\'')
