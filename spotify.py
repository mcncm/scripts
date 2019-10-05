#! /bin/python
"""
Author: mcncm, 2019

Methods:
"Play", "Pause", "PlayPause", "Next", "Previous"
"""

import sys

import dbus

bus_name = "org.mpris.MediaPlayer2.spotify"
object_path = "/org/mpris/MediaPlayer2"
interface = "org.mpris.MediaPlayer2.Player"

bus = dbus.SessionBus()
proxy = bus.get_object(bus_name, object_path)

def spotify_dbus_call(method):
    getattr(proxy, method)(dbus_interface=interface)

if __name__ == '__main__':
    spotify_dbus_call(sys.argv[1])
