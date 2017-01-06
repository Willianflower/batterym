#!/usr/bin/python
# This code is an example for a tutorial on Ubuntu Unity/Gnome AppIndicators:
# http://candidtim.github.io/appindicator/2014/09/13/ubuntu-appindicator-step-by-step.html
# icons from https://materialdesignicons.com/

import os
import time
import signal
import threading

from gi.repository import Gtk as gtk
from gi.repository import AppIndicator3 as appindicator


APPINDICATOR_ID = 'batteryindicator'
indicator = None
icon = None
category = appindicator.IndicatorCategory.SYSTEM_SERVICES
th_background = None
th_background_stop = None


def run_monitoring(stop_event):
    while not stop_event.is_set():
        time.sleep(1)


def run_background_monitoring():
    global th_background
    global th_background_stop
    th_background_stop = threading.Event()
    th_background = threading.Thread(
        target=run_monitoring, args=[th_background_stop])
    th_background.start()


def set_icon(new_icon):
    global icon
    icon = new_icon
    indicator.set_icon(icon)


def setup_indicator(icon):
    global indicator
    indicator = appindicator.Indicator.new(
        APPINDICATOR_ID, icon, category)
    indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
    indicator.set_menu(build_menu())
    indicator.set_label('84% 0:21', '')
    set_icon(icon)


def build_menu():
    menu = gtk.Menu()
    item_quit = gtk.MenuItem('Quit')
    item_quit.connect('activate', quit)
    menu.append(item_quit)
    menu.show_all()
    return menu


def quit(source):
    if th_background_stop:
        th_background_stop.set()
    gtk.main_quit()


def run_forever():
    gtk.main()


def run():
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    setup_indicator(
        os.path.abspath('ic_battery_charging_white_48dp.png'))
    run_background_monitoring()
    run_forever()


if __name__ == "__main__":
    run()
